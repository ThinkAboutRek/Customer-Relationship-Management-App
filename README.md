# Django CRM App

A lightweight Customer Relationship Management (CRM) web application built with Django 5.2, featuring:

- **User Authentication**  
  - Custom **login page** (`/login/`) that handles `?next=` redirects  
  - **Registration** with unique-email validation  
  - **Logout**  
  - Already-logged-in users are auto-redirected away from login/register

- **Protected Views**  
  - `@login_required` on all CRUD & dashboard views  
  - **Home** (`/`) protected without appending `?next=`  
  - Automatic redirect to `/login/` when unauthenticated

- **Customer Records CRUD**  
  - **List** all records (Dashboard)  
  - **Detail** view (`/record/<pk>/`)  
  - **Add** record (`/add_record/`) with unique email & phone validation  
  - **Update** record (`/update_record/<pk>/`)  
  - **Delete** record (`/delete_record/<pk>/`)

- **Flash Messages**  
  - Centralized in **base.html**’s fixed alert container  
  - Styled via Bootstrap 5  
  - Error flashes use `alert-danger`, success `alert-success`, warning `alert-warning`

- **Form Styling**  
  - Subclasses of `AuthenticationForm` & `UserCreationForm` for consistent Bootstrap 5 widgets  
  - Field-level help texts, placeholders, and inline validation

- **Theme Toggle**  
  - Light / Dark mode switch in navbar (stored in `localStorage`)

---

## 📂 Project Structure

```
CRM App/
├── D_CRM/                   # Django project settings
│   ├── settings.py         # with LOGIN_URL = 'login'
│   ├── urls.py             # root URLconf
│   └── wsgi.py, asgi.py
├── CRM_Website/             # Main CRM app
│   ├── admin.py            # Record registration
│   ├── forms.py            # LoginForm, SignUpForm, AddRecordForm
│   ├── models.py           # Record model
│   ├── tests.py            # (stub for unit tests)
│   ├── urls.py             # app-level URLconf (with trailing slashes)
│   └── views.py            # function-based views with @login_required
├── templates/
│   ├── base.html           # Global layout & flash messages
│   ├── navbar.html         # Navbar with theme toggle
│   ├── home.html           # Dashboard (protected)
│   ├── login.html          # Login page (no inline message loop)
│   ├── register.html       # Registration page
│   ├── add_record.html     # Add-record form
│   ├── record.html         # Detail view
│   ├── update_record.html  # Update-record form
│   └── …
├── static/                 # CSS, JS, images
├── manage.py               # Django CLI
├── mydb.py                 # MySQL initialization script (optional)
├── .env                    # Environment vars (gitignored)
├── .gitignore
├── Pipfile & Pipfile.lock  # Pipenv dependencies
└── README.md               # ← you're here
```

---

## 💻 Technologies & Dependencies

- **Django** – High-level Python web framework  
- **MySQL** – Relational database for data persistence  
- **Pipenv** – Virtual environment & dependency management  
- **python-dotenv** – Securely load environment variables  
- **Bootstrap 5** – Modern, responsive UI components  
- **Git & GitHub** – Version control and hosting  

### 📦 Pipenv Packages Installed

```bash
pipenv install django
pipenv install mysqlclient
pipenv install pymysql
pipenv install cryptography
pipenv install mysql-connector-python
pipenv install python-dotenv
```

---

## 🔧 Installation & Setup

1. **Clone & enter**  
   ```bash
   git clone https://github.com/ThinkAboutRek/ThinkAboutRek-Customer-Relationship-Management-App.git
   cd ThinkAboutRek-Customer-Relationship-Management-App
   ```

2. **Install dependencies & activate environment**  
   ```bash
   pip install pipenv      # if not already installed
   pipenv install
   pipenv shell
   ```

3. **Configure `.env`**  
   Create a `.env` file in the project root:
   ```ini
   SECRET_KEY=your_secret_key
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost
   LOGIN_URL=login
   MYSQL_NAME=CRM_DB
   MYSQL_USER=root
   MYSQL_PASSWORD=yourpassword
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   ```

4. **Initialize the database** (optional)  
   ```bash
   python mydb.py
   ```

5. **Apply migrations & create superuser**  
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run the development server**  
   ```bash
   python manage.py runserver
   ```

7. **Visit** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🚀 Usage

1. **Register** at `/register/`  
2. **Log in** at `/login/` (redirects back to intended page)  
3. **Dashboard** `/` – list all records  
4. **View** a record at `/record/<pk>/`  
5. **Add** at `/add_record/`  
6. **Edit** at `/update_record/<pk>/`  
7. **Delete** at `/delete_record/<pk>/`

---

## 🔧 Customizations

* **Unique validations** in `AddRecordForm.clean_email()` & `clean_phone()`  
* **Custom `login_user`** handles `?next`, blocks auth’d users, and uses `form.get_user()`  
* **Global flashes** in `base.html` (no duplicates)

---

## 📄 License

Open-source for educational and portfolio use.

---

Made with ☕ and curiosity by **Shayan Bagheri (ThinkAboutRek)**