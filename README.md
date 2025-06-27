# Customer Relationship Management App (CRM)

A CRM web application built with **Django**, **MySQL**, **Pipenv**, and **Bootstrap**.  
It provides user authentication, CRUD operations for customer records, theme toggle, and secure environment handling.

---

## 📁 Project Structure

```
CRM App/
├── D_CRM/                  # Django project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py         # Application settings with dotenv
│   ├── urls.py             # Root URL configurations
│   └── wsgi.py
├── CRM_Website/            # Main CRM application
│   ├── __init__.py
│   ├── admin.py            # Model registration for Django admin
│   ├── apps.py
│   ├── forms.py            # User signup & record forms
│   ├── models.py           # Record model definition
│   ├── tests.py            # Unit tests
│   ├── urls.py             # App-level URL configurations
│   └── views.py            # Views for authentication & CRUD
├── templates/              # HTML templates
│   ├── base.html           # Base layout with navbar & messages
│   ├── navbar.html         # Navigation bar with theme toggle
│   ├── home.html           # Dashboard & login form
│   ├── register.html       # User registration page
│   ├── add_record.html     # Form page to add a record
│   ├── record.html         # Detail view of a single record
│   └── update_record.html  # Form page to update a record
├── static/                 # Static files (CSS, JS, images)
├── manage.py               # Django management script
├── mydb.py                 # Script to initialize MySQL database
├── .env                    # Environment variables (ignored by git)
├── .gitignore              # Ignore env & temporary files
├── Pipfile                 # Pipenv dependencies
├── Pipfile.lock
└── README.md               # Project documentation
```

---

## 💻 Technologies

- **Django** – High-level Python web framework  
- **MySQL** – Relational database for data persistence  
- **Pipenv** – Virtual environment and dependency management  
- **python-dotenv** – Securely load environment variables  
- **Bootstrap 5** – Modern, responsive UI components  
- **Git & GitHub** – Version control and hosting  

---

## 🔧 Installation & Setup

1. **Clone the repository**  
   ```bash
   git clone https://github.com/ThinkAboutRek/ThinkAboutRek-Customer-Relationship-Management-App.git
   cd ThinkAboutRek-Customer-Relationship-Management-App
   ```

2. **Install dependencies**  
   ```bash
   pip install pipenv
   pipenv install
   pipenv shell
   ```

3. **Configure environment**  
   Create a `.env` file in the project root:
   ```ini
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

5. **Run migrations & create superuser**  
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Start the development server**  
   ```bash
   python manage.py runserver
   ```

---

## 🚀 Features

- **User Authentication**  
  - Home page doubles as login form  
  - User registration via `SignUpForm`  
  - Logout functionality

- **Record Management (`Record` model)**  
  - Fields:  
    - `first_name`, `last_name`, `email`, `phone`  
    - `address`, `city`, `county`, `postcode`  
    - `created_at` (auto timestamp)  
  - CRUD operations: add, view, update, delete records  

- **Theming**  
  - Light/dark toggle stored in `localStorage`  

- **Django Admin**  
  - Manage `Record` entries in the Django admin interface  

---

## 📂 URL Endpoints

| Path                   | View                  | Description                   |
|------------------------|-----------------------|-------------------------------|
| `/`                    | `home`                | Dashboard & login page        |
| `/register/`           | `register_user`       | User signup                   |
| `/logout/`             | `logout_user`         | Log out                       |
| `/record/<int:pk>/`    | `customer_record`     | Record detail view            |
| `/add_record/`         | `add_record`          | Add a new record              |
| `/update_record/<pk>/` | `update_record`       | Edit an existing record       |
| `/delete_record/<pk>/` | (in `home`)           | Delete a record (confirmation) | 

---

## 📄 License

Open-source for educational and portfolio use.

---

Made with ☕ and curiosity by **Shayan Bagheri (ThinkAboutRek)**