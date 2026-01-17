# Quickstart: Multi-Clinic Follow-up System

**Feature**: 001-clinic-followup  
**Date**: 2026-01-17  
**Target Audience**: Developers setting up local development environment

## Prerequisites

- **Python**: 3.11 or higher
- **PostgreSQL**: 15 or higher
- **Docker & Docker Compose**: (optional, recommended for local DB)
- **Git**: For cloning the repository

---

## Quick Setup (5 minutes)

### 1. Clone Repository

```bash
git clone https://github.com/innovai-outlier/swaif_sp_journey.git
cd swaif_sp_journey
git checkout 001-Clinic-Followup
```

### 2. Start PostgreSQL (Docker)

```bash
docker-compose up -d postgres
```

Or use local PostgreSQL and create database:
```sql
CREATE DATABASE swaif_clinic_followup;
```

### 3. Configure Environment

```bash
cp .env.example .env
```

Edit `.env`:
```bash
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/swaif_clinic_followup

# App
APP_LOCALE=pt-BR
SECRET_KEY=your-secret-key-here  # Generate with: openssl rand -hex 32
SESSION_TIMEOUT_SECONDS=86400  # 24 hours

# Logging
LOG_LEVEL=INFO
```

### 4. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 5. Run Migrations & Seed Data

```bash
# Apply database migrations
alembic upgrade head

# Seed initial data (Contoso clinic + sample patients)
python scripts/seed_data.py
```

### 6. Start Application

```bash
# Start FastAPI backend + Streamlit UI
python -m uvicorn app.main:app --reload --port 8000
```

In a separate terminal:
```bash
# Start Streamlit admin UI
streamlit run app/ui/admin_app.py --server.port 8501

# Start Streamlit patient UI
streamlit run app/ui/patient_app.py --server.port 8502
```

### 7. Access Application

- **API Docs**: http://localhost:8000/api/docs
- **Admin UI**: http://localhost:8501
- **Patient UI**: http://localhost:8502

**Seeded Credentials**:
- Admin: `admin@contoso.com` / `admin123`
- Patient: `patient1@contoso.com` / `patient123`

---

## Project Structure

```
swaif_sp_journey/
├── app/
│   ├── main.py                    # FastAPI app entry point
│   ├── models/                    # SQLAlchemy ORM models
│   │   ├── clinic.py
│   │   ├── user.py
│   │   ├── patient.py
│   │   ├── methodology.py
│   │   ├── task.py
│   │   ├── reward.py
│   │   └── ...
│   ├── repositories/              # Data access layer (tenant-aware)
│   │   ├── base.py                # TenantAwareRepository
│   │   └── ...
│   ├── services/                  # Business logic
│   │   ├── auth_service.py
│   │   ├── scoring_service.py
│   │   ├── redemption_service.py
│   │   └── label_service.py       # i18n
│   ├── api/                       # FastAPI routers
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── clinics.py
│   │       ├── tasks.py
│   │       ├── rewards.py
│   │       └── ...
│   ├── ui/                        # Streamlit UIs
│   │   ├── admin_app.py
│   │   └── patient_app.py
│   └── schemas/                   # Pydantic request/response models
│       └── ...
├── alembic/                       # Database migrations
│   ├── versions/
│   └── env.py
├── resources/
│   └── labels/
│       ├── pt-BR.json             # Brazilian Portuguese labels
│       └── en-US.json             # English labels (future)
├── scripts/
│   ├── seed_data.py               # Initial data seeding
│   └── archive_audit_logs.py     # Retention policy job
├── tests/
│   ├── unit/                      # Unit tests (business logic)
│   ├── integration/               # Integration tests (API + DB)
│   └── contract/                  # OpenAPI contract tests
├── specs/
│   └── 001-clinic-followup/
│       ├── spec.md                # Feature specification
│       ├── plan.md                # Implementation plan
│       ├── research.md            # Technical research
│       ├── data-model.md          # Data model documentation
│       ├── tasks.md               # Implementation checklist
│       └── contracts/
│           └── openapi.yaml       # OpenAPI 3.0 contract
├── docs/
│   └── sources/
│       └── 001-clinic-followup/   # Source materials
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## Development Workflow

### 1. Create Database Migration

```bash
alembic revision --autogenerate -m "Add new_table"
# Review generated migration in alembic/versions/
alembic upgrade head
```

### 2. Run Tests

```bash
# Unit tests
pytest tests/unit/ -v

# Integration tests (requires test DB)
pytest tests/integration/ -v

# Contract tests (validates API against OpenAPI spec)
pytest tests/contract/ -v

# All tests with coverage
pytest --cov=app --cov-report=html
# View coverage report: open htmlcov/index.html
```

### 3. Lint & Format

```bash
# Black (code formatting)
black app/ tests/

# Ruff (linting)
ruff check app/ tests/

# MyPy (type checking)
mypy app/
```

### 4. Check for Hardcoded UI Strings

```bash
# Best-effort lint for hardcoded strings (should use label keys)
python scripts/check_hardcoded_strings.py app/ui/
```

---

## Key Architectural Patterns

### Tenant Isolation (Multi-Clinic)

All tenant-scoped repositories extend `TenantAwareRepository`:

```python
# app/repositories/base.py
class TenantAwareRepository:
    def __init__(self, db: Session, clinic_id: UUID):
        self.db = db
        self.clinic_id = clinic_id
    
    def _apply_clinic_filter(self, query):
        return query.filter(self.model.clinic_id == self.clinic_id)

# Usage in API
@router.get("/patients")
def list_patients(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    repo = PatientRepository(db, current_user.active_clinic_id)
    return repo.list()  # Automatically filtered by clinic_id
```

### Internationalization (i18n)

All UI text uses label keys:

```python
# app/services/label_service.py
class LabelService:
    def __init__(self, locale: str = "pt-BR"):
        self.locale = locale
        self.labels = self._load_labels()
    
    def t(self, key: str, **kwargs) -> str:
        """Translate label key with interpolation"""
        value = self.labels.get(key, f"[MISSING: {key}]")
        return value.format(**kwargs)

# Usage in Streamlit
from app.services.label_service import label_service as t

st.title(t("admin.dashboard.title"))
st.write(t("patient.tasks.due_count", count=5))
```

Label files: `resources/labels/pt-BR.json`
```json
{
  "admin.dashboard.title": "Painel Administrativo",
  "patient.tasks.due_count": "{count} tarefas pendentes"
}
```

### Scoring Engine

Base points and streak bonuses are computed in `ScoringService`:

```python
# app/services/scoring_service.py
class ScoringService:
    def compute_base_points(self, task: Task) -> int:
        """FR-POINTS-01: Base scoring logic"""
        base = 100
        if task.had_delay:
            base -= 20
        if task.had_pause:
            base -= 25
        return max(0, base)
    
    def compute_streak_bonus(self, patient_id: UUID, task: Task) -> int:
        """FR-POINTS-02: Streak bonus (validated completions only)"""
        eligible = self._get_eligible_completions(patient_id)
        chain_position = self._compute_chain_position(eligible, task)
        return 10 + (chain_position * 2)
```

### Redemption Workflow

Points are reserved immediately on request, refunded on rejection/expiry:

```python
# app/services/redemption_service.py
class RedemptionService:
    def request_redemption(self, patient_id: UUID, reward_id: UUID) -> Redemption:
        """FR-REDEEM-01: Request redemption with eligibility snapshot"""
        reward = self.reward_repo.get(reward_id)
        patient = self.patient_repo.get(patient_id)
        
        # Check eligibility
        if patient.points_balance < reward.points_cost:
            raise InsufficientPointsError()
        
        # Snapshot eligibility
        snapshot = self._snapshot_eligibility(patient, reward)
        
        # Reserve points
        self.ledger_service.add_entry(
            patient_id, 
            event_type="REDEMPTION_RESERVED", 
            points_delta=-reward.points_cost
        )
        
        return self.redemption_repo.create(
            patient_id=patient_id,
            reward_id=reward_id,
            status="REQUESTED",
            eligibility_snapshot=snapshot
        )
```

---

## Testing Examples

### Unit Test (Scoring Logic)

```python
# tests/unit/test_scoring_service.py
def test_streak_bonus_chain_increment():
    """FR-POINTS-02: Streak bonus increments by +2 per link"""
    service = ScoringService()
    
    # Simulate 5 consecutive eligible completions
    bonuses = [service.compute_streak_bonus(patient_id, task) 
               for task in eligible_tasks]
    
    assert bonuses == [10, 12, 14, 16, 18]
```

### Integration Test (API + DB)

```python
# tests/integration/test_tasks_api.py
def test_assign_task_enforces_tenant_isolation(client, db, admin_user, patient_clinic_a, patient_clinic_b):
    """Verify admin in clinic A cannot assign task to patient in clinic B"""
    # Admin from Clinic A
    client.login(admin_user)
    
    response = client.post(
        f"/api/v1/patients/{patient_clinic_b.id}/tasks",
        json={"pillar_id": str(pillar_id), "title": "Test Task", "due_at": "2026-02-01T12:00:00Z"}
    )
    
    assert response.status_code == 404  # Patient not found in admin's clinic
```

### Contract Test (OpenAPI Validation)

```python
# tests/contract/test_openapi_contract.py
import schemathesis

schema = schemathesis.from_uri("http://localhost:8000/api/docs/openapi.json")

@schema.parametrize()
def test_api_conforms_to_contract(case):
    """Validates all API endpoints against OpenAPI spec"""
    response = case.call()
    case.validate_response(response)
```

---

## Manual Validation (Acceptance Criteria)

### AC1: Multi-Clinic Isolation

1. Login as admin: `admin@contoso.com` / `admin123`
2. Create new clinic: "Clinic B"
3. Create patient in Clinic B
4. Switch active clinic to "Contoso"
5. Verify patient from Clinic B is NOT visible in patient list ✅

### AC2: Setup Flow

1. As admin in new clinic:
   - Create Methodology: "Diabetes Care"
   - Add 3 Pillars: "Nutrition", "Exercise", "Medication"
   - Create Follow-up Plan: "Diabetes Follow-up" (link methodology + pillars)
   - Create 3 Journey Stages: "Lead" (order=0), "Onboarding" (order=1), "Active" (order=2)
2. Verify all entities are visible in admin UI ✅

### AC3: Task Assignment & Status

1. Assign task to patient (title="Log Blood Glucose", due_at=tomorrow)
2. Login as patient: `patient1@contoso.com` / `patient123`
3. View task in patient UI
4. Change status to "FEITO" (done)
5. Verify status transition is recorded ✅

### AC4: Scoring

1. Assign task with due_at=tomorrow
2. Patient completes before due date
3. Admin validates completion
4. Verify:
   - Base points: 100 (no deductions)
   - Streak bonus: 10 (first in chain)
5. Check patient points ledger shows both entries ✅

### AC5: Rewards & Eligibility

1. Create vendor: "Amazon"
2. Create reward: "Gift Card" (points_cost=200, quantity=10, eligible_plan_id=<Diabetes Follow-up>)
3. Login as patient NOT enrolled in Diabetes Follow-up
4. Verify reward is NOT shown in eligible list
5. Enroll patient in Diabetes Follow-up
6. Verify reward is NOW shown ✅

### AC6: Redemption Flow

1. Patient with 500 points requests reward (cost=200)
2. Verify points balance: 500 - 200 = 300
3. Admin approves redemption
4. Admin marks as "REDEEMED"
5. Verify final points balance: 300 ✅

### AC7: UI Labels (i18n)

1. Check `resources/labels/pt-BR.json` exists
2. Search codebase for hardcoded strings: `python scripts/check_hardcoded_strings.py`
3. Verify no hardcoded UI text found (best-effort check)
4. Change `APP_LOCALE=en-US` in `.env` (requires `resources/labels/en-US.json`)
5. Verify UI uses fallback to pt-BR if en-US key missing ✅

### AC8: LGPD Compliance

1. Query audit logs: `SELECT * FROM audit_logs WHERE event_type LIKE 'AUTH%' LIMIT 10`
2. Verify login/logout events are logged with timestamps
3. Verify task status changes are logged
4. Verify redemptions are logged
5. Check retention policy config: `analytics_period_days` in clinic table ✅

---

## Troubleshooting

### Database connection error

```bash
# Check PostgreSQL is running
docker-compose ps

# Check .env DATABASE_URL is correct
cat .env | grep DATABASE_URL

# Test connection
psql -h localhost -U postgres -d swaif_clinic_followup -c "SELECT 1"
```

### Migration error

```bash
# Rollback last migration
alembic downgrade -1

# Check migration history
alembic history

# Reset database (WARNING: deletes all data)
alembic downgrade base
alembic upgrade head
python scripts/seed_data.py
```

### Missing label key

If you see `[MISSING: some.key]` in UI:
1. Add key to `resources/labels/pt-BR.json`
2. Restart Streamlit app

### Tests failing

```bash
# Ensure test database is clean
pytest --create-db

# Run single test for debugging
pytest tests/unit/test_scoring_service.py::test_streak_bonus_chain_increment -v
```

---

## Next Steps

After validating the quickstart:

1. Review implementation checklist: `specs/001-clinic-followup/tasks.md`
2. Start with Task 0: Repo & Tooling
3. Follow dependency order in tasks.md
4. Run tests after each task batch
5. Update `.github/copilot-instructions.md` with new patterns

---

## Resources

- **Feature Spec**: [specs/001-clinic-followup/spec.md](./spec.md)
- **Implementation Plan**: [specs/001-clinic-followup/plan.md](./plan.md)
- **Data Model**: [specs/001-clinic-followup/data-model.md](./data-model.md)
- **API Contract**: [specs/001-clinic-followup/contracts/openapi.yaml](./contracts/openapi.yaml)
- **Research**: [specs/001-clinic-followup/research.md](./research.md)

---

## Support

For issues or questions:
- Check existing GitHub issues
- Review constitution: `.specify/memory/constitution.md`
- Review Copilot instructions: `.github/copilot-instructions.md`
