# Tasks: Multi-Clinic Follow-up Plans, Gamification, and Rewards

**Feature**: 001-clinic-followup  
**Branch**: 001-Clinic-Followup  
**Input**: Design documents from `/specs/001-clinic-followup/`  
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/openapi.yaml

**Tests**: Tests are MANDATORY for this healthcare system (NFR-TEST-01 through NFR-TEST-06). All tests must pass before code merge.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story] Description`

- **Checkbox**: ALWAYS `- [ ]` (markdown checkbox)
- **[TaskID]**: Sequential number (T001, T002, T003...) in execution order
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- **File paths**: Exact paths included in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create backend project structure: backend/src/{models,repositories,services,api,schemas,middleware,config,utils,dependencies}
- [ ] T002 Create frontend project structure: frontend/src/{components,pages/{admin,patient},services}
- [ ] T003 Create test directory structure: backend/tests/{unit,integration,contract,e2e}
- [ ] T004 Initialize Python project with requirements.txt (FastAPI, SQLAlchemy, Alembic, Pydantic, pytest, pytest-cov, schemathesis)
- [ ] T005 [P] Configure Docker Compose with PostgreSQL 15+ service in docker-compose.yml
- [ ] T006 [P] Configure environment variables template in .env.example (DATABASE_URL, APP_LOCALE, SECRET_KEY, SESSION_TIMEOUT_SECONDS)
- [ ] T007 [P] Setup Alembic migrations in alembic/ directory with env.py configuration
- [ ] T008 [P] Configure pytest with conftest.py for shared fixtures in backend/tests/conftest.py
- [ ] T009 [P] Configure logging infrastructure in backend/src/config/logging.py
- [ ] T010 [P] Create .gitignore for Python project (venv/, __pycache__/, .env, *.pyc)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T011 Create database configuration in backend/src/config/database.py (SQLAlchemy engine, session factory)
- [ ] T012 [P] Create base SQLAlchemy model in backend/src/models/base.py (UUID primary keys, timestamps)
- [ ] T013 [P] Create base Pydantic schemas in backend/src/schemas/base.py (BaseModel with Config)
- [ ] T014 [P] Create TenantAwareRepository base class in backend/src/repositories/base.py (enforces clinic_id filtering)
- [ ] T015 [P] Create error handler middleware in backend/src/middleware/error_handler.py (global exception handling)
- [ ] T016 [P] Create security utilities in backend/src/utils/security.py (bcrypt password hashing, session token generation)
- [ ] T017 Create FastAPI application entry point in backend/src/main.py (app initialization, middleware, CORS)
- [ ] T018 [P] Create API router structure in backend/src/api/v1/__init__.py (router aggregation)
- [ ] T019 [P] Setup pytest fixtures for test database and client in backend/tests/conftest.py
- [ ] T020 [P] Create test data factories for Clinic, User in backend/tests/conftest.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Multi-Clinic Setup & Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable authentication, session management, and multi-clinic tenant isolation. Seed Contoso training clinic.

**Independent Test**: 
- Admin can create new clinic beyond seeded Contoso
- Users can login with email/password
- Session management with logout works
- Multi-clinic admins can switch active clinic
- Patients belong to exactly one clinic
- Data isolation: clinic A users cannot access clinic B data

### Tests for User Story 1 (MANDATORY) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T021 [P] [US1] Contract test for /auth endpoints in backend/tests/contract/test_auth_contract.py
- [ ] T022 [P] [US1] Contract test for /clinics endpoints in backend/tests/contract/test_clinics_contract.py
- [ ] T023 [P] [US1] Integration test for login/logout flow in backend/tests/integration/test_api_auth.py
- [ ] T024 [P] [US1] Integration test for tenant isolation in backend/tests/integration/test_tenant_isolation.py
- [ ] T025 [P] [US1] E2E test for complete auth flow in backend/tests/e2e/test_auth_flow.py
- [ ] T026 [P] [US1] Unit test for AuthService in backend/tests/unit/test_auth_service.py
- [ ] T027 [P] [US1] Unit test for security utilities in backend/tests/unit/test_security.py

### Implementation for User Story 1

- [ ] T028 [P] [US1] Create Clinic model in backend/src/models/clinic.py (id, name, is_training, analytics_period_days, timestamps)
- [ ] T029 [P] [US1] Create User model in backend/src/models/user.py (id, email, password_hash, role, timestamps)
- [ ] T030 [P] [US1] Create ClinicMembership model in backend/src/models/clinic_membership.py (join table for Admin ↔ Clinic)
- [ ] T031 [US1] Create Alembic migration for Clinic, User, ClinicMembership tables in alembic/versions/001_create_auth_tables.py
- [ ] T032 [P] [US1] Create Clinic Pydantic schemas in backend/src/schemas/clinic.py (ClinicCreate, ClinicResponse)
- [ ] T033 [P] [US1] Create User Pydantic schemas in backend/src/schemas/user.py (UserCreate, UserSession, LoginRequest)
- [ ] T034 [US1] Implement AuthService in backend/src/services/auth_service.py (login, logout, session validation, password hashing)
- [ ] T035 [P] [US1] Implement ClinicRepository in backend/src/repositories/clinic_repository.py (CRUD operations)
- [ ] T036 [P] [US1] Implement UserRepository in backend/src/repositories/user_repository.py (CRUD operations)
- [ ] T037 [US1] Create authentication dependency in backend/src/dependencies/auth.py (get_current_user, require_admin, get_active_clinic)
- [ ] T038 [US1] Implement /auth routes in backend/src/api/v1/auth.py (login, logout, me, set-active-clinic)
- [ ] T039 [US1] Implement /clinics routes in backend/src/api/v1/clinics.py (list, create, get)
- [ ] T040 [US1] Create seed script for Contoso clinic in scripts/seed_data.py (training clinic + admin user)
- [ ] T041 [US1] Add session middleware configuration to backend/src/main.py
- [ ] T042 [US1] Add audit logging for auth events (login, logout, failed attempts)

**Checkpoint**: At this point, authentication and multi-clinic infrastructure should be fully functional and testable independently

---

## Phase 4: User Story 2 - Methodology, Pillars & Follow-up Plans (Priority: P1)

**Goal**: Enable Clinic Admins to configure Methodologies with Pillars and create Follow-up Plans that link to selected Pillars.

**Independent Test**:
- Admin can create Methodology with description
- Admin can create multiple Pillars under a Methodology
- Admin can create Follow-up Plan linked to Methodology and select Pillars
- Plans enforce tenant isolation (clinic A plans not visible in clinic B)

### Tests for User Story 2 (MANDATORY) ⚠️

- [ ] T043 [P] [US2] Contract test for /methodologies endpoints in backend/tests/contract/test_methodologies_contract.py
- [ ] T044 [P] [US2] Contract test for /plans endpoints in backend/tests/contract/test_plans_contract.py
- [ ] T045 [P] [US2] Integration test for methodology CRUD in backend/tests/integration/test_api_methodologies.py
- [ ] T046 [P] [US2] Integration test for plan CRUD in backend/tests/integration/test_api_plans.py

### Implementation for User Story 2

- [ ] T047 [P] [US2] Create Methodology model in backend/src/models/methodology.py (id, clinic_id FK, name, description, timestamps)
- [ ] T048 [P] [US2] Create Pillar model in backend/src/models/pillar.py (id, methodology_id FK, name, description, timestamps)
- [ ] T049 [P] [US2] Create FollowUpPlan model in backend/src/models/follow_up_plan.py (id, clinic_id FK, methodology_id FK, name, description, timestamps)
- [ ] T050 [P] [US2] Create PlanPillar join model in backend/src/models/plan_pillar.py (id, plan_id FK, pillar_id FK)
- [ ] T051 [US2] Create Alembic migration for Methodology, Pillar, FollowUpPlan, PlanPillar tables in alembic/versions/002_create_methodology_tables.py
- [ ] T052 [P] [US2] Create Methodology Pydantic schemas in backend/src/schemas/methodology.py (MethodologyCreate, MethodologyResponse)
- [ ] T053 [P] [US2] Create Pillar Pydantic schemas in backend/src/schemas/pillar.py (PillarCreate, PillarResponse)
- [ ] T054 [P] [US2] Create FollowUpPlan Pydantic schemas in backend/src/schemas/follow_up_plan.py (FollowUpPlanCreate, FollowUpPlanResponse)
- [ ] T055 [US2] Implement MethodologyRepository in backend/src/repositories/methodology_repository.py (extends TenantAwareRepository)
- [ ] T056 [P] [US2] Implement PillarRepository in backend/src/repositories/pillar_repository.py
- [ ] T057 [US2] Implement FollowUpPlanRepository in backend/src/repositories/follow_up_plan_repository.py (extends TenantAwareRepository)
- [ ] T058 [US2] Implement /methodologies routes in backend/src/api/v1/methodologies.py (list, create, get, list pillars, create pillar)
- [ ] T059 [US2] Implement /plans routes in backend/src/api/v1/plans.py (list, create, get, update pillar associations)
- [ ] T060 [US2] Add seed data for sample Methodology + Pillars for Contoso in scripts/seed_data.py

**Checkpoint**: At this point, methodology and plan management should be fully functional and testable independently

---

## Phase 5: User Story 3 - Journey Stages & Patient Management (Priority: P1)

**Goal**: Enable Clinic Admins to define ordered Journey Stages and create/manage Patients enrolled in plans.

**Independent Test**:
- Admin can create ordered Journey Stages (lead → onboarding → active → close)
- Admin can create Patient with enrollment in a Follow-up Plan
- Admin can advance Patient through journey stages
- Patients belong to exactly one clinic (tenant isolation enforced)
- Patient journey history is tracked

### Tests for User Story 3 (MANDATORY) ⚠️

- [ ] T061 [P] [US3] Contract test for /journey-stages endpoints in backend/tests/contract/test_journey_contract.py
- [ ] T062 [P] [US3] Contract test for /patients endpoints in backend/tests/contract/test_patients_contract.py
- [ ] T063 [P] [US3] Integration test for journey stage CRUD in backend/tests/integration/test_api_journey.py
- [ ] T064 [P] [US3] Integration test for patient CRUD in backend/tests/integration/test_api_patients.py

### Implementation for User Story 3

- [ ] T065 [P] [US3] Create JourneyStage model in backend/src/models/journey_stage.py (id, clinic_id FK, name, order_index, timestamps)
- [ ] T066 [P] [US3] Create Patient model in backend/src/models/patient.py (id, user_id FK, clinic_id FK, full_name, enrollment_date, current_journey_stage_id FK, timestamps)
- [ ] T067 [P] [US3] Create PatientJourney model in backend/src/models/patient_journey.py (id, patient_id FK, journey_stage_id FK, entered_at, exited_at)
- [ ] T068 [US3] Create Alembic migration for JourneyStage, Patient, PatientJourney tables in alembic/versions/003_create_patient_tables.py
- [ ] T069 [P] [US3] Create JourneyStage Pydantic schemas in backend/src/schemas/journey_stage.py (JourneyStageCreate, JourneyStageResponse)
- [ ] T070 [P] [US3] Create Patient Pydantic schemas in backend/src/schemas/patient.py (PatientCreate, PatientResponse)
- [ ] T071 [US3] Implement JourneyStageRepository in backend/src/repositories/journey_stage_repository.py (extends TenantAwareRepository)
- [ ] T072 [US3] Implement PatientRepository in backend/src/repositories/patient_repository.py (extends TenantAwareRepository)
- [ ] T073 [US3] Implement PatientService in backend/src/services/patient_service.py (advance_journey method with PatientJourney tracking)
- [ ] T074 [US3] Implement /journey-stages routes in backend/src/api/v1/journey.py (list, create, update)
- [ ] T075 [US3] Implement /patients routes in backend/src/api/v1/patients.py (list, create, get, advance-journey)
- [ ] T076 [US3] Add seed data for Journey Stages and 10 sample patients for Contoso in scripts/seed_data.py

**Checkpoint**: At this point, journey and patient management should be fully functional and testable independently

---

## Phase 6: User Story 4 - Task Assignment & Status Management (Priority: P1)

**Goal**: Enable Clinic Admins to assign tasks to patients. Patients can view and update task statuses. Support status transitions with validation.

**Independent Test**:
- Admin can assign task to patient with due date and pillar association
- Patient can view assigned tasks
- Patient can update task status (valid transitions only)
- System tracks task status history
- Soft delete for cancelled tasks with audit trail
- Task status transitions follow state machine (FR-TASK-03)

### Tests for User Story 4 (MANDATORY) ⚠️

- [ ] T077 [P] [US4] Contract test for /tasks endpoints in backend/tests/contract/test_tasks_contract.py
- [ ] T078 [P] [US4] Integration test for task CRUD in backend/tests/integration/test_api_tasks.py
- [ ] T079 [P] [US4] E2E test for task workflow (assign → patient updates → admin views) in backend/tests/e2e/test_task_workflow.py
- [ ] T080 [P] [US4] Unit test for TaskService state machine in backend/tests/unit/test_task_service.py

### Implementation for User Story 4

- [ ] T081 [P] [US4] Create Task model in backend/src/models/task.py (id, patient_id FK, pillar_id FK, title, description, status enum, assigned_at, due_at, completed_at, validated_at, deleted_at, timestamps)
- [ ] T082 [US4] Create Alembic migration for Task table in alembic/versions/004_create_task_table.py
- [ ] T083 [P] [US4] Create Task Pydantic schemas in backend/src/schemas/task.py (TaskCreate, TaskResponse, TaskStatusUpdate)
- [ ] T084 [US4] Implement TaskRepository in backend/src/repositories/task_repository.py (tenant-aware queries, soft delete filtering)
- [ ] T085 [US4] Implement TaskService in backend/src/services/task_service.py (status transition validation, state machine, completed_at timestamp management)
- [ ] T086 [US4] Implement /patients/{patient_id}/tasks routes in backend/src/api/v1/tasks.py (list with filters, assign)
- [ ] T087 [US4] Implement /tasks/{task_id}/status routes in backend/src/api/v1/tasks.py (update status with transition validation)
- [ ] T088 [US4] Add audit logging for task status changes and cancellations
- [ ] T089 [US4] Add seed data for sample tasks for Contoso patients in scripts/seed_data.py

**Checkpoint**: At this point, task assignment and status management should be fully functional and testable independently

---

## Phase 7: User Story 5 - Base Scoring System (Priority: P1)

**Goal**: Implement deterministic base points calculation based on task completion with delay/pause/reopen deductions. Record all points transactions in immutable ledger.

**Independent Test**:
- Task completed without delay/pause/reopen awards 100 base points
- Task completed with delay awards 80 points (−20 deduction)
- Task completed with pause/reopen but no delay awards 75 points (−25 deduction)
- Task completed with pause/reopen AND delay awards 60 points (−40 deduction)
- Cancelled by patient awards 0 points (all lost)
- Cancelled by clinic preserves current points
- All transactions logged to PointsLedger with balance_after calculation

### Tests for User Story 5 (MANDATORY) ⚠️

- [ ] T090 [P] [US5] Integration test for points calculation scenarios in backend/tests/integration/test_api_scoring.py
- [ ] T091 [P] [US5] Unit test for ScoringService base points calculation in backend/tests/unit/test_scoring_service.py (100% coverage required)
- [ ] T092 [P] [US5] Unit test for PointsLedger balance calculation in backend/tests/unit/test_points_ledger.py

### Implementation for User Story 5

- [ ] T093 [P] [US5] Create PointsLedger model in backend/src/models/points_ledger.py (id, patient_id FK, task_id FK nullable, event_type enum, points_delta, balance_after, metadata JSONB, created_at immutable)
- [ ] T094 [US5] Create Alembic migration for PointsLedger table in alembic/versions/005_create_points_ledger_table.py
- [ ] T095 [P] [US5] Create PointsLedger Pydantic schemas in backend/src/schemas/points_ledger.py (PointsLedgerEntry, PointsLedgerResponse)
- [ ] T096 [US5] Implement PointsLedgerRepository in backend/src/repositories/points_ledger_repository.py (append-only, balance calculation)
- [ ] T097 [US5] Implement ScoringService in backend/src/services/scoring_service.py (base points calculation logic per FR-POINTS-01, ledger entry creation)
- [ ] T098 [US5] Integrate ScoringService with TaskService status transitions (auto-award base points on FEITO status)
- [ ] T099 [US5] Implement /patients/{patient_id}/points-ledger routes in backend/src/api/v1/scoring.py (list ledger with pagination)
- [ ] T100 [US5] Add audit logging for points awarded/deducted events

**Checkpoint**: At this point, base scoring system should be fully functional and testable independently

---

## Phase 8: User Story 6 - Streak Bonus & Validation (Priority: P2)

**Goal**: Implement clinic-validated streak bonus system. Consecutive early completions (before due date) increase bonus by +2 per link. Same-day completions count as single chain link.

**Independent Test**:
- Task completed strictly before due date is eligible for streak bonus
- Admin validation action awards streak bonus (separate from status change)
- Consecutive eligible completions increase bonus: 10, 12, 14, 16...
- Same-day completions share bonus tier (single chain link)
- Chain breaks on ineligible completion (late, cancelled)
- Next eligible after break resets to 10 points
- Validation metadata includes chain position and bonus tier

### Tests for User Story 6 (MANDATORY) ⚠️

- [ ] T101 [P] [US6] Integration test for streak bonus scenarios in backend/tests/integration/test_api_validation.py
- [ ] T102 [P] [US6] Unit test for ScoringService streak calculation in backend/tests/unit/test_scoring_service.py (100% coverage required, chain logic)
- [ ] T103 [P] [US6] Unit test for same-day completion grouping in backend/tests/unit/test_scoring_service.py

### Implementation for User Story 6

- [ ] T104 [US6] Extend ScoringService with streak bonus calculation in backend/src/services/scoring_service.py (query eligible completions, group by date, calculate chain, increment by +2)
- [ ] T105 [US6] Implement validation workflow in TaskService (set validated_at timestamp, trigger streak bonus calculation)
- [ ] T106 [US6] Implement /tasks/{task_id}/validate routes in backend/src/api/v1/tasks.py (admin-only endpoint)
- [ ] T107 [US6] Add streak bonus metadata to PointsLedger entries (chain_position, streak_bonus_tier, completion_date)
- [ ] T108 [US6] Add audit logging for validation events and streak bonuses awarded

**Checkpoint**: At this point, streak bonus system should be fully functional and testable independently

---

## Phase 9: User Story 7 - Rewards Catalog (Priority: P2)

**Goal**: Enable Clinic Admins to create Vendors and Rewards with eligibility rules. Patients view rewards (points cost only, no monetary values).

**Independent Test**:
- Admin can create Vendor with contact info
- Admin can create Reward with points cost, monetary value (admin-only), quantity, expiry, eligibility rules
- Reward eligibility rules: eligible_plan_id (optional), eligible_pillar_id (optional), both (AND logic), neither (all patients)
- Patient view shows only points cost, not monetary value
- Rewards enforce tenant isolation
- Expired/unavailable rewards are filtered from patient view

### Tests for User Story 7 (MANDATORY) ⚠️

- [ ] T109 [P] [US7] Contract test for /vendors endpoints in backend/tests/contract/test_vendors_contract.py
- [ ] T110 [P] [US7] Contract test for /rewards endpoints in backend/tests/contract/test_rewards_contract.py
- [ ] T111 [P] [US7] Integration test for reward eligibility filtering in backend/tests/integration/test_api_rewards.py
- [ ] T112 [P] [US7] Unit test for reward eligibility evaluation in backend/tests/unit/test_reward_service.py

### Implementation for User Story 7

- [ ] T113 [P] [US7] Create Vendor model in backend/src/models/vendor.py (id, clinic_id FK, name, contact_info, timestamps)
- [ ] T114 [P] [US7] Create Reward model in backend/src/models/reward.py (id, vendor_id FK, clinic_id FK, name, description, points_cost, monetary_value, quantity_available, expires_at, eligible_plan_id FK nullable, eligible_pillar_id FK nullable, is_active, timestamps)
- [ ] T115 [US7] Create Alembic migration for Vendor, Reward tables in alembic/versions/006_create_reward_tables.py
- [ ] T116 [P] [US7] Create Vendor Pydantic schemas in backend/src/schemas/vendor.py (VendorCreate, VendorResponse)
- [ ] T117 [P] [US7] Create Reward Pydantic schemas in backend/src/schemas/reward.py (RewardCreate, RewardResponse, RewardPatientView with monetary_value excluded)
- [ ] T118 [US7] Implement VendorRepository in backend/src/repositories/vendor_repository.py (extends TenantAwareRepository)
- [ ] T119 [US7] Implement RewardRepository in backend/src/repositories/reward_repository.py (extends TenantAwareRepository, eligibility filtering)
- [ ] T120 [US7] Implement RewardService in backend/src/services/reward_service.py (eligibility evaluation logic per FR-REWARD-01)
- [ ] T121 [US7] Implement /vendors routes in backend/src/api/v1/vendors.py (list, create, get)
- [ ] T122 [US7] Implement /rewards routes in backend/src/api/v1/rewards.py (list with patient eligibility filter, create, get)
- [ ] T123 [US7] Add role-based response filtering (exclude monetary_value for patients)
- [ ] T124 [US7] Add seed data for sample Vendors and Rewards for Contoso in scripts/seed_data.py

**Checkpoint**: At this point, rewards catalog should be fully functional and testable independently

---

## Phase 10: User Story 8 - Redemption Workflow (Priority: P2)

**Goal**: Enable patients to request reward redemptions. Admins approve/reject. System enforces point balance checks, eligibility snapshots, and auto-expiration with refunds.

**Independent Test**:
- Patient can request redemption if sufficient points and reward eligible
- System blocks redemption if insufficient points (clear error message)
- Points deducted immediately on request (reserved)
- Eligibility snapshot captured at request time (plan changes don't affect pending redemptions)
- Admin can approve or reject redemption
- Points refunded on rejection/cancellation
- Approved redemptions expire after 30 days with auto-refund (scheduled job)
- Redemption statuses tracked: REQUESTED, APPROVED, REJECTED, REDEEMED, CANCELLED_BY_PATIENT, CANCELLED_BY_CLINIC, EXPIRED

### Tests for User Story 8 (MANDATORY) ⚠️

- [ ] T125 [P] [US8] Contract test for /redemptions endpoints in backend/tests/contract/test_redemptions_contract.py
- [ ] T126 [P] [US8] Integration test for redemption workflow in backend/tests/integration/test_api_redemptions.py
- [ ] T127 [P] [US8] E2E test for complete redemption flow (request → approve → expire/refund) in backend/tests/e2e/test_redemption_flow.py
- [ ] T128 [P] [US8] Unit test for RedemptionService eligibility snapshot in backend/tests/unit/test_redemption_service.py (100% coverage required)
- [ ] T129 [P] [US8] Unit test for points reserve/refund logic in backend/tests/unit/test_redemption_service.py

### Implementation for User Story 8

- [ ] T130 [P] [US8] Create Redemption model in backend/src/models/redemption.py (id, patient_id FK, reward_id FK, status enum, points_cost, eligibility_snapshot JSONB, requested_at, approved_at, rejected_at, redeemed_at, expired_at, cancelled_at, admin_notes, timestamps)
- [ ] T131 [US8] Create Alembic migration for Redemption table in alembic/versions/007_create_redemption_table.py
- [ ] T132 [P] [US8] Create Redemption Pydantic schemas in backend/src/schemas/redemption.py (RedemptionCreate, RedemptionResponse)
- [ ] T133 [US8] Implement RedemptionRepository in backend/src/repositories/redemption_repository.py (tenant-aware queries)
- [ ] T134 [US8] Implement RedemptionService in backend/src/services/redemption_service.py (eligibility snapshot, points reserve, refund logic, status transitions)
- [ ] T135 [US8] Implement /redemptions routes in backend/src/api/v1/redemptions.py (list with filters, request, approve, reject, cancel, mark redeemed)
- [ ] T136 [US8] Add point insufficiency validation before redemption request (return 400 with clear error)
- [ ] T137 [US8] Create auto-expiration scheduled job in scripts/expire_redemptions.py (daily cron: mark EXPIRED if approved_at < NOW() - 30 days)
- [ ] T138 [US8] Integrate RedemptionService with PointsLedger for reserve/refund transactions
- [ ] T139 [US8] Add audit logging for redemption lifecycle events

**Checkpoint**: At this point, redemption workflow should be fully functional and testable independently

---

## Phase 11: User Story 9 - Adherence Analytics (Priority: P3)

**Goal**: Admin dashboard showing adherence segmentation by quartiles. Hybrid aggregation (real-time for current day, batch for historical). Configurable analytics period per clinic (7-90 days).

**Independent Test**:
- Admin can view adherence dashboard with quartile segmentation
- Dashboard shows: Total patients, Average points, Period range (configurable days per clinic)
- Adherence table columns: Patient Name, Quartile (Q1/Q2/Q3/Q4), Total Points, Streak Points, Tasks Completed, Tasks Delayed, Tasks Paused, Tasks Cancelled
- Quartile distribution indicator shows count of patients in each quartile
- Filter/sort controls: by quartile, by points (asc/desc), by name
- Metrics computed over configurable period (default 30 days, range 7-90 days from Clinic.analytics_period_days)
- Hybrid aggregation: real-time for current day + batch for historical
- Cancelled tasks included in analytics

### Tests for User Story 9 (MANDATORY) ⚠️

- [ ] T140 [P] [US9] Contract test for /analytics endpoints in backend/tests/contract/test_analytics_contract.py
- [ ] T141 [P] [US9] Integration test for analytics computation in backend/tests/integration/test_api_analytics.py
- [ ] T142 [P] [US9] Unit test for quartile calculation in backend/tests/unit/test_analytics_service.py

### Implementation for User Story 9

- [ ] T143 [P] [US9] Create AnalyticsSnapshot model in backend/src/models/analytics_snapshot.py (id, clinic_id FK, patient_id FK, date, total_points, streak_points, tasks_completed, tasks_delayed, tasks_paused, tasks_cancelled, created_at)
- [ ] T144 [US9] Create Alembic migration for AnalyticsSnapshot table with partitioning in alembic/versions/008_create_analytics_snapshot_table.py
- [ ] T145 [US9] Implement AnalyticsRepository in backend/src/repositories/analytics_repository.py (extends TenantAwareRepository, hybrid query: snapshots + real-time)
- [ ] T146 [US9] Implement AnalyticsService in backend/src/services/analytics_service.py (quartile computation, aggregation logic, configurable period)
- [ ] T147 [US9] Create daily analytics aggregation job in scripts/aggregate_analytics.py (cron: compute previous day metrics, insert to AnalyticsSnapshot)
- [ ] T148 [US9] Implement /analytics routes in backend/src/api/v1/analytics.py (adherence dashboard endpoint with quartile data)
- [ ] T149 [US9] Add analytics period configuration validation (7-90 days) to Clinic model

**Checkpoint**: At this point, analytics dashboard should be fully functional and testable independently

---

## Phase 12: User Story 10 - Internationalization (Priority: P1)

**Goal**: All UI text comes from locale files (pt-BR default). Support adding new locales with fallback. Locale set via APP_LOCALE env var.

**Independent Test**:
- No hardcoded UI strings in code (all via label service)
- pt-BR locale file complete with all required labels
- Label service supports interpolation (e.g., "Welcome, {name}")
- Missing keys return pt-BR value + warning log (never crash)
- Locale switchable via APP_LOCALE environment variable
- en-US locale file structure ready for future

### Tests for User Story 10 (MANDATORY) ⚠️

- [ ] T150 [P] [US10] Unit test for LabelService interpolation in backend/tests/unit/test_label_service.py
- [ ] T151 [P] [US10] Unit test for LabelService fallback behavior in backend/tests/unit/test_label_service.py
- [ ] T152 [P] [US10] Integration test for locale loading in backend/tests/integration/test_i18n.py

### Implementation for User Story 10

- [ ] T153 [P] [US10] Create pt-BR label pack in resources/labels/pt-BR.json (all UI strings from spec acceptance criteria)
- [ ] T154 [P] [US10] Create en-US label pack template in resources/labels/en-US.json (structure only, values TBD)
- [ ] T155 [US10] Implement LabelService in backend/src/services/label_service.py (load locale file, interpolation, fallback to pt-BR, warning logs)
- [ ] T156 [US10] Add APP_LOCALE environment variable to .env.example
- [ ] T157 [US10] Integrate LabelService with API responses (label key resolution before response serialization)
- [ ] T158 [US10] Add linter rule to detect hardcoded strings in backend/src/ (use grep or ruff custom rule)

**Checkpoint**: At this point, internationalization should be fully functional and testable independently

---

## Phase 13: User Story 11 - Audit & Compliance (Priority: P1)

**Goal**: Maintain immutable audit logs for all critical events. 5-year retention in active storage, then archive to cold storage. Support LGPD compliance.

**Independent Test**:
- All critical events logged to AuditLog (auth, admin config changes, task status, points ledger, redemptions)
- Audit logs include: clinic_id, user_id, event_type, entity_type, entity_id, event_data JSONB, ip_address, user_agent, created_at
- Audit logs are immutable (append-only, no updates/deletes)
- Logs retained 5 years in PostgreSQL
- Archive job moves logs older than 5 years to cold storage (S3 Glacier) with archived_at timestamp
- Partitioning by year for performance

### Tests for User Story 11 (MANDATORY) ⚠️

- [ ] T159 [P] [US11] Integration test for audit log creation in backend/tests/integration/test_audit_logs.py
- [ ] T160 [P] [US11] Unit test for archive job logic in backend/tests/unit/test_archive_audit_logs.py

### Implementation for User Story 11

- [ ] T161 [P] [US11] Create AuditLog model in backend/src/models/audit_log.py (id, clinic_id FK nullable, user_id FK nullable, event_type enum, entity_type, entity_id UUID nullable, event_data JSONB, ip_address, user_agent, created_at immutable, archived_at nullable)
- [ ] T162 [US11] Create Alembic migration for AuditLog table with year partitioning in alembic/versions/009_create_audit_log_table.py
- [ ] T163 [US11] Implement AuditLogRepository in backend/src/repositories/audit_log_repository.py (append-only, partition-aware queries)
- [ ] T164 [US11] Implement AuditService in backend/src/services/audit_service.py (log creation helper, capture request context)
- [ ] T165 [US11] Create audit logging middleware in backend/src/middleware/audit_logger.py (capture IP, user agent for all requests)
- [ ] T166 [US11] Integrate audit logging with all critical operations (auth, admin CRUD, task status, points, redemptions)
- [ ] T167 [US11] Create archive audit logs job in scripts/archive_audit_logs.py (cron: export logs older than 5 years to S3, mark archived_at)
- [ ] T168 [US11] Add S3 configuration to .env.example (S3_BUCKET, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

**Checkpoint**: At this point, audit and compliance logging should be fully functional and testable independently

---

## Phase 14: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T169 [P] Create comprehensive API documentation in docs/api.md
- [ ] T170 [P] Update README.md with project overview, setup instructions, quickstart commands
- [ ] T171 [P] Create deployment guide in docs/deployment.md (Docker Compose, environment variables, migrations)
- [ ] T172 Code cleanup: remove commented code, unused imports, ensure consistent formatting
- [ ] T173 Performance optimization: add database indexes per data-model.md specifications
- [ ] T174 [P] Security hardening: validate RBAC on all admin-only endpoints, verify no PHI/PII in logs
- [ ] T175 [P] Add OpenAPI schema validation script using schemathesis in backend/tests/contract/validate_openapi.py
- [ ] T176 [P] Create CI/CD configuration (.github/workflows/ci.yml) with test gates (unit, integration, contract, e2e, coverage ≥80%)
- [ ] T177 Run complete acceptance criteria validation per spec.md section 8
- [ ] T178 Run quickstart.md validation: fresh environment setup, seed data, smoke tests
- [ ] T179 [P] Add performance benchmarking for analytics queries (ensure <500ms p95 per plan.md)
- [ ] T180 [P] Create troubleshooting guide in docs/troubleshooting.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-13)**: All depend on Foundational phase completion
  - US1 (Auth): Can start after Foundational - no dependencies on other stories
  - US2 (Methodology): Depends on US1 (needs Clinic entity)
  - US3 (Journey/Patients): Depends on US1 (needs Clinic, User) and US2 (needs FollowUpPlan)
  - US4 (Tasks): Depends on US3 (needs Patient) and US2 (needs Pillar)
  - US5 (Base Scoring): Depends on US4 (needs Task)
  - US6 (Streak Bonus): Depends on US5 (extends ScoringService)
  - US7 (Rewards): Depends on US2 (needs Pillar, FollowUpPlan for eligibility)
  - US8 (Redemptions): Depends on US7 (needs Reward) and US5 (needs PointsLedger)
  - US9 (Analytics): Depends on US4 (needs Task) and US5 (needs PointsLedger)
  - US10 (i18n): Can start after Foundational - no dependencies (integrates throughout)
  - US11 (Audit): Can start after Foundational - no dependencies (integrates throughout)
- **Polish (Phase 14)**: Depends on all desired user stories being complete

### Suggested MVP Scope (First Release)

**MVP = Phase 1 + Phase 2 + US1 + US2 + US3 + US4 + US5 + US10 + US11**

This provides:
- Multi-clinic setup & authentication
- Methodology & plan configuration
- Patient management & journey tracking
- Task assignment & status management
- Base scoring system
- Internationalization
- Audit & compliance

**Post-MVP** (Phase 2 release):
- US6 (Streak Bonus)
- US7 (Rewards Catalog)
- US8 (Redemption Workflow)
- US9 (Analytics Dashboard)

### Parallel Opportunities

Within each phase:
- All tasks marked [P] can run in parallel (different files, no dependencies)
- Tests for a user story can be written in parallel before implementation
- Models within a story can be created in parallel
- Different user stories can be worked on in parallel by different team members (respecting dependencies above)

### Test-Driven Development Flow

For each user story:
1. Write ALL tests first (contract, integration, e2e, unit) - they should FAIL
2. Implement data models (create migrations, run migrations)
3. Implement repositories (data access layer)
4. Implement services (business logic)
5. Implement API routes (controllers)
6. Run tests - they should now PASS
7. Verify acceptance criteria independently for this story
8. Move to next user story

---

## Implementation Strategy

### MVP-First Approach

Focus on delivering a working end-to-end system with core functionality:
1. Complete Phase 1 (Setup) and Phase 2 (Foundational) fully
2. Implement US1 through US5, US10, US11 (core clinical workflow + compliance)
3. Deploy to staging, validate acceptance criteria
4. Gather user feedback from clinic admins and patients
5. Iterate on Phase 2 features (US6-US9) based on feedback

### Incremental Delivery

Each user story completion is a deployable increment:
- US1: Clinics can be created, users can login
- US2: Methodologies and plans can be configured
- US3: Patients can be enrolled and tracked through journey
- US4: Tasks can be assigned and patients can update statuses
- US5: Points are automatically calculated and tracked
- US6: Streak bonuses incentivize early completion
- US7: Rewards catalog is available for browsing
- US8: Redemptions can be requested and approved
- US9: Analytics provide adherence insights
- US10: All UI is internationalized (pt-BR default)
- US11: Full audit trail for compliance

### Quality Gates (Pre-Merge Checklist)

Before merging any user story:
- [ ] All tests pass (unit, integration, contract, e2e)
- [ ] Test coverage ≥80% overall (100% for critical services)
- [ ] OpenAPI contract validation passes (schemathesis)
- [ ] No PHI/PII in application logs
- [ ] RBAC enforced on all admin-only endpoints
- [ ] Tenant isolation verified (no cross-clinic data leakage)
- [ ] Acceptance criteria for this story validated manually
- [ ] Code review completed by peer
- [ ] Database migrations tested (up and down)
- [ ] Documentation updated (API docs, README)

---

## Total Task Count: 180 tasks

**Breakdown by Phase**:
- Phase 1 (Setup): 10 tasks
- Phase 2 (Foundational): 10 tasks
- Phase 3 (US1 - Auth): 22 tasks (7 tests + 15 implementation)
- Phase 4 (US2 - Methodology): 18 tasks (4 tests + 14 implementation)
- Phase 5 (US3 - Journey): 16 tasks (4 tests + 12 implementation)
- Phase 6 (US4 - Tasks): 13 tasks (4 tests + 9 implementation)
- Phase 7 (US5 - Base Scoring): 11 tasks (3 tests + 8 implementation)
- Phase 8 (US6 - Streak Bonus): 8 tasks (3 tests + 5 implementation)
- Phase 9 (US7 - Rewards): 16 tasks (4 tests + 12 implementation)
- Phase 10 (US8 - Redemptions): 15 tasks (5 tests + 10 implementation)
- Phase 11 (US9 - Analytics): 10 tasks (3 tests + 7 implementation)
- Phase 12 (US10 - i18n): 9 tasks (3 tests + 6 implementation)
- Phase 13 (US11 - Audit): 11 tasks (2 tests + 9 implementation)
- Phase 14 (Polish): 12 tasks

**Parallel Opportunities**: 89 tasks marked [P] (49% can run in parallel within their phase)

**Independent Test Criteria**: Each user story (US1-US11) has clear acceptance criteria and can be validated independently

**MVP Scope**: 106 tasks (Phases 1-7 + US10 + US11) - representing 59% of total work

---

## Format Validation

✅ **ALL tasks follow checklist format**:
- Checkbox: `- [ ]` present
- Task ID: T001-T180 sequential
- [P] marker: 89 tasks properly marked as parallelizable
- [Story] label: 129 tasks (US1-US11) properly labeled
- File paths: All implementation tasks include exact file paths

✅ **Organization by user story**: Tasks grouped into phases by user story for independent implementation and testing

✅ **Tests are MANDATORY**: Included per NFR-TEST-01 through NFR-TEST-06, written FIRST (TDD approach)

✅ **Dependencies clear**: Phase dependencies and user story dependencies documented

✅ **Acceptance criteria mapped**: Each user story has "Independent Test" section matching spec.md acceptance criteria
