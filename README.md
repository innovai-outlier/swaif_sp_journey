# SWAIF Clinic Follow-up System

Multi-clinic patient follow-up system with gamification, scoring, and rewards.

## Setup Complete ✓

The project has been initialized with:

- **Backend**: FastAPI + SQLAlchemy + Alembic
- **Frontend**: Streamlit (admin + patient UIs)
- **Database**: PostgreSQL 15 (running in Docker)
- **Authentication**: Email/password with bcrypt
- **Testing**: pytest + pytest-cov + schemathesis

## Current Status

**Completed** (19/163 tasks):
- ✅ Phase 1: Project Structure & Configuration
- ✅ Phase 2: Foundation (Base models, repositories, utilities)
- ✅ Phase 3: User Story 1 - Models (Clinic, User, ClinicMembership)
- ✅ Project setup verification (.gitignore, .dockerignore)

## Quick Start

### 1. Database

PostgreSQL is already running in Docker:

```bash
docker ps | findstr swaif
```

### 2. Python Environment

Virtual environment is set up with all dependencies:

```bash
# Activate venv
.\venv\Scripts\activate

# Verify installation
python -c "import fastapi, sqlalchemy; print('All good!')"
```

### 3. Environment Configuration

Edit `.env` file and update SECRET_KEY:

```bash
# Generate a secret key
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Database Migrations

Create and run migrations:

```bash
# Create initial migration
alembic revision --autogenerate -m "Initial schema"

# Apply migrations
alembic upgrade head
```

### 5. Run Application

```bash
# Start FastAPI backend
python -m uvicorn backend.src.main:app --reload --host 0.0.0.0 --port 8000
```

API Documentation: http://localhost:8000/api/docs

## Next Steps

Continue implementation according to [tasks.md](specs/001-clinic-followup/tasks.md):

1. **Complete Phase 2** - Create initial database migration (T013)
2. **Phase 3 Remaining** - Repositories, services, API routers, UI pages (T017-T033)
3. **Phase 4+** - Additional user stories following the spec

## Project Structure

```
swaif_sp_journey/
├── backend/
│   ├── src/
│   │   ├── models/          # SQLAlchemy models
│   │   ├── repositories/    # Data access layer
│   │   ├── services/        # Business logic
│   │   ├── api/v1/          # FastAPI routers
│   │   ├── schemas/         # Pydantic models
│   │   ├── config/          # Configuration
│   │   ├── middleware/      # Middleware
│   │   ├── dependencies/    # FastAPI dependencies
│   │   └── utils/           # Utilities
│   └── tests/               # Tests
├── frontend/
│   └── src/                 # Streamlit UI
├── alembic/                 # Database migrations
├── scripts/                 # Utility scripts
├── specs/                   # Feature specifications
└── docs/                    # Documentation

```

## Documentation

- **Specification**: [specs/001-clinic-followup/spec.md](specs/001-clinic-followup/spec.md)
- **Implementation Plan**: [specs/001-clinic-followup/plan.md](specs/001-clinic-followup/plan.md)
- **Data Model**: [specs/001-clinic-followup/data-model.md](specs/001-clinic-followup/data-model.md)
- **Task Checklist**: [specs/001-clinic-followup/tasks.md](specs/001-clinic-followup/tasks.md)
- **Quickstart**: [specs/001-clinic-followup/quickstart.md](specs/001-clinic-followup/quickstart.md)

## Tech Stack

- **Language**: Python 3.13
- **Web Framework**: FastAPI 0.109.0
- **UI Framework**: Streamlit 1.30.0
- **Database**: PostgreSQL 15+ with SQLAlchemy 2.0.45
- **Migrations**: Alembic 1.13.1
- **Authentication**: passlib with bcrypt
- **Testing**: pytest, pytest-cov, schemathesis
- **Validation**: Pydantic 2.12.5

## Contributing

Follow the Spec Kit SDD workflow:

1. Read `.specify/memory/constitution.md`
2. For the active feature, read specs in order: `spec.md` → `plan.md` → `tasks.md`
3. Implement only what is in `tasks.md`
4. Mark tasks as complete (`[X]`) in `tasks.md` as you go

## License

See [LICENSE](LICENSE) file for details.
