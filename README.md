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
