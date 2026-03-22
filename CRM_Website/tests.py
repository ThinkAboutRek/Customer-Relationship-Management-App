from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Record


class RecordModelTest(TestCase):

    def test_str_returns_full_name(self):
        record = Record(first_name='Jane', last_name='Doe')
        self.assertEqual(str(record), 'Jane Doe')

    def test_company_and_notes_default_to_empty(self):
        record = Record.objects.create(
            first_name='Jane', last_name='Doe',
            email='jane@example.com', phone='07000000000',
            address='1 Test St', city='London',
            county='Greater London', postcode='E1 1AA'
        )
        self.assertEqual(record.company, '')
        self.assertEqual(record.notes, '')


class AuthViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='TestPass123!')

    def test_home_redirects_when_not_logged_in(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response['Location'])

    def test_home_accessible_when_logged_in(self):
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_loads(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_with_valid_credentials(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'TestPass123!'
        })
        self.assertRedirects(response, reverse('home'))

    def test_login_with_invalid_credentials(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please correct the errors below.')

    def test_logout_redirects_to_login(self):
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

    def test_register_page_loads(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_register_creates_user_and_logs_in(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_logged_in_user_redirected_from_login(self):
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('login'))
        self.assertRedirects(response, reverse('home'))

    def test_logged_in_user_redirected_from_register(self):
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('register'))
        self.assertRedirects(response, reverse('home'))


class RecordCRUDTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='TestPass123!')
        self.client.login(username='testuser', password='TestPass123!')
        self.record = Record.objects.create(
            first_name='John', last_name='Smith',
            email='john@example.com', phone='07111111111',
            address='2 Example Rd', city='Manchester',
            county='Greater Manchester', postcode='M1 1AA'
        )

    def test_add_record(self):
        response = self.client.post(reverse('add_record'), {
            'first_name': 'Alice', 'last_name': 'Brown',
            'email': 'alice@example.com', 'phone': '07222222222',
            'company': 'Acme Ltd',
            'address': '3 New St', 'city': 'Leeds',
            'county': 'West Yorkshire', 'postcode': 'LS1 1AA',
            'notes': '',
        })
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(Record.objects.filter(email='alice@example.com').exists())

    def test_view_record_detail(self):
        response = self.client.get(reverse('record', args=[self.record.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John')
        self.assertContains(response, 'Smith')

    def test_update_record(self):
        response = self.client.post(reverse('update_record', args=[self.record.pk]), {
            'first_name': 'John', 'last_name': 'Updated',
            'email': 'john@example.com', 'phone': '07111111111',
            'company': '',
            'address': '2 Example Rd', 'city': 'Manchester',
            'county': 'Greater Manchester', 'postcode': 'M1 1AA',
            'notes': '',
        })
        self.assertRedirects(response, reverse('home'))
        self.record.refresh_from_db()
        self.assertEqual(self.record.last_name, 'Updated')

    def test_delete_record_via_post(self):
        response = self.client.post(reverse('delete_record', args=[self.record.pk]))
        self.assertRedirects(response, reverse('home'))
        self.assertFalse(Record.objects.filter(pk=self.record.pk).exists())

    def test_delete_record_via_get_does_not_delete(self):
        response = self.client.get(reverse('delete_record', args=[self.record.pk]))
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(Record.objects.filter(pk=self.record.pk).exists())

    def test_record_detail_returns_404_for_missing_record(self):
        response = self.client.get(reverse('record', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_add_record_form_page_loads(self):
        response = self.client.get(reverse('add_record'))
        self.assertEqual(response.status_code, 200)

    def test_update_record_form_page_loads(self):
        response = self.client.get(reverse('update_record', args=[self.record.pk]))
        self.assertEqual(response.status_code, 200)


class FormValidationTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='TestPass123!')
        self.client.login(username='testuser', password='TestPass123!')
        Record.objects.create(
            first_name='Existing', last_name='User',
            email='taken@example.com', phone='07333333333',
            address='1 Old St', city='Bristol',
            county='Avon', postcode='BS1 1AA'
        )

    def test_update_does_not_reject_own_email(self):
        record = Record.objects.create(
            first_name='Update', last_name='Test',
            email='myemail@example.com', phone='07800000000',
            address='5 Test Rd', city='London',
            county='Greater London', postcode='E1 2BB'
        )
        response = self.client.post(reverse('update_record', args=[record.pk]), {
            'first_name': 'Update', 'last_name': 'Test',
            'email': 'myemail@example.com', 'phone': '07800000000',
            'company': '', 'address': '5 Test Rd',
            'city': 'London', 'county': 'Greater London', 'postcode': 'E1 2BB',
            'notes': '',
        })
        self.assertRedirects(response, reverse('home'))

    def test_add_record_rejects_duplicate_email(self):
        response = self.client.post(reverse('add_record'), {
            'first_name': 'Another', 'last_name': 'Person',
            'email': 'taken@example.com', 'phone': '07444444444',
            'company': '', 'address': '2 New St',
            'city': 'Bristol', 'county': 'Avon', 'postcode': 'BS2 2AA',
            'notes': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'already in use')

    def test_add_record_rejects_duplicate_phone(self):
        response = self.client.post(reverse('add_record'), {
            'first_name': 'Another', 'last_name': 'Person',
            'email': 'other@example.com', 'phone': '07333333333',
            'company': '', 'address': '2 New St',
            'city': 'Bristol', 'county': 'Avon', 'postcode': 'BS2 2AA',
            'notes': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'already in use')

    def test_register_rejects_duplicate_email(self):
        self.client.logout()
        User.objects.create_user(username='existing', password='Pass123!', email='used@example.com')
        response = self.client.post(reverse('register'), {
            'username': 'newperson',
            'first_name': 'New', 'last_name': 'Person',
            'email': 'used@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'already registered')


class SearchAndExportTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='TestPass123!')
        self.client.login(username='testuser', password='TestPass123!')
        Record.objects.create(
            first_name='Alice', last_name='Smith',
            email='alice@example.com', phone='07555555555',
            company='Acme Ltd', address='1 Test St',
            city='London', county='Greater London', postcode='E1 1AA'
        )
        Record.objects.create(
            first_name='Bob', last_name='Jones',
            email='bob@example.com', phone='07666666666',
            company='Globex', address='2 Test St',
            city='Leeds', county='West Yorkshire', postcode='LS1 1AA'
        )

    def test_search_returns_matching_records(self):
        response = self.client.get(reverse('home') + '?q=alice')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alice')
        self.assertNotContains(response, 'Bob')

    def test_search_by_company(self):
        response = self.client.get(reverse('home') + '?q=Globex')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bob')
        self.assertNotContains(response, 'Alice')

    def test_empty_search_returns_all_records(self):
        response = self.client.get(reverse('home') + '?q=')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alice')
        self.assertContains(response, 'Bob')

    def test_export_csv_returns_correct_content_type(self):
        response = self.client.get(reverse('export_records'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')

    def test_export_csv_contains_all_records(self):
        response = self.client.get(reverse('export_records'))
        content = response.content.decode('utf-8')
        self.assertIn('alice@example.com', content)
        self.assertIn('bob@example.com', content)

    def test_export_csv_respects_search_filter(self):
        response = self.client.get(reverse('export_records') + '?q=alice')
        content = response.content.decode('utf-8')
        self.assertIn('alice@example.com', content)
        self.assertNotIn('bob@example.com', content)

    def test_export_requires_authentication(self):
        self.client.logout()
        response = self.client.get(reverse('export_records'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response['Location'])

    def test_csv_has_correct_header_row(self):
        response = self.client.get(reverse('export_records'))
        first_line = response.content.decode('utf-8').splitlines()[0]
        self.assertIn('Email', first_line)
        self.assertIn('First Name', first_line)
        self.assertIn('Company', first_line)

    def test_search_with_no_results_shows_empty_table(self):
        response = self.client.get(reverse('home') + '?q=zzznomatch')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No records available.')
