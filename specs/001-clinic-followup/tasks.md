# Tasks: Multi-Clinic Follow-up Plans, Gamification, and Rewards

**Branch**: `001-Clinic-Followup` | **Date**: 2026-01-17 | **Spec**: [spec.md](./spec.md)  
**Input**: Design documents from `/specs/001-clinic-followup/`

**Tests**: Tests are OPTIONAL - not explicitly requested in specification. No test tasks included per mode instructions.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **Checkbox**: All tasks start with `- [ ]`
- **[ID]**: Sequential task number (T001, T002, ...)
- **[P]**: Task can run in parallel (different files, no blocking dependencies)
- **[Story]**: User story label (US1-US8) - ONLY for user story phases
- **Description**: Clear action with exact file path

## User Story Mapping (from spec.md)

- **US1 (P1)**: Multi-Clinic Setup & Authentication (FR-CLINIC-01, FR-AUTH-01)
- **US2 (P2)**: Methodology & Journey Configuration (FR-METHOD-01, FR-PLAN-01, FR-JOURNEY-01)
- **US3 (P3)**: Task Management & Assignment (FR-TASK-01 through FR-TASK-04)
- **US4 (P4)**: Points & Scoring System (FR-POINTS-01, FR-POINTS-02)
- **US5 (P5)**: Rewards Catalog (FR-REWARD-01)
- **US6 (P6)**: Redemption Workflow (FR-REDEEM-01, FR-REDEEM-02)
- **US7 (P7)**: Analytics Dashboard (FR-ANALYTICS-01)
- **US8 (P8)**: Internationalization & Compliance (FR-I18N-01, FR-COMPLIANCE-01)

## Path Conventions

- **Backend**: `backend/src/`
- **Frontend**: `frontend/src/`
- **Tests**: `backend/tests/`, `frontend/tests/`
- **Resources**: `resources/`
- **Scripts**: `scripts/`
- **Migrations**: `alembic/versions/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directory structure backend/src/{models,repositories,services,api,schemas} and frontend/src/{components,pages,services}
- [X] T002 Initialize Python project with requirements.txt including FastAPI, Streamlit, SQLAlchemy, Pydantic, Alembic, passlib, pytest
- [X] T003 [P] Create Docker Compose configuration in docker-compose.yml with PostgreSQL service
- [X] T004 [P] Create environment configuration in .env.example with DATABASE_URL, APP_LOCALE, SECRET_KEY, SESSION_TIMEOUT_SECONDS, LOG_LEVEL
- [X] T005 [P] Initialize Alembic for database migrations in alembic/ directory
- [X] T006 [P] Configure logging infrastructure in backend/src/config/logging.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 Create base database models in backend/src/models/base.py with Base class and common fields (id, created_at, updated_at)
- [X] T008 Create TenantAwareRepository base class in backend/src/repositories/base.py with clinic_id filtering
- [X] T009 [P] Implement password hashing utilities in backend/src/utils/security.py using passlib with bcrypt
- [X] T010 [P] Create FastAPI application entry point in backend/src/main.py with CORS, middleware setup
- [X] T011 [P] Implement error handling middleware in backend/src/middleware/error_handler.py
- [X] T012 [P] Create Pydantic base schemas in backend/src/schemas/base.py for request/response models
- [ ] T013 Create initial database migration for base tables in alembic/versions/001_initial_schema.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Multi-Clinic Setup & Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable multiple clinics with tenant isolation and secure email/password authentication. Seed Contoso training clinic.

**Independent Test**: Admin can create new clinic, login with credentials, no cross-clinic data leakage.

### Implementation for User Story 1

- [X] T014 [P] [US1] Create Clinic model in backend/src/models/clinic.py with fields: id, name, is_training, analytics_period_days, created_at, updated_at
- [X] T015 [P] [US1] Create User model in backend/src/models/user.py with fields: id, email, password_hash, role, created_at, updated_at
- [X] T016 [P] [US1] Create ClinicMembership model in backend/src/models/clinic_membership.py with fields: id, user_id, clinic_id, joined_at
- [ ] T017 [US1] Create database migration for Clinic, User, ClinicMembership tables in alembic/versions/002_clinic_auth.py
- [ ] T018 [P] [US1] Implement ClinicRepository in backend/src/repositories/clinic_repository.py with create, get, list, update methods
- [ ] T019 [P] [US1] Implement UserRepository in backend/src/repositories/user_repository.py with create, get_by_email, list methods
- [ ] T020 [US1] Implement AuthService in backend/src/services/auth_service.py with login, logout, validate_session, get_current_user methods
- [ ] T021 [US1] Implement ClinicService in backend/src/services/clinic_service.py with create_clinic, get_clinic, list_clinics, set_active_clinic methods
- [ ] T022 [P] [US1] Create auth API router in backend/src/api/v1/auth.py with POST /login, POST /logout, GET /me, POST /set-active-clinic endpoints
- [ ] T023 [P] [US1] Create clinics API router in backend/src/api/v1/clinics.py with GET /clinics, POST /clinics, GET /clinics/{id} endpoints
- [ ] T024 [P] [US1] Create Pydantic schemas in backend/src/schemas/auth.py for LoginRequest, UserSession
- [ ] T025 [P] [US1] Create Pydantic schemas in backend/src/schemas/clinic.py for ClinicCreate, Clinic response models
- [ ] T026 [US1] Implement session management middleware in backend/src/middleware/session.py with cookie-based sessions
- [ ] T027 [US1] Implement authentication dependency in backend/src/dependencies/auth.py for get_current_user, require_admin
- [ ] T028 [US1] Create seed script in scripts/seed_data.py to create Contoso clinic with is_training=true and initial admin user
- [ ] T029 [US1] Create admin UI login page in frontend/src/pages/admin/login.py with email/password form
- [ ] T030 [US1] Create admin UI clinic selector component in frontend/src/components/clinic_selector.py for multi-clinic admins
- [ ] T031 [US1] Create admin UI clinic management page in frontend/src/pages/admin/clinics.py with create clinic form and list view
- [ ] T032 [US1] Create patient UI login page in frontend/src/pages/patient/login.py with email/password form
- [ ] T033 [US1] Implement audit logging for authentication events in backend/src/services/audit_service.py (AUTH_LOGIN_SUCCESS, AUTH_LOGIN_FAILED, AUTH_LOGOUT)

**Checkpoint**: At this point, User Story 1 should be fully functional - admin can create clinics, login, and see tenant isolation

---

## Phase 4: User Story 2 - Methodology & Journey Configuration (Priority: P2)

**Goal**: Enable Clinic Admin to configure Methodologies with Pillars, Follow-up Plans, and ordered Journey Stages.

**Independent Test**: Admin can create complete setup (1 Methodology with ≥3 Pillars, 1 Follow-up Plan, ≥3 Journey Stages) and see in UI.

### Implementation for User Story 2

- [ ] T034 [P] [US2] Create Methodology model in backend/src/models/methodology.py with fields: id, clinic_id, name, description, created_at, updated_at
- [ ] T035 [P] [US2] Create Pillar model in backend/src/models/pillar.py with fields: id, methodology_id, name, description, created_at, updated_at
- [ ] T036 [P] [US2] Create FollowUpPlan model in backend/src/models/follow_up_plan.py with fields: id, clinic_id, methodology_id, name, description, created_at, updated_at
- [ ] T037 [P] [US2] Create PlanPillar model in backend/src/models/plan_pillar.py with fields: id, plan_id, pillar_id
- [ ] T038 [P] [US2] Create JourneyStage model in backend/src/models/journey_stage.py with fields: id, clinic_id, name, order_index, created_at, updated_at
- [ ] T039 [US2] Create database migration for Methodology, Pillar, FollowUpPlan, PlanPillar, JourneyStage tables in alembic/versions/003_methodology_journey.py
- [ ] T040 [P] [US2] Implement MethodologyRepository in backend/src/repositories/methodology_repository.py extending TenantAwareRepository
- [ ] T041 [P] [US2] Implement PillarRepository in backend/src/repositories/pillar_repository.py
- [ ] T042 [P] [US2] Implement FollowUpPlanRepository in backend/src/repositories/follow_up_plan_repository.py extending TenantAwareRepository
- [ ] T043 [P] [US2] Implement JourneyStageRepository in backend/src/repositories/journey_stage_repository.py extending TenantAwareRepository
- [ ] T044 [US2] Implement MethodologyService in backend/src/services/methodology_service.py with create, list, add_pillar methods
- [ ] T045 [US2] Implement FollowUpPlanService in backend/src/services/follow_up_plan_service.py with create, list, link_pillars methods
- [ ] T046 [US2] Implement JourneyStageService in backend/src/services/journey_stage_service.py with create, list, reorder methods
- [ ] T047 [P] [US2] Create methodologies API router in backend/src/api/v1/methodologies.py with GET/POST /methodologies, GET/POST /methodologies/{id}/pillars endpoints
- [ ] T048 [P] [US2] Create plans API router in backend/src/api/v1/plans.py with GET/POST /plans endpoints
- [ ] T049 [P] [US2] Create journey API router in backend/src/api/v1/journey.py with GET/POST /journey-stages endpoints
- [ ] T050 [P] [US2] Create Pydantic schemas in backend/src/schemas/methodology.py for MethodologyCreate, Methodology, PillarCreate, Pillar
- [ ] T051 [P] [US2] Create Pydantic schemas in backend/src/schemas/follow_up_plan.py for FollowUpPlanCreate, FollowUpPlan
- [ ] T052 [P] [US2] Create Pydantic schemas in backend/src/schemas/journey_stage.py for JourneyStageCreate, JourneyStage
- [ ] T053 [US2] Create admin UI methodology management page in frontend/src/pages/admin/methodologies.py with create methodology, add pillars forms
- [ ] T054 [US2] Create admin UI follow-up plan management page in frontend/src/pages/admin/plans.py with create plan, link pillars forms
- [ ] T055 [US2] Create admin UI journey stage management page in frontend/src/pages/admin/journey_stages.py with create stage, reorder stages UI
- [ ] T056 [US2] Implement audit logging for configuration changes in backend/src/services/audit_service.py (ADMIN_METHOD_CREATED, ADMIN_PILLAR_CREATED, ADMIN_PLAN_CREATED, ADMIN_JOURNEY_STAGE_CREATED)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - complete clinic setup flow works

---

## Phase 5: User Story 3 - Task Management & Assignment (Priority: P3)

**Goal**: Enable Clinic Admin to assign tasks to patients with due dates, patients to view and update task statuses, implement soft delete.

**Independent Test**: Admin assigns task to patient, patient views task, changes status to FEITO, status transition recorded and visible.

### Implementation for User Story 3

- [ ] T057 [P] [US3] Create Patient model in backend/src/models/patient.py with fields: id, user_id, clinic_id, full_name, enrollment_date, current_journey_stage_id, created_at, updated_at
- [ ] T058 [P] [US3] Create PatientJourney model in backend/src/models/patient_journey.py with fields: id, patient_id, journey_stage_id, entered_at, exited_at
- [ ] T059 [P] [US3] Create Task model in backend/src/models/task.py with fields: id, patient_id, pillar_id, title, description, status, assigned_at, due_at, completed_at, validated_at, deleted_at, created_at, updated_at
- [ ] T060 [US3] Create database migration for Patient, PatientJourney, Task tables in alembic/versions/004_patients_tasks.py
- [ ] T061 [P] [US3] Implement PatientRepository in backend/src/repositories/patient_repository.py extending TenantAwareRepository
- [ ] T062 [P] [US3] Implement TaskRepository in backend/src/repositories/task_repository.py with soft delete support (deleted_at filter)
- [ ] T063 [US3] Implement PatientService in backend/src/services/patient_service.py with create, list, get, advance_journey methods
- [ ] T064 [US3] Implement TaskService in backend/src/services/task_service.py with assign_task, get_tasks, update_status, validate_status_transition methods
- [ ] T065 [P] [US3] Create patients API router in backend/src/api/v1/patients.py with GET/POST /patients, GET /patients/{id}, POST /patients/{id}/advance-journey endpoints
- [ ] T066 [P] [US3] Create tasks API router in backend/src/api/v1/tasks.py with GET/POST /patients/{id}/tasks, PATCH /patients/{id}/tasks/{task_id}/status endpoints
- [ ] T067 [P] [US3] Create Pydantic schemas in backend/src/schemas/patient.py for PatientCreate, Patient, AdvanceJourneyRequest
- [ ] T068 [P] [US3] Create Pydantic schemas in backend/src/schemas/task.py for TaskAssign, Task, TaskStatusUpdate with status enum validation
- [ ] T069 [US3] Implement task status transition validation in backend/src/services/task_service.py per FR-TASK-03 rules
- [ ] T070 [US3] Create admin UI patient management page in frontend/src/pages/admin/patients.py with patient list, create patient, patient detail views
- [ ] T071 [US3] Create admin UI task assignment page in frontend/src/pages/admin/tasks.py with assign task form, task list with filters (status, due date)
- [ ] T072 [US3] Create admin UI patient journey management in frontend/src/pages/admin/patient_detail.py with advance journey stage action
- [ ] T073 [US3] Create patient UI task list page in frontend/src/pages/patient/tasks.py with task cards, status filter, due date sorting
- [ ] T074 [US3] Create patient UI task detail page in frontend/src/pages/patient/task_detail.py with status update dropdown, transition validation
- [ ] T075 [US3] Implement soft delete for cancelled tasks in backend/src/services/task_service.py setting deleted_at timestamp
- [ ] T076 [US3] Update TaskRepository queries to default filter deleted_at IS NULL with include_deleted flag option
- [ ] T077 [US3] Implement audit logging for task events in backend/src/services/audit_service.py (ADMIN_TASK_ASSIGNED, PATIENT_TASK_STATUS_CHANGED)

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently - full task workflow functional

---

## Phase 6: User Story 4 - Points & Scoring System (Priority: P4)

**Goal**: Implement deterministic scoring with base points (delay/pause deductions) and clinic-validated streak bonuses with chain increments.

**Independent Test**: Patient completes task before due date, receives 100 base points immediately. Admin validates, streak bonus (10+2*chain_position) added to ledger.

### Implementation for User Story 4

- [ ] T078 [P] [US4] Create PointsLedger model in backend/src/models/points_ledger.py with fields: id, patient_id, task_id, event_type, points_delta, balance_after, metadata (JSONB), created_at
- [ ] T079 [US4] Create database migration for PointsLedger table in alembic/versions/005_points_ledger.py
- [ ] T080 [P] [US4] Implement PointsLedgerRepository in backend/src/repositories/points_ledger_repository.py with append-only constraint enforcement
- [ ] T081 [US4] Implement ScoringService in backend/src/services/scoring_service.py with compute_base_points (FR-POINTS-01 deduction rules) method
- [ ] T082 [US4] Implement streak bonus computation in backend/src/services/scoring_service.py with compute_streak_bonus method (10 + chain_position * 2, same-day = 1 link)
- [ ] T083 [US4] Implement LedgerService in backend/src/services/ledger_service.py with add_entry, get_balance, get_history methods
- [ ] T084 [US4] Integrate base points calculation in TaskService.update_status when transitioning to FEITO status
- [ ] T085 [US4] Create scoring API router in backend/src/api/v1/scoring.py with POST /patients/{id}/tasks/{task_id}/validate endpoint (admin-only)
- [ ] T086 [US4] Implement validate_completion action in TaskService that triggers streak bonus calculation and ledger entry
- [ ] T087 [P] [US4] Create Pydantic schemas in backend/src/schemas/scoring.py for PointsLedgerEntry, PointsBalance
- [ ] T088 [US4] Create admin UI validation page in frontend/src/pages/admin/validations.py with pending validation list, validate action button
- [ ] T089 [US4] Create patient UI points page in frontend/src/pages/patient/points.py with current balance, ledger history table (read-only)
- [ ] T090 [US4] Implement audit logging for scoring events in backend/src/services/audit_service.py (SYSTEM_POINTS_AWARDED, ADMIN_TASK_VALIDATED)
- [ ] T091 [US4] Add unit test helper in backend/tests/unit/test_scoring_service.py for 5 consecutive completions example (bonuses: 10, 12, 14, 16, 18)
- [ ] T092 [US4] Add unit test helper in backend/tests/unit/test_scoring_service.py for broken chain example (bonuses: 10, 10, 10, 12, 10)

**Checkpoint**: At this point, User Stories 1-4 should all work independently - complete scoring flow functional

---

## Phase 7: User Story 5 - Rewards Catalog (Priority: P5)

**Goal**: Enable Clinic Admin to create Vendors and Rewards with eligibility rules. Patients browse rewards showing points_cost only (no monetary_value).

**Independent Test**: Admin creates reward with eligible_plan_id, patient enrolled in that plan sees reward, patient not enrolled does not see it.

### Implementation for User Story 5

- [ ] T093 [P] [US5] Create Vendor model in backend/src/models/vendor.py with fields: id, clinic_id, name, contact_info, created_at, updated_at
- [ ] T094 [P] [US5] Create Reward model in backend/src/models/reward.py with fields: id, vendor_id, clinic_id, name, description, points_cost, monetary_value, quantity_available, expires_at, eligible_plan_id, eligible_pillar_id, is_active, created_at, updated_at
- [ ] T095 [US5] Create database migration for Vendor, Reward tables in alembic/versions/006_vendors_rewards.py
- [ ] T096 [P] [US5] Implement VendorRepository in backend/src/repositories/vendor_repository.py extending TenantAwareRepository
- [ ] T097 [P] [US5] Implement RewardRepository in backend/src/repositories/reward_repository.py extending TenantAwareRepository
- [ ] T098 [US5] Implement VendorService in backend/src/services/vendor_service.py with create, list, update methods
- [ ] T099 [US5] Implement RewardService in backend/src/services/reward_service.py with create, list, update, check_eligibility methods
- [ ] T100 [US5] Implement eligibility evaluation logic in RewardService.check_eligibility per FR-REWARD-01 (AND logic for plan + pillar if both set)
- [ ] T101 [P] [US5] Create vendors API router in backend/src/api/v1/vendors.py with GET/POST /vendors endpoints (admin-only)
- [ ] T102 [P] [US5] Create rewards API router in backend/src/api/v1/rewards.py with GET/POST /rewards (admin), GET /rewards/eligible (patient) endpoints
- [ ] T103 [P] [US5] Create Pydantic schemas in backend/src/schemas/vendor.py for VendorCreate, Vendor
- [ ] T104 [P] [US5] Create Pydantic schemas in backend/src/schemas/reward.py for RewardCreate, Reward (admin view with monetary_value), RewardPatient (patient view points_cost only)
- [ ] T105 [US5] Create admin UI vendor management page in frontend/src/pages/admin/vendors.py with vendor list, create vendor form
- [ ] T106 [US5] Create admin UI reward management page in frontend/src/pages/admin/rewards.py with reward list, create reward form with eligibility dropdowns, monetary_value field
- [ ] T107 [US5] Create patient UI rewards catalog page in frontend/src/pages/patient/rewards.py with reward cards showing points_cost, quantity, expiry (NO monetary_value)
- [ ] T108 [US5] Implement reward eligibility filtering in patient rewards view using RewardService.check_eligibility
- [ ] T109 [US5] Implement audit logging for reward events in backend/src/services/audit_service.py (ADMIN_VENDOR_CREATED, ADMIN_REWARD_CREATED, ADMIN_REWARD_UPDATED)

**Checkpoint**: At this point, User Stories 1-5 should all work independently - rewards catalog functional with eligibility

---

## Phase 8: User Story 6 - Redemption Workflow (Priority: P6)

**Goal**: Enable patients to request redemptions with eligibility snapshot, admins to approve/reject, automatic expiration after 30 days, points reserve/refund.

**Independent Test**: Patient with 500 points requests 200-point reward, balance immediately becomes 300. Admin approves. If not redeemed in 30 days, auto-expires and refunds 200 points.

### Implementation for User Story 6

- [ ] T110 [P] [US6] Create Redemption model in backend/src/models/redemption.py with fields: id, patient_id, reward_id, status, points_cost, eligibility_snapshot (JSONB), requested_at, approved_at, rejected_at, redeemed_at, expired_at, cancelled_at, admin_notes, created_at, updated_at
- [ ] T111 [US6] Create database migration for Redemption table in alembic/versions/007_redemptions.py
- [ ] T112 [P] [US6] Implement RedemptionRepository in backend/src/repositories/redemption_repository.py
- [ ] T113 [US6] Implement RedemptionService in backend/src/services/redemption_service.py with request_redemption, approve, reject, redeem, cancel, auto_expire methods
- [ ] T114 [US6] Implement eligibility snapshot logic in RedemptionService.request_redemption capturing patient plan, pillar completions per FR-REDEEM-01
- [ ] T115 [US6] Implement insufficient points check in RedemptionService.request_redemption blocking request if balance < points_cost with clear error message
- [ ] T116 [US6] Implement points reserve on request in RedemptionService.request_redemption via LedgerService.add_entry with event_type=REDEMPTION_RESERVED
- [ ] T117 [US6] Implement points refund logic in RedemptionService for rejected/cancelled/expired redemptions via LedgerService.add_entry with event_type=REDEMPTION_REFUNDED
- [ ] T118 [P] [US6] Create redemptions API router in backend/src/api/v1/redemptions.py with POST /redemptions (patient), PATCH /redemptions/{id}/approve (admin), PATCH /redemptions/{id}/reject (admin) endpoints
- [ ] T119 [P] [US6] Create Pydantic schemas in backend/src/schemas/redemption.py for RedemptionRequest, Redemption, RedemptionApprove, RedemptionReject
- [ ] T120 [US6] Create patient UI redemption request page in frontend/src/pages/patient/redemptions.py with request button, redemption history, status display
- [ ] T121 [US6] Create admin UI redemption management page in frontend/src/pages/admin/redemptions.py with pending list, approve/reject actions, admin notes field
- [ ] T122 [US6] Create scheduled job script in scripts/expire_redemptions.py to auto-expire APPROVED redemptions older than 30 days (status=EXPIRED) and refund points
- [ ] T123 [US6] Add cron configuration or task scheduler setup for scripts/expire_redemptions.py to run daily
- [ ] T124 [US6] Implement audit logging for redemption events in backend/src/services/audit_service.py (PATIENT_REDEMPTION_REQUESTED, ADMIN_REDEMPTION_APPROVED, ADMIN_REDEMPTION_REJECTED, SYSTEM_REDEMPTION_EXPIRED, PATIENT_REDEMPTION_CANCELLED)

**Checkpoint**: At this point, User Stories 1-6 should all work independently - complete redemption workflow functional

---

## Phase 9: User Story 7 - Analytics Dashboard (Priority: P7)

**Goal**: Provide admin analytics for adherence segmentation with quartiles over configurable period (7-90 days), hybrid real-time + batch aggregation.

**Independent Test**: Admin views analytics dashboard showing patients grouped in quartiles by total points accumulated in last 30 days (configurable).

### Implementation for User Story 7

- [ ] T125 [P] [US7] Create AnalyticsSnapshot model in backend/src/models/analytics_snapshot.py with fields: id, clinic_id, patient_id, snapshot_date, total_points, streak_points, tasks_completed, tasks_delayed, tasks_paused, tasks_cancelled, created_at
- [ ] T126 [US7] Create database migration for AnalyticsSnapshot table in alembic/versions/008_analytics_snapshots.py
- [ ] T127 [P] [US7] Implement AnalyticsRepository in backend/src/repositories/analytics_repository.py with get_snapshots, get_current_day_metrics methods
- [ ] T128 [US7] Implement AnalyticsService in backend/src/services/analytics_service.py with compute_quartiles, get_adherence_metrics, aggregate_daily methods
- [ ] T129 [US7] Implement hybrid aggregation logic in AnalyticsService combining historical snapshots with real-time current day queries
- [ ] T130 [US7] Implement quartile computation in AnalyticsService.compute_quartiles sorting patients by total points and dividing into 4 equal groups
- [ ] T131 [US7] Create scheduled job script in scripts/aggregate_analytics.py to run daily at midnight computing previous day metrics and storing in AnalyticsSnapshot
- [ ] T132 [US7] Add cron configuration or task scheduler setup for scripts/aggregate_analytics.py
- [ ] T133 [P] [US7] Create analytics API router in backend/src/api/v1/analytics.py with GET /analytics/adherence endpoint (admin-only)
- [ ] T134 [P] [US7] Create Pydantic schemas in backend/src/schemas/analytics.py for AdherenceMetrics, QuartileSegmentation
- [ ] T135 [US7] Create admin UI analytics dashboard page in frontend/src/pages/admin/analytics.py with quartile visualization, adherence metrics tables
- [ ] T136 [US7] Add analytics period configuration UI in admin clinic settings page to set analytics_period_days (7-90 days range validation)

**Checkpoint**: At this point, User Stories 1-7 should all work independently - analytics dashboard functional

---

## Phase 10: User Story 8 - Internationalization & Compliance (Priority: P8)

**Goal**: Implement i18n with pt-BR default using label packs, no hardcoded UI strings. Implement LGPD audit logging with 5-year retention policy.

**Independent Test**: All UI text loaded from resources/labels/pt-BR.json, can switch to en-US with fallback. All critical events logged to audit_logs with timestamps.

### Implementation for User Story 8

- [ ] T137 [P] [US8] Create AuditLog model in backend/src/models/audit_log.py with fields: id, clinic_id, user_id, event_type, entity_type, entity_id, event_data (JSONB), ip_address, user_agent, created_at, archived_at
- [ ] T138 [US8] Create database migration for AuditLog table in alembic/versions/009_audit_logs.py with table partitioning by year
- [ ] T139 [P] [US8] Implement AuditLogRepository in backend/src/repositories/audit_log_repository.py with append-only constraint
- [ ] T140 [US8] Complete AuditService implementation in backend/src/services/audit_service.py with log_event method for all event types
- [ ] T141 [US8] Integrate audit logging calls in all services for critical events (auth, config changes, task status, scoring, redemptions)
- [ ] T142 [US8] Create resources/labels/ directory structure
- [ ] T143 [P] [US8] Create pt-BR label pack in resources/labels/pt-BR.json with all UI strings for admin and patient UIs
- [ ] T144 [P] [US8] Create en-US label pack skeleton in resources/labels/en-US.json for future use
- [ ] T145 [US8] Implement LabelService in backend/src/services/label_service.py with load_labels, t(key, **kwargs) interpolation, missing key fallback to pt-BR with warning log
- [ ] T146 [US8] Update environment configuration to read APP_LOCALE from .env (default: pt-BR)
- [ ] T147 [US8] Replace all hardcoded UI strings in admin Streamlit pages with label service calls t() function
- [ ] T148 [US8] Replace all hardcoded UI strings in patient Streamlit pages with label service calls t() function
- [ ] T149 [US8] Create audit log retention policy script in scripts/archive_audit_logs.py to export logs older than 5 years to S3 Glacier and mark as archived
- [ ] T150 [US8] Add cron configuration for scripts/archive_audit_logs.py to run monthly
- [ ] T151 [US8] Create hardcoded string checker script in scripts/check_hardcoded_strings.py to grep for potential hardcoded UI strings (best-effort regex)
- [ ] T152 [US8] Add lint gate to run scripts/check_hardcoded_strings.py and warn if hardcoded strings found

**Checkpoint**: At this point, all User Stories 1-8 are complete - full feature set functional with i18n and compliance

---

## Phase 11: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final validation

- [ ] T153 [P] Update README.md with project overview, setup instructions, and quickstart reference
- [ ] T154 [P] Update .github/copilot-instructions.md adding Backend section (FastAPI, SQLAlchemy, Alembic, pytest) and Frontend section (Streamlit for admin/patient UIs)
- [ ] T155 [P] Create comprehensive quickstart validation script in scripts/validate_quickstart.py to automate acceptance criteria testing
- [ ] T156 [P] Add API documentation comments to all FastAPI routers for OpenAPI docs
- [ ] T157 Code review and refactoring for consistent error handling across all services
- [ ] T158 Code review and refactoring for consistent logging patterns across all modules
- [ ] T159 [P] Performance optimization for tenant-aware queries with proper indexes
- [ ] T160 [P] Security hardening review of authentication, authorization, and session management
- [ ] T161 Run full quickstart.md validation manually covering all 8 acceptance criteria
- [ ] T162 Final smoke test: create clinic, setup methodology, assign tasks, score points, redeem rewards end-to-end
- [ ] T163 [P] Run contract validation using schemathesis against /api/docs/openapi.json and compare with specs/001-clinic-followup/contracts/openapi.yaml

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup (Phase 1) completion - BLOCKS all user stories
- **User Stories (Phase 3-10)**: All depend on Foundational (Phase 2) completion
  - User stories can proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5 → P6 → P7 → P8)
- **Polish (Phase 11)**: Depends on all desired user stories being complete

### User Story Dependencies

- **US1 (P1)**: Multi-Clinic Setup & Authentication - No dependencies on other stories
- **US2 (P2)**: Methodology & Journey Configuration - No dependencies on other stories
- **US3 (P3)**: Task Management - Requires US1 (Patient model depends on Clinic), US2 (Task requires Pillar, Journey)
- **US4 (P4)**: Points & Scoring - Requires US3 (scoring operates on Tasks)
- **US5 (P5)**: Rewards Catalog - Requires US2 (reward eligibility depends on Plan, Pillar)
- **US6 (P6)**: Redemption Workflow - Requires US4 (redemptions consume points), US5 (redemptions reference Rewards)
- **US7 (P7)**: Analytics Dashboard - Requires US3, US4 (analytics aggregates task and points data)
- **US8 (P8)**: Internationalization & Compliance - Can start in parallel with any story, integrated throughout

### Within Each User Story

1. Models before repositories
2. Repositories before services
3. Services before API routers
4. API routers before UI pages
5. Core implementation before audit logging integration

### Parallel Opportunities

- **Setup (Phase 1)**: Tasks T002-T006 can run in parallel
- **Foundational (Phase 2)**: Tasks T009-T012 can run in parallel
- **Within each user story**: Tasks marked [P] can run in parallel (e.g., US1: T014-T016, T018-T019, T022-T025, T029-T032)
- **Across user stories**: After Phase 2, US1, US2, and US8 (i18n infrastructure) can all start in parallel. US3 must wait for US1+US2. US4 must wait for US3. US5 can start after US2. US6 must wait for US4+US5. US7 must wait for US3+US4.

### Suggested MVP Scope

**MVP = User Story 1 + User Story 2 + User Story 3 (Phases 1-5)**

This delivers:
- ✅ Multi-clinic setup with authentication
- ✅ Methodology, plan, journey configuration
- ✅ Task assignment and status workflow
- ✅ Tenant isolation and audit basics

**Remaining stories can be delivered incrementally:**
- **Increment 2**: Add US4 (Points & Scoring)
- **Increment 3**: Add US5 + US6 (Rewards & Redemptions)
- **Increment 4**: Add US7 (Analytics)
- **Increment 5**: Complete US8 (i18n & Compliance polish)

---

## Parallel Example: User Story 1 (Multi-Clinic Setup & Authentication)

After completing Foundational phase, these US1 tasks can run in parallel:

**Batch 1 - Models** (parallel):
```bash
git checkout -b feature/us1-models
# Work on T014, T015, T016 simultaneously (different files)
```

**Batch 2 - Repositories** (parallel, after Batch 1):
```bash
git checkout -b feature/us1-repositories
# Work on T018, T019 simultaneously (different files)
```

**Batch 3 - API + Schemas** (parallel, after services):
```bash
git checkout -b feature/us1-api
# Work on T022, T023, T024, T025 simultaneously (different files)
```

**Batch 4 - UI Pages** (parallel, after API):
```bash
git checkout -b feature/us1-ui
# Work on T029, T030, T031, T032 simultaneously (different files)
```

---

## Implementation Strategy

**MVP-First Approach**: Deliver US1 + US2 + US3 first for working task management system, then add scoring, rewards, analytics incrementally.

**Independent Testing**: Each user story phase includes independent test criteria. Checkpoint after each story to verify it works standalone before integration.

**Incremental Delivery**: Each user story represents a shippable increment. Product owner can decide to release after any story completion.

**Parallel Execution**: Within phases and across independent user stories, tasks marked [P] can be parallelized across team members for faster delivery.

---

**Total Tasks**: 163  
**MVP Tasks (Phases 1-5)**: 77 (US1-US3)  
**Parallel Tasks Identified**: 69 tasks marked [P]  
**User Stories**: 8 (US1-US8)  
**Phases**: 11 (1 Setup + 1 Foundational + 8 User Stories + 1 Polish)
