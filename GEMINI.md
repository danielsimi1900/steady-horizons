# Gemini Project Context: mysite-1

## Project Overview
This is a Python web application built using the **Django 6.0.4** framework. The project is currently in its initial setup phase, providing a foundation for a blog or similar web-based system.

- **Primary Technologies:** Python 3.12, Django 6.0, SQLite (database).
- **Core Components:**
    - `blog/`: The main Django project directory containing `manage.py` and the project configuration (`blog/blog/`).
    - `mysite1/`: A local Python virtual environment containing the project's dependencies (Django, Pillow, sqlparse, asgiref).

## Building and Running
All administrative and development commands should be executed from the root directory using the virtual environment.

### Environment Setup
To activate the virtual environment:
```bash
source mysite1/bin/activate
```

### Database & Migrations
To initialize or update the database schema:
```bash
python blog/manage.py migrate
```

### Running the Development Server
To start the Django development server:
```bash
python blog/manage.py runserver
```
The application will be accessible at `http://127.0.0.1:8000/`.

### Administrative Tasks
- **Create Superuser:** `python blog/manage.py createsuperuser`
- **Collect Static Files:** `python blog/manage.py collectstatic`
- **Run Tests:** `python blog/manage.py test`

## Development Conventions
- **Structure:** The Django project is housed in the `blog/` subdirectory. Always use `blog/manage.py` for management commands.
- **Dependencies:** Managed within the `mysite1` virtual environment.
- **Coding Style:** Adheres to standard Django and PEP 8 conventions.
- **Configuration:** Main settings are located in `blog/blog/settings.py`.
