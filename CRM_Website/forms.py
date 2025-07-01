from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Record

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username'
        })
        self.fields['username'].label = ''

        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password'].label = ''


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        })
    )
    first_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username'
        })
        self.fields['username'].label = ''
        self.fields['username'].help_text = (
            '<span class="form-text text-muted"><small>'
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
            '</small></span>'
        )

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = (
            '<ul class="form-text text-muted small">'
            '<li>Your password can\'t be too similar to your other personal information.</li>'
            '<li>Your password must contain at least 8 characters.</li>'
            '<li>Your password can\'t be a commonly used password.</li>'
            '<li>Your password can\'t be entirely numeric.</li>'
            '</ul>'
        )

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = (
            '<span class="form-text text-muted"><small>'
            'Enter the same password as before, for verification.'
            '</small></span>'
        )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("That email is already registered.")
        return email

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        # save the email field (first_name/last_name are handled by super().save())
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class AddRecordForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True,
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "First Name",
            "class": "form-control"
        })
    )
    last_name = forms.CharField(
        required=True,
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "Last Name",
            "class": "form-control"
        })
    )
    email = forms.EmailField(
        required=True,
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "Email",
            "class": "form-control"
        })
    )
    phone = forms.CharField(
        required=True,
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "Phone",
            "class": "form-control"
        })
    )
    address = forms.CharField(
        required=True,
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "Address",
            "class": "form-control"
        })
    )
    city = forms.CharField(
        required=True,
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "City",
            "class": "form-control"
        })
    )
    county = forms.CharField(
        required=True,
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "County",
            "class": "form-control"
        })
    )
    postcode = forms.CharField(
        required=True,
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "Postcode",
            "class": "form-control"
        })
    )

    class Meta:
        model = Record
        fields = '__all__'
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Record.objects.filter(email__iexact=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("That email is already in use.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        qs = Record.objects.filter(phone__iexact=phone)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("That phone number is already in use.")
        return phone