# Implementation Plan: Multi-Clinic Follow-up Plans, Gamification, and Rewards

**Branch**: `001-Clinic-Followup` | **Date**: 2026-01-17 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-clinic-followup/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Multi-clinic patient follow-up system with gamification, deterministic scoring, and rewards redemption. Enables Clinic Admins to configure methodologies, follow-up plans, patient journeys, and assign tasks. Patients earn points via task completion with streak bonuses (clinic-validated). Points enable reward redemptions. System enforces tenant isolation, LGPD compliance, and uses internationalized UI labels (pt-BR default).

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: FastAPI (backend API), Streamlit (admin/patient UI), SQLAlchemy (ORM), Pydantic (validation), Alembic (migrations)  
**Storage**: PostgreSQL 15+ (relational data with JSON support for audit logs)  
**Session Management**: Server-side sessions with 24-hour timeout (SESSION_TIMEOUT_SECONDS=86400), stored in PostgreSQL sessions table, single active session per user (new login invalidates previous), logout explicitly revokes session token  
**Testing**: pytest (unit, integration, contract), pytest-cov (≥80% coverage), schemathesis (OpenAPI contract validation), pytest-asyncio (async tests)  
**Target Platform**: Linux server (Docker containerized), web browser clients
**Project Type**: web (backend + frontend)  
**Performance Goals**: 100 concurrent users, <500ms API response p95, real-time analytics for current day + batch for historical  
**Constraints**: LGPD compliance (5-year retention + archival), tenant isolation (no cross-clinic data leakage), no hardcoded UI strings  
**Scale/Scope**: 10 clinics, 1000 patients/clinic, 10k tasks/patient/year, 5-year audit retention

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Law 1: Intent before code
✅ **PASS** - `spec.md` exists and is comprehensive (functional requirements, acceptance criteria, non-goals documented).

### Law 2: Spec ≠ plan
✅ **PASS** - `spec.md` contains no implementation details (focuses on behavior, constraints, roles, requirements). This `plan.md` will contain architecture decisions.

### Law 3: Plan is the technical contract
⏳ **IN PROGRESS** - This plan will document: architecture (backend/frontend split), data model, API contracts, tradeoffs (hybrid analytics, soft delete), and validation approach (pytest + manual acceptance tests).

### Law 4: Tasks are executable
✅ **PASS** - `tasks.md` exists with dependency-ordered checkboxes covering repo setup → data → domain → auth → i18n → admin UI → patient UI → scoring → rewards → analytics → compliance → quality gates.

### Law 5: No silent assumptions
✅ **PASS** - Spec includes resolved Clarifications section (session 2026-01-17) addressing: auth approach, task creation authority, analytics aggregation strategy, validation workflow, point insufficiency handling, deletion/retention strategy, eligibility evaluation, audit log retention, analytics period bounds, same-day completion handling.

### Law 6: Multimodal sources are evidence
✅ **PASS** - Sources documented: `docs/sources/001-clinic-followup/initial-intake.md`, `docs/sources/001-clinic-followup/seed-data.md`.

### Law 7: Copilot must be constrained
✅ **PASS** - `.github/copilot-instructions.md` exists and references this repo's constitution and spec-driven workflow. Will be updated with technology stack after Phase 1.

### Law 8: Validation is part of the feature
✅ **PASS** - Acceptance criteria defined in spec (multi-clinic isolation, setup, tasks, scoring rules, rewards eligibility, redemptions, UI labels, LGPD audit logs). `tasks.md` includes quality gates (end-to-end smoke flow).

### Law 9: PR gating
✅ **PASS** - Requirement acknowledged. Code changes will be accompanied by spec artifacts (`spec.md`, `plan.md`, `tasks.md`).

**VERDICT**: All gates PASS or IN PROGRESS. No violations. Safe to proceed to Phase 0 research.

## Project Structure

### Documentation (this feature)

```text
specs/001-clinic-followup/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
│   └── openapi.yaml     # OpenAPI 3.0 contract
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
# Web application (backend + frontend)
backend/
├── src/
│   ├── models/          # SQLAlchemy ORM models (16 entities)
│   ├── repositories/    # Data access layer (TenantAwareRepository base)
│   ├── services/        # Business logic (ScoringService, RedemptionService, LabelService)
│   └── api/             # FastAPI routers (v1)
│       └── v1/
│           ├── auth.py
│           ├── clinics.py
│           ├── methodologies.py
│           ├── plans.py
│           ├── journey.py
│           ├── patients.py
│           ├── tasks.py
│           ├── scoring.py
│           ├── vendors.py
│           ├── rewards.py
│           ├── redemptions.py
│           └── analytics.py
└── tests/
    ├── unit/            # Business logic tests
    ├── integration/     # API + DB tests
    └── contract/        # OpenAPI validation tests

frontend/
├── src/
│   ├── components/      # Shared Streamlit components
│   ├── pages/
│   │   ├── admin/       # Admin UI pages (clinic setup, patient mgmt, validations)
│   │   └── patient/     # Patient UI pages (tasks, points, rewards)
│   └── services/        # UI service layer (calls backend API)
└── tests/               # UI component tests (optional for v1)

alembic/                 # Database migrations
├── versions/
└── env.py

resources/
└── labels/
    ├── pt-BR.json       # Brazilian Portuguese (default)
    └── en-US.json       # English (future)

scripts/
├── seed_data.py         # Initial data seeding (Contoso + 10 patients)
└── archive_audit_logs.py  # Retention policy background job
```

**Structure Decision**: Web application structure chosen due to FastAPI backend + Streamlit frontend requirement. Backend serves REST API (`/api/v1/*`) with OpenAPI docs, frontend consumes API. Shared session management across both layers. Single Docker Compose deployment for local dev (backend + frontend + PostgreSQL).

## Testing Strategy

### Overview
**Testing is MANDATORY** for this healthcare system handling PHI/PII and subject to LGPD compliance. All tests must pass before code merge.

### Test Organization
```text
backend/tests/
├── unit/                    # Fast isolated tests (services, utilities)
│   ├── test_scoring_service.py       # Base points, streak bonus calculations
│   ├── test_redemption_service.py    # Eligibility, points reserve/refund
│   ├── test_auth_service.py          # Password hashing, session validation
│   ├── test_task_service.py          # Status transitions, validation logic
│   └── test_label_service.py         # i18n interpolation, fallback
├── integration/             # Database + API tests
│   ├── test_api_auth.py              # /login, /logout, /me endpoints
│   ├── test_api_tasks.py             # Task CRUD, status updates
│   ├── test_api_redemptions.py       # Redemption workflow
│   └── test_tenant_isolation.py      # Cross-clinic data leakage prevention
├── contract/                # OpenAPI schema validation
│   └── test_openapi_contract.py      # schemathesis validation
├── e2e/                     # Critical user flows
│   ├── test_task_workflow.py         # Assign → Complete → Validate
│   ├── test_redemption_flow.py       # Request → Approve → Expire/Refund
│   └── test_auth_flow.py             # Login → Session → Logout
└── conftest.py              # Shared fixtures (db, client, test data)
```

### Coverage Requirements
- **Minimum**: 80% overall coverage (pytest-cov)
- **Critical paths**: 100% coverage for:
  - ScoringService (points calculations, streak bonuses)
  - RedemptionService (eligibility, points reserve/refund)
  - AuthService (authentication, session management)
  - TenantAwareRepository (clinic isolation)

### Test Data Strategy
- **Fixtures**: pytest fixtures in conftest.py for:
  - Test database with known schema
  - Test clinics (Clinic A, Clinic B for isolation tests)
  - Test users (admin, patient roles)
  - Test tasks, rewards, redemptions
- **Isolation**: Each test creates isolated data, no shared state
- **Cleanup**: Automatic teardown after each test
- **Factories**: Consider factory_boy for complex object creation

### Contract Testing
- **Tool**: schemathesis (property-based testing for OpenAPI)
- **Scope**: Validate all endpoints against specs/001-clinic-followup/contracts/openapi.yaml
- **Checks**:
  - Response schemas match specification
  - Required fields present
  - Data types correct
  - Enum values valid
  - Status codes per specification

### Security Testing
- **Password Security**: Verify bcrypt hashing, never store plaintext
- **Session Security**: Verify token generation, expiration, revocation
- **RBAC**: Verify admin-only endpoints reject patient requests
- **Tenant Isolation**: Verify clinic A users cannot access clinic B data
- **SQL Injection**: Verify SQLAlchemy parameterized queries (no raw SQL)
- **PHI/PII**: Verify no sensitive data in logs (test log output inspection)

### CI/CD Integration
**Pre-merge gates** (all must pass):
1. Unit tests: `pytest backend/tests/unit/`
2. Integration tests: `pytest backend/tests/integration/`
3. Contract tests: `pytest backend/tests/contract/`
4. E2E tests: `pytest backend/tests/e2e/`
5. Coverage check: `pytest --cov=backend/src --cov-report=term --cov-fail-under=80`
6. Linting: `ruff check backend/` (or equivalent)
7. Type checking: `mypy backend/src/` (optional but recommended)

**No bypassing gates**: For healthcare compliance, test failures block merge.

### Test Execution
```bash
# Run all tests with coverage
pytest --cov=backend/src --cov-report=html --cov-report=term

# Run specific test categories
pytest backend/tests/unit/          # Fast unit tests only
pytest backend/tests/integration/   # Integration tests
pytest backend/tests/contract/      # Contract validation
pytest backend/tests/e2e/           # End-to-end flows

# Run with verbose output
pytest -v

# Run specific test file
pytest backend/tests/unit/test_scoring_service.py -v
```

### Test Development Workflow
1. **TDD approach**: Write tests before implementation
2. **Red-Green-Refactor**: Fail → Pass → Improve
3. **Unit tests first**: Test business logic in isolation
4. **Integration tests**: Verify component interactions
5. **E2E tests last**: Validate complete user flows
6. **Contract tests**: Ensure API matches specification

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**NO VIOLATIONS** - This section is not applicable. All constitution gates passed.

 
 