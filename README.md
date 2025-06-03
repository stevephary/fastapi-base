# 🚀 FASTAPI STARTER TEMPLATE

A production-ready FastAPI template for new projects, featuring built-in user authentication and email verification.

---

## 🛠️ Technology Stack & Features

### ⚙️ Core Technologies

- 🧰 **SQLModel** – ORM for interacting with SQL databases using Python  
- 🔍 **Pydantic** – For data validation and settings management, integrated with FastAPI  
- 💾 **PostgreSQL** – Reliable and powerful relational database system 
- ⚡ **uv** – A CLI tool to manage virtual environments and dependencies  
- 🗃️ **Alembic** – Database migration tool for SQLAlchemy and SQLModel   

### 🔐 Authentication & Security

- 🔒 Secure password hashing using `passlib`  
- 🔑 JWT (JSON Web Token)-based authentication  
- 📫 Email-based password recovery  
- ✅ Email verification on user registration  

### 🧱 Architecture & Deployment

- 📦 Modular and scalable project structure  
- 🐳 Fully Dockerized – comes with a ready-to-use `docker-compose` setup  

---

## 📦 How to Use

This repository is a **GitHub template**. To start a new project:

1. Click the **"Use this template"** button on GitHub  
2. Create your new repository  
3. Clone your newly created repository:

```bash
git clone https://github.com/your-username/your-new-repo.git
cd your-new-repo
````

---

## 📝 Before You Start

* Open `pyproject.toml` and update the project name:

  ```toml
  [project]
  name = "your-project-name"
  ```

* In `docker-compose.yml`, update the service/container names to your preferred names.
  Make sure to use those names consistently in related Docker commands.

---

## 🔧 Local Development Setup

```bash
# Create a virtual environment
uv venv

# Activate the environment
source .venv/bin/activate

# Sync and install dependencies
uv sync

# Run database migrations
alembic head

# Start the FastAPI development server
uvicorn app.main:app --reload
```

---

## 🐳 Docker Setup

```bash
# Build the containers
docker compose build

# Start the database container (replace dbcontainername with your DB service name)
docker compose up -d dbcontainername

# Run Alembic migrations (replace containername with your app container name)
docker compose run containername --rm alembic head

# Start all services
docker compose up
```

---

✅ Your FastAPI app is now ready with modular structure, Docker support, authentication, and email verification.

```
```
