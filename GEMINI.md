# TaskFlow API - Gemini Context

## Project Overview

This project is the backend API for **TaskFlow**, a modern task management application. It is built with Python and the FastAPI framework, designed to serve a corresponding Angular 19 frontend. The API provides comprehensive functionality for managing workspaces, projects, tasks, users, and authentication.

### Core Technologies

- **Backend:** Python 3.11+, FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Data Validation:** Pydantic
- **Authentication:** JWT with OAuth2 Password Flow (using `python-jose` and `passlib`)
- **Dependency Management:** Poetry
- **Database Migrations:** Alembic
- **Containerization:** Docker and Docker Compose are used to run the PostgreSQL database.

### Architecture

The application follows a modular, layered architecture:

- **`app/main.py`**: The main entry point, responsible for FastAPI app initialization, middleware configuration (CORS, Gzip, Rate Limiting), and custom exception handlers.
- **`app/api/`**: Contains the API routing logic, separating endpoints into logical groups.
- **`app/services/`**: Holds the core business logic, acting as an intermediary between the API routes and the database layer.
- **`app/db/`**: Manages all database interactions, including session management, model definitions (using SQLAlchemy's Declarative Base), and mixins.
- **`app/schemas/`**: Defines the Pydantic models used for request/response validation and serialization.
- **`app/core/`**: Contains application-wide configuration (`config.py`), logging setup, and security utilities.

## Building and Running

There are two primary ways to run this project for development.

### Option 1: Local Development with Dockerized Database (Recommended)

This method runs the Python application directly on your host machine while the PostgreSQL database runs in a Docker container.

**Prerequisites:**
- Python 3.11+
- Poetry
- Docker

**Steps:**

1.  **Start the database:**
    ```bash
    docker-compose up -d
    ```

2.  **Install Python dependencies:**
    ```bash
    poetry install
    ```

3.  **Activate the virtual environment:**
    ```bash
    poetry shell
    ```

4.  **Set up environment variables:** Copy the example `.env` file. The default values are configured to connect to the Dockerized database.
    ```bash
    cp .env.example .env
    ```

5.  **Apply database migrations:**
    ```bash
    alembic upgrade head
    ```

6.  **Run the FastAPI server:**
    ```bash
    uvicorn app.main:app --reload
    ```

7.  **Access the API:**
    - **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
    - **Redoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Option 2: Fully Local Development

This method requires a local PostgreSQL server running on your host machine.

**Steps:**
1.  Ensure your local PostgreSQL server is running.
2.  Follow steps 2-6 from Option 1.
3.  You must update the `.env` file with the correct connection string for your local PostgreSQL instance.

## Development Conventions

- **Database Migrations:** Changes to SQLAlchemy models must be accompanied by a new migration file generated using `alembic revision --autogenerate -m "Your migration message"` and applied with `alembic upgrade head`.
- **Code Style & Linting:** The project uses **Ruff** for linting and code formatting. It is recommended to run `ruff check .` and `ruff format .` before committing changes.
- **Testing:** The project is set up for testing with `pytest`. Tests are located in the `/tests` directory.
- **Configuration:** All configuration is managed via environment variables loaded into the Pydantic `Settings` object in `app/core/config.py`. Do not use hardcoded credentials or settings.
- **Modularity:** Business logic should be placed in service functions, keeping API routes thin and focused on handling HTTP requests and responses.
