# FastAPI Expense Tracker

A production-oriented REST API for managing personal expenses, built with **FastAPI, PostgreSQL, SQLAlchemy, Alembic, JWT authentication, Pytest, and Docker**.

The project is being developed incrementally with the goal of progressing from a containerized backend to CI/CD, cloud deployment, and additional production-grade features.

---

## Table of Contents

* [Overview](#overview)
* [Tech Stack](#tech-stack)
* [Current Features](#current-features)
* [Project Structure](#project-structure)
* [Prerequisites](#prerequisites)
* [Getting Started](#getting-started)

  * [1. Clone the Repository](#1-clone-the-repository)
  * [2. Create the Environment File](#2-create-the-environment-file)
  * [3. PostgreSQL Setup](#3-postgresql-setup)
  * [4. Run Database Migrations](#4-run-database-migrations)
  * [5. Start the Application](#5-start-the-application)
* [Docker Setup](#docker-setup)
* [Database Migrations](#database-migrations)
* [API Documentation](#api-documentation)
* [Authentication](#authentication)
* [Testing](#testing)
* [Environment Variables](#environment-variables)
* [Development vs Docker Database](#development-vs-docker-database)
* [Useful Commands](#useful-commands)
* [Current Production Hardening](#current-production-hardening)
* [Future Roadmap](#future-roadmap)

---

# Overview

The **FastAPI Expense Tracker** is a REST API designed to provide authenticated users with the ability to manage and track their expenses.

The application uses:

* FastAPI for the API layer
* PostgreSQL for persistent data storage
* SQLAlchemy for database interaction
* Alembic for database schema migrations
* JWT for authentication
* Pydantic for request/response validation and configuration
* Pytest for automated testing
* Docker and Docker Compose for containerized development

The project is intentionally being built in stages, with production hardening, CI/CD, cloud deployment, and advanced backend features planned for later stages.

---

# Tech Stack

| Technology        | Purpose                                 |
| ----------------- | --------------------------------------- |
| Python 3.11       | Programming language                    |
| FastAPI           | REST API framework                      |
| PostgreSQL 15     | Relational database                     |
| SQLAlchemy 2      | ORM / database interaction              |
| Alembic           | Database migrations                     |
| Pydantic v2       | Data validation                         |
| Pydantic Settings | Environment-based configuration         |
| JWT               | Authentication                          |
| Passlib / bcrypt  | Password hashing                        |
| Pytest            | Automated testing                       |
| Docker            | Containerization                        |
| Docker Compose    | Multi-container development environment |
| Uvicorn           | ASGI server                             |

---

# Current Features

## Authentication

* User signup
* User login
* Password hashing
* JWT access tokens
* Bearer token authentication
* Authenticated user retrieval
* Protected API endpoints

## Expense Management

* Create expenses
* Retrieve expenses
* Pagination
* Filtering
* Expense categories
* Database indexes for relevant queries
* Authenticated access to expense endpoints

## Database

* PostgreSQL
* SQLAlchemy ORM
* Alembic migrations
* Foreign keys and constraints
* Database indexes
* Separate development and Docker database environments

## API

* Versioned API routes
* Health check endpoint
* Automatic OpenAPI documentation
* Swagger UI
* Pydantic request/response schemas

## Testing

* Pytest
* Authentication tests
* Expense API tests
* Test database
* Dependency overrides for database sessions

## Docker

* Dockerized FastAPI application
* Dockerized PostgreSQL
* Docker Compose
* PostgreSQL health check
* FastAPI health check
* Automatic Alembic migration execution in the current Docker development setup

---

# Project Structure

The project currently follows a structure similar to:

```text
fastapi-expense-tracker/
│
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       └── router.py
│   │
│   ├── core/
│   │   └── config.py
│   │
│   ├── db/
│   │   ├── models/
│   │   ├── base.py
│   │   └── session.py
│   │
│   ├── schemas/
│   ├── services/
│   ├── dependencies.py
│   └── main.py
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_expenses.py
│
├── .env
├── .env.docker
├── .env.example
├── .gitignore
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

> The exact structure may evolve as the project progresses.

---

# Prerequisites

To run the project locally, you should have:

* Python 3.11+
* PostgreSQL 15+
* Git
* pip
* A PostgreSQL client such as pgAdmin (optional)

For Docker-based development:

* Docker Desktop
* Docker Compose

---

# Getting Started

There are currently two ways to run the application:

1. **Local development with PostgreSQL installed locally**
2. **Docker-based development**

Docker is the recommended approach for reproducing the complete application environment.

---

## 1. Clone the Repository

Clone the repository:

```bash
git clone <repository-url>
```

Move into the project directory:

```bash
cd fastapi-expense-tracker
```

---

## 2. Create the Environment File

The repository contains:

```text
.env.example
```

This file is a safe template and does not contain real secrets.

Create your local `.env` from the template.

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

Then open `.env` and provide your own values.

Example:

```env
DEBUG=False

DATABASE_URL=postgresql+psycopg2://postgres:your_password@localhost:5432/expense_db

SECRET_KEY=replace_with_a_secure_random_secret

POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=expense_db
```

### Important

Never commit:

```text
.env
.env.docker
```

These files contain environment-specific configuration and secrets.

The repository intentionally tracks:

```text
.env.example
```

instead.

---

# 3. PostgreSQL Setup

## Local PostgreSQL

If you are running PostgreSQL directly on your machine, create a database named:

```text
expense_db
```

For example, using pgAdmin:

```text
PostgreSQL Server
└── Databases
    └── expense_db
```

The database itself must exist before Alembic can connect to it.

Alembic is responsible for managing the **database schema**, not normally creating the PostgreSQL database itself.

---

# 4. Run Database Migrations

Once PostgreSQL is running and `DATABASE_URL` is configured:

```bash
alembic upgrade head
```

Alembic will apply all migrations that have not yet been applied.

These migrations can create and modify:

* Tables
* Columns
* Foreign keys
* Constraints
* Indexes
* Other database schema objects defined by the migrations

Alembic also maintains its migration state using:

```text
alembic_version
```

---

# 5. Start the Application

For local development:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

---

# Docker Setup

Docker provides a reproducible environment containing:

```text
FastAPI
   │
   ▼
FastAPI Container
   │
   ▼
PostgreSQL Container
```

The current Docker development setup uses Docker Compose.

---

## Start the Application with Docker

Make sure Docker Desktop is running.

Then:

```bash
docker compose up --build
```

Docker Compose starts:

1. PostgreSQL
2. PostgreSQL health check
3. FastAPI container
4. Database connectivity check
5. Alembic migrations
6. FastAPI/Uvicorn

The API should then be available at:

```text
http://localhost:8000
```

---

## Stop the Application

```bash
docker compose down
```

This stops and removes the containers while preserving the named PostgreSQL volume.

---

## Stop Containers and Remove the Database Volume

**Warning:** this removes the Docker PostgreSQL data stored in the volume.

```bash
docker compose down -v
```

This should only be used when you intentionally want to reset the Docker database.

---

# Docker Database

The Docker Compose PostgreSQL service uses:

```yaml
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB
```

When the PostgreSQL container initializes a new data directory, the PostgreSQL Docker image uses these values to initialize the database.

Therefore, with the Docker setup:

```text
docker compose up
        │
        ▼
PostgreSQL container
        │
        ▼
expense_db created
        │
        ▼
Alembic
        │
        ▼
Tables / indexes / schema
```

This differs from running PostgreSQL directly on your machine, where the database must generally be created before Alembic connects to it.

---

# Database Migrations

Alembic is the project's database schema migration tool.

## Apply migrations

```bash
alembic upgrade head
```

## Create a new migration

After making a schema/model change:

```bash
alembic revision --autogenerate -m "describe the change"
```

Review the generated migration before applying it.

Then:

```bash
alembic upgrade head
```

## Check current migration

```bash
alembic current
```

## View migration history

```bash
alembic history
```

Migrations are committed to Git because they are part of the application's source code and database schema history.

---

# API Documentation

Once the application is running, FastAPI automatically provides interactive API documentation.

## Swagger UI

```text
http://localhost:8000/docs
```

## ReDoc

```text
http://localhost:8000/redoc
```

## OpenAPI schema

```text
http://localhost:8000/openapi.json
```

---

# Authentication

The API uses JWT-based authentication.

The general flow is:

```text
User
 │
 ├── Signup
 │
 └── Login
       │
       ▼
   JWT Access Token
       │
       ▼
Authorization: Bearer <token>
       │
       ▼
Protected API endpoint
```

Protected endpoints require a valid Bearer token.

Swagger UI can be used to test authentication through its **Authorize** functionality.

---

# Health Check

The application exposes a health endpoint:

```text
GET /health
```

When the application is running:

```text
http://localhost:8000/health
```

This endpoint is also used by the current Docker health check.

---

# Testing

The project uses Pytest.

Run the complete test suite:

```bash
pytest -v
```

Tests use a separate test database and database-session overrides so that application tests do not operate against the normal development database.

The test suite currently covers authentication and expense functionality.

---

# Environment Variables

The application uses **Pydantic Settings** for environment-based configuration.

The primary application configuration currently includes:

| Variable            | Purpose                            |
| ------------------- | ---------------------------------- |
| `DATABASE_URL`      | SQLAlchemy database connection URL |
| `SECRET_KEY`        | JWT signing secret                 |
| `DEBUG`             | Application debug configuration    |
| `POSTGRES_USER`     | PostgreSQL username                |
| `POSTGRES_PASSWORD` | PostgreSQL password                |
| `POSTGRES_DB`       | PostgreSQL database name           |

The application configuration is defined in:

```text
app/core/config.py
```

---

# Development vs Docker Database

The application uses different database hostnames depending on where FastAPI is running.

## Running FastAPI directly on the host

The database URL uses:

```text
localhost
```

Example:

```env
DATABASE_URL=postgresql+psycopg2://postgres:your_password@localhost:5432/expense_db
```

## Running FastAPI inside Docker

The FastAPI container communicates with PostgreSQL using the Docker Compose service name:

```text
db
```

Example:

```env
DATABASE_URL=postgresql+psycopg2://postgres:your_password@db:5432/expense_db
```

Inside a container, `localhost` refers to the container itself, not the PostgreSQL container.

Docker Compose provides service-to-service DNS resolution, allowing the FastAPI container to reach PostgreSQL using:

```text
db:5432
```

---

# Git and Environment Files

The repository intentionally tracks:

```text
.env.example
```

but ignores:

```text
.env
.env.docker
```

The purpose of `.env.example` is to document the environment variables required to run the project without exposing real credentials.

A new developer can:

```text
Clone repository
      │
      ▼
Copy .env.example → .env
      │
      ▼
Add their own local values
      │
      ▼
Run application
```

Real secrets should never be committed to the repository.

---

# Useful Commands

## Local FastAPI server

```bash
uvicorn app.main:app --reload
```

## Run tests

```bash
pytest -v
```

## Apply migrations

```bash
alembic upgrade head
```

## Create migration

```bash
alembic revision --autogenerate -m "describe the change"
```

## Start Docker

```bash
docker compose up
```

## Rebuild Docker image

```bash
docker compose up --build
```

## Stop Docker

```bash
docker compose down
```

## Reset Docker database

```bash
docker compose down -v
```

## View running containers

```bash
docker compose ps
```

## View application logs

```bash
docker compose logs app
```

## View PostgreSQL logs

```bash
docker compose logs db
```

---

# Current Production Hardening

The project is currently undergoing a dedicated **Production Hardening** phase.

Already established:

* Environment-based application configuration
* Pydantic Settings
* Secrets moved out of the Compose file
* `.env` excluded from Git
* `.env.docker` excluded from Git
* `.env.example` provided as a safe configuration template
* Dockerized PostgreSQL
* Docker health checks
* Alembic migrations working inside Docker

The remaining production-hardening work includes:

* Production-ready Dockerfile
* Gunicorn with Uvicorn workers
* Separation of development and production Compose configurations
* Removal of unnecessary development-only Docker configuration
* Production configuration cleanup
* Removal of application-level `Base.metadata.create_all()` in favor of Alembic-only schema management
* Preparation for an NGINX/reverse-proxy architecture

---

# Future Roadmap

## Phase 1 — Core Backend + Docker

**Completed**

* FastAPI backend
* PostgreSQL
* SQLAlchemy
* Alembic
* JWT authentication
* Expense APIs
* Automated tests
* Docker
* Docker Compose
* Dockerized PostgreSQL

---

## Phase 2 — Production Hardening

**In progress**

* Environment-based configuration
* Secret management
* Production Dockerfile
* Gunicorn + Uvicorn workers
* Development/production Compose separation
* Production configuration cleanup
* NGINX/reverse-proxy preparation

---

## Phase 3 — CI/CD

Planned:

* GitHub repository workflow
* GitHub Actions
* Automated tests
* Docker image builds
* Container image registry
* Automated deployment
* CI/CD secrets management

---

## Phase 4 — Cloud Deployment

Planned:

* Cloud server deployment
* Production PostgreSQL
* NGINX reverse proxy
* Domain configuration
* HTTPS/SSL
* Production environment variables/secrets
* Database migrations during deployment
* Application restart/update strategy

---

## Phase 5 — Advanced Features

Planned:

* Redis
* Caching
* Background jobs
* Rate limiting
* Refresh tokens
* Role-based access control
* Logging
* Monitoring
* Additional production-grade FastAPI features

---

## Phase 6+ — Portfolio and Scaling

Potential improvements:

* Cloud infrastructure improvements
* Observability
* Horizontal scaling
* Architecture improvements
* Performance optimization
* Frontend application

---

# Project Status

**Current stage: Production Hardening**

The core backend, authentication, expense APIs, testing, database migrations, and Docker environment are complete.

The next major focus is making the Docker and configuration setup suitable for a production deployment before moving on to CI/CD.
