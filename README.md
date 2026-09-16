# IronCore Gym — Membership Management System

A full-stack web application for managing gym operations — members, trainers, membership plans, payments, and business analytics — built with Flask and PostgreSQL.

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/flask-3.0-black)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## Overview

Small gyms often rely on registers, spreadsheets, or messaging apps to track members, payments, and renewals — a process that's error-prone and offers no real visibility into the business. This project replaces that with a centralized, web-based admin system that manages the full membership lifecycle and generates business reports automatically.

## Features

- **Member Management** — add, edit, search members; view a full profile with membership and payment history
- **Trainer Management** — maintain trainer records with specialization and contact details
- **Plan Management** — configurable membership plans (name, duration, price)
- **Payment Tracking** — record payments with status (`Completed` / `Pending` / `Failed`)
- **Membership Renewal** — selecting a plan automatically calculates start and end dates
- **Dashboard** — real-time stats: total/active members, monthly and all-time revenue, memberships expiring soon
- **Reports & Analytics** — top plans, most active members, monthly revenue trends, revenue by plan, member spending analysis, trainer performance
- **Authentication** — session-based admin login via Flask-Login, hashed passwords (no plaintext storage)

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| ORM / Database | SQLAlchemy, PostgreSQL (production) / SQLite (local) |
| Frontend | HTML, Bootstrap 5, Jinja2 |
| Auth | Flask-Login, Werkzeug password hashing |
| Deployment | Render (Web Service + Managed PostgreSQL) |

## Database Schema

Trainers ──┐
│ (optional assignment)
▼
Members ──────────┐
│ │
▼ ▼
Memberships Payments
│
▼
Plans


**Tables:**
- `members` — member_id, member_name, email, phone, join_date, trainer_id (FK)
- `trainers` — trainer_id, trainer_name, specialization, phone
- `plans` — plan_id, plan_name, duration, price
- `memberships` — membership_id, member_id (FK), plan_id (FK), start_date, end_date
- `payments` — payment_id, member_id (FK), amount, payment_date, status

## Project Structure

gym-management/
├── app/
│ ├── init.py # App factory, DB init, blueprint registration
│ ├── models.py # SQLAlchemy models
│ ├── routes/
│ │ ├── auth.py # Login / logout
│ │ ├── dashboard.py # Home dashboard with live stats
│ │ ├── members.py # Member CRUD + renewal
│ │ ├── plans.py # Plan CRUD
│ │ ├── payments.py # Payment recording
│ │ ├── trainers.py # Trainer CRUD
│ │ └── reports.py # Analytics & reports
│ ├── templates/ # Jinja2 templates
│ └── static/css/style.css # Styling
├── run.py # Application entry point
├── requirements.txt
├── Procfile # For gunicorn (Render)
├── render.yaml # Render Blueprint config
└── README.md


## Getting Started

### Prerequisites
- Python 3.10 or higher
- pip

### Installation

```bash
git clone https://github.com/<your-username>/gym-management.git
cd gym-management

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Run locally

```bash
python run.py
```

Visit `http://localhost:5000`. The app uses SQLite by default when no `DATABASE_URL` is set, so no database setup is required to try it out.

**Default login:** `admin` / `admin123` — override via `ADMIN_USERNAME` / `ADMIN_PASSWORD` environment variables, and change it after first login.

## Deployment

This project is deployment-ready for [Render](https://render.com) with PostgreSQL, via the included `render.yaml` Blueprint.

1. Push this repository to GitHub.
2. In Render, select **New → Blueprint** and connect the repo.
3. Render provisions a web service and a managed PostgreSQL database automatically, and links them via the `DATABASE_URL` environment variable.
4. Set `ADMIN_PASSWORD` when prompted, then deploy.

See inline comments in `render.yaml` for configuration details.

## Reports

The Reports module runs live SQL aggregation queries (joins, `SUM`, `COUNT`, `GROUP BY`) against the database to surface:

- Top 5 most popular plans
- Most active members (by payment count)
- Monthly revenue report
- Revenue generated per plan
- Full member spending ranking
- Trainer performance (members handled)

## Roadmap

- [ ] Separate login portals for trainers and members
- [ ] Attendance / check-in tracking
- [ ] Automated SMS/email renewal reminders
- [ ] Online payment gateway integration



## Author

Built as a gym operations management project — feel free to fork and adapt for your own use case.
