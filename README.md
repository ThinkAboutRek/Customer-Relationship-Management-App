This is a secure Customer Relationship Management (CRM) web application built with **Django**, **MySQL**, **Pipenv**, and **Bootstrap**. The project demonstrates a full-stack setup including database connectivity, project structure best practices, and GitHub version control.

---

## 📁 Project Structure

```
CRM APP/
├── D_CRM/              # Django project (settings, URLs, etc.)
│   ├── settings.py
│   └── ...
├── CRM_Website/        # Main app for CRM features (models, views, etc.)
├── manage.py           # Django entry point
├── .env                # Secure DB config (ignored in Git)
├── .gitignore          # Prevents pushing sensitive files
├── Pipfile             # Pipenv environment
├── Pipfile.lock
├── mydb.py             # Script to create MySQL database (using .env)
```

---

## 💻 Technologies Used

- **Django** – Backend web framework
- **MySQL** – Relational database
- **Pipenv** – Virtual environment & dependency management
- **python-dotenv** – For secure environment variables
- **Bootstrap 5** – For front-end styling (to be added)
- **Git + GitHub** – Version control

---

## 🔐 Environment Variables (.env)

The `.env` file holds database configuration and is **excluded from Git**. Example format:

```
MYSQL_NAME=CRM_DB
MYSQL_USER=root
MYSQL_PASSWORD=yourpassword
MYSQL_HOST=localhost
MYSQL_PORT=3306
```

---

## 🛠️ Setup Instructions

1. **Clone the repo**:
```bash
git clone https://github.com/ThinkAboutRek/ThinkAboutRek-Customer-Relationship-Management-App.git
```

2. **Install dependencies**:
```bash
pip install pipenv
pipenv install
```

3. **Activate shell**:
```bash
pipenv shell
```

4. **Create the database (optional)**:
```bash
python mydb.py
```

5. **Run migrations**:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser**:
```bash
python manage.py createsuperuser
```

7. **Start the server**:
```bash
python manage.py runserver
```

---

## 📄 License

This project is open for educational and portfolio use.

---

Made with ☕ and curiosity by **ThinkAboutRek (Shayan Bagheri)**