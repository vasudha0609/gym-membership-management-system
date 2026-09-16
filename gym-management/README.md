# Gym Membership Management System

A Flask + PostgreSQL web app for managing gym members, trainers, plans,
memberships, payments, and analytics reports.

## Schema

Matches this design exactly:

- **Members**(member_id, member_name, email, phone, join_date) — plus an
  optional `trainer_id` extension so a member can be assigned to a trainer.
- **Trainers**(trainer_id, trainer_name, specialization, phone)
- **Plans**(plan_id, plan_name, duration, price)
- **Memberships**(membership_id, member_id, plan_id, start_date, end_date)
- **Payments**(payment_id, member_id, amount, payment_date, status)

A `users` table is added separately for app login (admin/staff) — it isn't
part of the gym data model itself.

## Features

- Member management (add/edit/delete/search, view profile with full history)
- Plan management with pricing and duration
- Trainer management with member assignment
- Payment recording with status (Completed / Pending / Failed)
- Membership renewal flow (auto-calculates end date from plan duration)
- Reports page: top 5 plans, most active members, monthly revenue,
  revenue by plan, member spending analysis, trainer performance
- Login-protected (Flask-Login), auto-creates a default admin on first run

## Run locally

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Visit http://localhost:5000 — default login is `admin` / `admin123`
(override with the `ADMIN_USERNAME` / `ADMIN_PASSWORD` env vars).

By default it uses a local SQLite file (`gym.db`) if no `DATABASE_URL` is
set, so you can try it immediately with no database setup.

## Deploy to Render

### Option A — One-click Blueprint (recommended)

1. Push this project to a GitHub repository.
2. In the Render dashboard, click **New > Blueprint**, and point it at your repo.
   Render will read `render.yaml` and automatically:
   - Create a free PostgreSQL database (`gym-management-db`)
   - Create a web service, wire `DATABASE_URL` to that database
   - Generate a random `SECRET_KEY`
3. You'll be prompted to set `ADMIN_PASSWORD` (since it's marked `sync: false`) — set it to something secure.
4. Click **Apply** — Render builds and deploys automatically.

### Option B — Manual setup

1. **Create a PostgreSQL database**: Render dashboard → New → PostgreSQL.
   Copy its **Internal Connection String**.
2. **Create a Web Service**: New → Web Service → connect your repo.
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn run:app`
3. Add environment variables on the web service:
   - `DATABASE_URL` = the connection string from step 1
   - `SECRET_KEY` = any random string
   - `ADMIN_USERNAME` = admin (optional, defaults to `admin`)
   - `ADMIN_PASSWORD` = a secure password
4. Deploy. Tables are created automatically on first boot (`db.create_all()`),
   and a default admin account is seeded if the `users` table is empty.

## Project structure

```
gym-management/
├── app/
│   ├── __init__.py          # App factory, DB init, blueprint registration
│   ├── models.py            # SQLAlchemy models matching the schema
│   ├── routes/
│   │   ├── auth.py          # Login/logout
│   │   ├── dashboard.py     # Home dashboard with stats
│   │   ├── members.py       # Member CRUD + renewal
│   │   ├── plans.py         # Plan CRUD
│   │   ├── payments.py      # Payment recording
│   │   ├── trainers.py      # Trainer CRUD
│   │   └── reports.py       # Analytics/reports
│   ├── templates/           # Jinja2 templates (Bootstrap 5 UI)
│   └── static/css/style.css
├── run.py                   # Entry point
├── requirements.txt
├── Procfile                 # For gunicorn
├── render.yaml              # Render Blueprint definition
└── README.md
```

## Notes

- SQLite is used locally by default; PostgreSQL is used automatically once
  `DATABASE_URL` is set (Render sets this for you via the Blueprint).
- The `gym_membership_queries.sql` file provided separately contains the raw
  SQL (views, stored procedures, reports) matching this exact schema, useful
  if you want to run analysis directly against the Postgres database via
  `psql` or a GUI tool like pgAdmin/DBeaver.
