# Django CRM App

A full-stack Customer Relationship Management (CRM) web application built with Django 6 and PostgreSQL (Supabase), featuring a REST API, CSV export, live search, and a clean Bootstrap 5 UI with dark mode support.

- **User Authentication**
  - Custom **login page** (`/login/`) that handles `?next=` redirects
  - **Registration** with unique-email validation
  - **Logout**
  - Already-logged-in users are auto-redirected away from login/register

- **Protected Views**
  - `@login_required` on all CRUD, export, and dashboard views
  - **Home** (`/`) protected without appending `?next=`
  - Automatic redirect to `/login/` when unauthenticated

- **Customer Records CRUD**
  - **List** all records with search, filter, and pagination (Dashboard)
  - **Detail** view (`/record/<pk>/`)
  - **Add** record (`/add_record/`) with unique email & phone validation
  - **Update** record (`/update_record/<pk>/`)
  - **Delete** record via POST + CSRF token (`/delete_record/<pk>/`)

- **Search & Filter**
  - Live `?q=` search across first name, last name, email, and company
  - Search state is preserved across pagination

- **Pagination**
  - 10 records per page with Bootstrap-styled page controls
  - Page links carry the active search query

- **Export to CSV**
  - Download all records (or current search results) as a `.csv` file
  - Requires authentication; exports all fields including company and notes

- **REST API (Django REST Framework)**
  - Token-based authentication (`POST /api/token/`)
  - `GET /api/records/` — paginated list, supports `?q=` filter
  - `GET /api/records/<pk>/` — single record detail
  - All endpoints return JSON and require a valid auth token

- **Flash Messages**
  - Centralized in **base.html**'s fixed alert container
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
├── D_CRM/                    # Django project settings
│   ├── settings.py           # PostgreSQL, DRF config, env-var-driven SECRET_KEY & DEBUG
│   ├── urls.py               # Root URLconf — web routes + API routes
│   └── wsgi.py, asgi.py
├── CRM_Website/              # Main CRM app
│   ├── admin.py              # RecordAdmin with list display, search, and filters
│   ├── api_views.py          # DRF ListAPIView and RetrieveAPIView for Record
│   ├── serializers.py        # RecordSerializer (ModelSerializer)
│   ├── forms.py              # LoginForm, SignUpForm, AddRecordForm
│   ├── models.py             # Record model (first/last name, email, phone, company, address, notes)
│   ├── tests.py              # (stub for unit tests)
│   ├── urls.py               # App-level URLconf (CRUD + export routes)
│   └── views.py              # Function-based views with @login_required + shared filter helper
├── CRM_Website/templates/
│   ├── base.html             # Global layout, flash messages, dark mode script
│   ├── navbar.html           # Navbar with username display and theme toggle
│   ├── home.html             # Dashboard — search bar, table, pagination, export button
│   ├── login.html            # Login page
│   ├── register.html         # Registration page
│   ├── add_record.html       # Add-record form
│   ├── record.html           # Detail view with company and notes
│   └── update_record.html    # Update-record form
├── manage.py                 # Django CLI
├── .env                      # Environment variables (gitignored)
├── .gitignore
├── Pipfile                   # Pipenv dependencies
└── README.md                 # ← you're here
```

---

## 💻 Technologies & Dependencies

- **Django 6** – High-level Python web framework
- **Django REST Framework** – REST API with token authentication
- **PostgreSQL (Supabase)** – Cloud-hosted relational database
- **psycopg2-binary** – PostgreSQL adapter for Python
- **python-dotenv** – Securely load environment variables
- **Bootstrap 5** – Modern, responsive UI components
- **Git & GitHub** – Version control and hosting

### 📦 Python Packages

```bash
pip install django
pip install djangorestframework
pip install psycopg2-binary
pip install python-dotenv
```

---

## 🔧 Installation & Setup

1. **Clone & enter**
   ```bash
   git clone https://github.com/ThinkAboutRek/Customer-Relationship-Management-App.git
   cd Customer-Relationship-Management-App
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv

   # Windows (PowerShell)
   .venv\Scripts\activate

   # macOS / Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install django djangorestframework psycopg2-binary python-dotenv
   ```

4. **Configure `.env`**
   Create a `.env` file in the project root:
   ```ini
   SECRET_KEY=your-secret-key-here
   DEBUG=True

   DB_NAME=postgres
   DB_USER=postgres.your_project_ref
   DB_PASSWORD=your_supabase_password
   DB_HOST=aws-0-eu-central-1.pooler.supabase.com
   DB_PORT=5432
   ```
   Get your Supabase connection details from your project dashboard → **Connect** → **Session pooler**.

5. **Apply migrations & create superuser**
   ```bash
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
2. **Log in** at `/login/` (redirects back to intended page via `?next=`)
3. **Dashboard** `/` — list all records with search and pagination
4. **Search** using the search bar — filters by name, email, or company
5. **View** a record at `/record/<pk>/`
6. **Add** at `/add_record/`
7. **Edit** at `/update_record/<pk>/`
8. **Delete** at `/delete_record/<pk>/` (POST only, CSRF protected)
9. **Export** all or filtered records as CSV via the **Export CSV** button

---

## 🔌 REST API

All API endpoints require a token. First obtain one:

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

Response:
```json
{ "token": "abc123yourtokenhere" }
```

Then use the token in subsequent requests:

```bash
# List all records
curl http://127.0.0.1:8000/api/records/ \
  -H "Authorization: Token abc123yourtokenhere"

# Filter records
curl "http://127.0.0.1:8000/api/records/?q=john" \
  -H "Authorization: Token abc123yourtokenhere"

# Get a single record
curl http://127.0.0.1:8000/api/records/1/ \
  -H "Authorization: Token abc123yourtokenhere"
```

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/token/` | Obtain auth token |
| `GET` | `/api/records/` | List all records (supports `?q=` filter) |
| `GET` | `/api/records/<pk>/` | Retrieve a single record |

---

## 🔧 Customizations

- **Shared filter helper** `_filter_records()` in `views.py` — used by both the dashboard and the CSV export to keep filter logic DRY
- **Unique validations** in `AddRecordForm.clean_email()` & `clean_phone()` — enforces no duplicate contact details
- **Custom `login_user`** handles `?next=`, blocks already-authenticated users, and uses `form.get_user()`
- **Global flashes** in `base.html` (no duplicates across templates)
- **Admin panel** configured with `list_display`, `search_fields`, `list_filter`, and `readonly_fields` on `RecordAdmin`

---

## 📄 License

Open-source for educational and portfolio use.

---

Made with ☕ and curiosity by **Shayan Bagheri (ThinkAboutRek)**
