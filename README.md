# 🏡 Neighborhood Community Web Application

A web-based platform designed to help neighborhood communities share news and activities in one centralized space. This application aims to improve communication between residents and local committees while building a stronger sense of community.

---

## 📌 Purpose of the Application

This project aims to create a centralized, easy-to-use web application designed specifically for our neighborhood community. The platform will serve as an information hub where all residents can stay informed about local news and upcoming activities. It will also act as a communication channel for the various neighborhood committees.

---

## ✨ Key Features

### 1. Public Community Page
A publicly accessible area that displays:
- News updates from various neighborhood committees
- Announcements about activities hosted by various neighborhood committees
- Public documents presented by the general community board

### 2. Content Management Portal (Admin Area)
A secure area for committee members to:
- Create and publish news posts
- Announce and manage activities
- Upload public accessible files

The idea is to use builtin Django Groups (committees) and Users (committee members).

### 3. Targeted Content
News posts and events are created by committee (e.g., adult, children, sports) to help residents find relevant content.

### 4. Upload Functionality
Committees can upload:
- News and event posters linked to the publications
- Public accessible documents

### 5. Archive Access
An archive view allows users to:
- Browse content organized by **year and month**
- Filtering above content by committee

---

## 🛠️ Tech Stack

This project is built with simplicity, extensibility, and contribution in mind.

| Layer        | Tech Stack                                 |
|--------------|--------------------------------------------|
| Backend      | Django (Python)                            |
| Database     | SQLite for MVP → PostgreSQL                |
| Frontend     | Django Templates                           |
| File Storage | Local file storage for MVP → Cloud storage |
| Deployment   | _To be determined_                         |

### Database Notes
- Start with **SQLite** for simple MVP development.
- Upgrade to **PostgreSQL** when scaling, or for better multi-user support, indexing, and performance.

### File Storage Notes
- MVP uses **local file storage** (Django `MEDIA_ROOT`) for images and PDFs.
- Upgrade to **cloud storage (e.g., AWS S3, Google Cloud Storage)** for scalability, reliability, and remote access to media.

---

## 📦 Getting Started

### Prerequisites
- Python 3.8+ installed
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/neighborhood-community-application.git
   cd neighborhood-community-application
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser for admin access**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Website: http://127.0.0.1:8000/
   - Admin portal: http://127.0.0.1:8000/admin/

### Development Workflow

1. **Create a new branch for your feature**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes and run tests**
   ```bash
   python manage.py test
   ```

3. **Submit a pull request**
   - Push your branch to the repository
   - Create a pull request with a description of your changes

### Security Configuration

Set the following environment variables for a secure deployment:

- `SECRET_KEY` – unique secret for the application.
- `DEBUG` – should be `False` in production.
- `ALLOWED_HOSTS` – comma-separated list of permitted hostnames.
- `SECURE_SSL_REDIRECT` – set to `True` to force HTTPS.
- `SESSION_COOKIE_SECURE` and `CSRF_COOKIE_SECURE` – ensure cookies are sent only over HTTPS.
- `SECURE_HSTS_SECONDS`, `SECURE_HSTS_INCLUDE_SUBDOMAINS`, `SECURE_HSTS_PRELOAD` – control HTTP Strict Transport Security.
- `CSRF_TRUSTED_ORIGINS` – list of origins trusted to post to the application.

### Logging

The application uses Python's built-in logging framework. Logs are written to
both the console and to `logs/app.log`. The verbosity can be controlled with
the `LOG_LEVEL` environment variable (default: `INFO`). The log directory is
created automatically when the project starts.

Logging statements are present in the news, activities, and committees apps to
trace data retrieval and filtering operations, aiding debugging and observability.

### Committees and User Groups
This application uses Django's built-in Groups functionality to manage committees:
- Each committee is represented as a Django Group
- Committee members are assigned to their respective Group
- Content is associated with specific committees for filtering

---

## 📄 License

This project is open source and will be licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

## 🤝 Acknowledgements

This project is built with ❤️ for community engagement and digital inclusion.