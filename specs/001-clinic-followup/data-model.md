# Data Model: Multi-Clinic Follow-up System

**Feature**: 001-clinic-followup  
**Date**: 2026-01-17  
**Status**: Phase 1 Complete

## Overview
This document defines the relational data model for the multi-tenant clinic follow-up system. All entities enforce tenant isolation via `clinic_id` foreign keys where applicable.

---

## Entity Relationship Diagram (ERD)

```
┌─────────────┐       ┌──────────────┐       ┌─────────────┐
│   Clinic    │◄──────│  Methodology │◄──────│   Pillar    │
└─────────────┘   1:N └──────────────┘   1:N └─────────────┘
      ▲                      ▲                       ▲
      │                      │                       │
      │ 1:N                  │ N:M                   │ N:M
      │                      │                       │
┌─────────────┐       ┌──────────────┐       ┌─────────────┐
│    User     │       │ FollowUpPlan │       │  PlanPillar │
│ (Clinic)    │       │              │◄──────┤  (join)     │
└─────────────┘       └──────────────┘       └─────────────┘
      ▲                      ▲
      │ 1:N                  │ 1:N
      │                      │
┌─────────────┐       ┌──────────────┐       ┌─────────────┐
│   Patient   │       │JourneyStage  │       │    Task     │
│             │◄──────┤              │       │             │
└─────────────┘   1:N └──────────────┘       └─────────────┘
      ▲                      ▲                       ▲
      │ 1:N                  │ 1:1                   │ N:1
      │                      │                       │
┌─────────────┐       ┌──────────────┐       ┌─────────────┐
│PointsLedger│       │PatientJourney│       │   Vendor    │
│             │       │              │       │             │
└─────────────┘       └──────────────┘       └─────────────┘
      ▲                                             ▲
      │ 1:N                                         │ 1:N
      │                                             │
┌─────────────┐       ┌──────────────┐       ┌─────────────┐
│ Redemption  │◄──────│    Reward    │       │  AuditLog   │
│             │   N:1 │              │       │             │
└─────────────┘       └──────────────┘       └─────────────┘
```

---

## Core Entities

### 1. Clinic

Represents a medical clinic (tenant). Multi-clinic support (FR-CLINIC-01).

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PK | Unique clinic identifier |
| `name` | VARCHAR(255) | NOT NULL, UNIQUE | Clinic name (e.g., "Contoso") |
| `is_training` | BOOLEAN | NOT NULL, DEFAULT FALSE | True for training/demo clinics |
| `analytics_period_days` | INTEGER | NOT NULL, DEFAULT 30, CHECK >= 7 AND <= 90 | Configurable analytics period (FR-ANALYTICS-01) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Record creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Record last update timestamp |

**Indexes**:
- PRIMARY KEY (`id`)
- UNIQUE (`name`)

**Seed Data**: "Contoso" with `is_training=true`

---

### 2. User

Represents authenticated users (Clinic Admins and Patients). Users authenticate via email + password (FR-AUTH-01).

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PK | Unique user identifier |
| `email` | VARCHAR(320) | NOT NULL, UNIQUE | User email (login identifier) |
| `password_hash` | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| `role` | VARCHAR(50) | NOT NULL, CHECK IN ('ADMIN', 'PATIENT') | User role |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Record creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Record last update timestamp |

**Indexes**:
- PRIMARY KEY (`id`)
- UNIQUE (`email`)
- INDEX (`role`)

**Relationships**:
- Admin users: N:M with Clinic via `ClinicMembership`
- Patient users: 1:1 with Patient entity

---

### 3. ClinicMembership

Join table for Admin users with multiple clinic memberships.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PK | Unique membership identifier |
| `user_id` | UUID | FK → User, NOT NULL | Admin user |
| `clinic_id` | UUID | FK → Clinic, NOT NULL | Clinic |
| `joined_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Membership start date |

**Indexes**:
- PRIMARY KEY (`id`)
- UNIQUE (`user_id`, `clinic_id`)
- INDEX (`clinic_id`)

---

### 4. Patient

Represents a patient enrolled in a clinic. Patients belong to exactly one clinic (tenant-scoped).

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PK | Unique patient identifier |
| `user_id` | UUID | FK → User, NOT NULL, UNIQUE | Associated user account |
| `clinic_id` | UUID | FK → Clinic, NOT NULL | Owning clinic (tenant isolation) |
| `full_name` | VARCHAR(255) | NOT NULL | Patient full name |
| `enrollment_date` | DATE | NOT NULL | Date patient enrolled in clinic |
| `current_journey_stage_id` | UUID | FK → JourneyStage, NULL | Current position in journey |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Record creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Record last update timestamp |

**Indexes**:
- PRIMARY KEY (`id`)
- UNIQUE (`user_id`)
- INDEX (`clinic_id`, `current_journey_stage_id`)
- CHECK (`clinic_id IS NOT NULL`)

---

### 5. Methodology

Clinic-defined treatment/follow-up methodology (e.g., "Diabetes Care", "Cardiac Rehab").

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PK | Unique methodology identifier |
| `clinic_id` | UUID | FK → Clinic, NOT NULL | Owning clinic |
| `name` | VARCHAR(255) | NOT NULL | Methodology name |
| `description` | TEXT | NULL | Methodology description |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Record creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Record last update timestamp |

**Indexes**:
- PRIMARY KEY (`id`)
- INDEX (`clinic_id`)
- UNIQUE (`clinic_id`, `name`)

---

### 6. Pillar

Represents a pillar within a methodology (e.g., "Nutrition", "Exercise", "Medication Adherence").

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PK | Unique pillar identifier |
| `methodology_id` | UUID | FK → Methodology, NOT NULL | Parent methodology |
| `name` | VARCHAR(255) | NOT NULL | Pillar name |
| `description` | TEXT | NULL | Pillar description |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Record creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Record last update timestamp |

**Indexes**:
- PRIMARY KEY (`id`)
- INDEX (`methodology_id`)
- UNIQUE (`methodology_id`, `name`)

**Tenant Isolation**: Inherited from `methodology_id → clinic_id`

---

### 7. FollowUpPlan

Clinic-defined follow-up plan linking a methodology to selected pillars.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PK | Unique plan identifier |
| `clinic_id` | UUID | FK → Clinic, NOT NULL | Owning clinic |
| `methodology_id` | UUID | FK → Methodology, NOT NULL | Linked methodology |
| `name` | VARCHAR(255) | NOT NULL | Plan name |
| `description` | TEXT | NULL | Plan description |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Record creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Record last update timestamp |

**Indexes**:
- PRIMARY KEY (`id`)
- INDEX (`clinic_id`, `methodology_id`)
- UNIQUE (`clinic_id`, `name`)

**Relationships**: N:M with Pillar via `PlanPillar`

---

### 8. PlanPillar

Join table for FollowUpPlan ↔ Pillar (many-to-many).

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `plan_id` | UUID | FK → FollowUpPlan, NOT NULL | Plan |
| `pillar_id` | UUID | FK → Pillar, NOT NULL | Pillar |

**Indexes**:
- PRIMARY KEY (`id`)
- UNIQUE (`plan_id`, `pillar_id`)
- INDEX (`pillar_id`)

---

### 9. JourneyStage

Ordered stages in a patient's journey (e.g., "Lead", "Onboarding", "Active Follow-up", "Close").

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PK | Unique stage identifier |
| `clinic_id` | UUID | FK → Clinic, NOT NULL | Owning clinic |
| `name` | VARCHAR(255) | NOT NULL | Stage name |
| `order_index` | INTEGER | NOT NULL | Display order (0, 1, 2, ...) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Record creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Record last update timestamp |

**Indexes**:
- PRIMARY KEY (`id`)
- INDEX (`clinic_id`, `order_index`)
- UNIQUE (`clinic_id`, `name`)
- UNIQUE (`clinic_id`, `order_index`)

---

### 10. PatientJourney

Tracks patient progression through journey stages (audit log of stage transitions).

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PK | Unique journey entry identifier |
| `patient_id` | UUID | FK → Patient, NOT NULL | Patient |
| `journey_stage_id` | UUID | FK → JourneyStage, NOT NULL | Stage entered |
| `entered_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Stage entry timestamp |
| `exited_at` | TIMESTAMP | NULL | Stage exit timestamp (NULL if current) |

**Indexes**:
- PRIMARY KEY (`id`)
- INDEX (`patient_id`, `entered_at`)
- INDEX (`journey_stage_id`)

**Notes**: Current stage is the row with `exited_at IS NULL`

---

## Task & Scoring Entities

### 11. Task

Represents a task assigned to a patient by a Clinic Admin (FR-TASK-01).

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PK | Unique task identifier |
| `patient_id` | UUID | FK → Patient, NOT NULL | Assigned patient |
| `pillar_id` | UUID | FK → Pillar, NOT NULL | Associated pillar |
| `title` | VARCHAR(500) | NOT NULL | Task title (i18n label key or direct text) |
| `description` | TEXT | NULL | Task description |
| `status` | VARCHAR(50) | NOT NULL, CHECK IN (statuses) | Current task status (see below) |
| `assigned_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Task assignment timestamp |
| `due_at` | TIMESTAMP | NOT NULL | Task deadline |
| `completed_at` | TIMESTAMP | NULL | Task completion timestamp (when status → FEITO) |
| `validated_at` | TIMESTAMP | NULL | Admin validation timestamp (unlocks streak bonus) |
| `deleted_at` | TIMESTAMP | NULL | Soft delete timestamp (FR-TASK-04) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Record creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Record last update timestamp |

**Task Statuses** (FR-TASK-02):
- `A_FAZER`, `FEITO`, `EM_ATRASO`, `PAUSADO`, `RETOMADO`, `CANCELADO_PELO_PACIENTE`, `CANCELADO_PELA_CLINICA`

**Status Transitions** (FR-TASK-03):
- `A_FAZER` → `FEITO` | `EM_ATRASO` | `PAUSADO` | `CANCELADO_PELO_PACIENTE` | `CANCELADO_PELA_CLINICA`
- `EM_ATRASO` → `FEITO` | `PAUSADO` | `CANCELADO_PELO_PACIENTE` | `CANCELADO_PELA_CLINICA`
- `PAUSADO` → `RETOMADO` | `CANCELADO_PELO_PACIENTE` | `CANCELADO_PELA_CLINICA`
- `RETOMADO` → `FEITO` | `EM_ATRASO` | `PAUSADO` | `CANCELADO_PELO_PACIENTE` | `CANCELADO_PELA_CLINICA`
- Terminal states: `FEITO`, `CANCELADO_*`

**Indexes**:
- PRIMARY KEY (`id`)
- INDEX (`patient_id`, `status`, `deleted_at`)
- INDEX (`pillar_id`)
- INDEX (`due_at`)

**Tenant Isolation**: Inherited from `patient_id → clinic_id`

**Validation Rules**:
- `completed_at` set when status transitions to `FEITO`
- `validated_at` set by admin action (separate from status transition)
- `deleted_at` set when status is `CANCELADO_*` (soft delete)

---

### 12. PointsLedger

Immutable log of all points awarded/deducted. All points transactions flow through this ledger (FR-POINTS-01, FR-POINTS-02).

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PK | Unique ledger entry identifier |
| `patient_id` | UUID | FK → Patient, NOT NULL | Patient earning/losing points |
| `task_id` | UUID | FK → Task, NULL | Associated task (NULL for non-task events like refunds) |
| `event_type` | VARCHAR(50) | NOT NULL, CHECK IN (types) | Event type (see below) |
| `points_delta` | INTEGER | NOT NULL | Points change (positive or negative) |
| `balance_after` | INTEGER | NOT NULL | Patient's balance after this entry |
| `metadata` | JSONB | NULL | Event-specific metadata (e.g., streak chain position) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Ledger entry timestamp (immutable) |

**Event Types**:
- `BASE_POINTS_AWARDED`: Base task points (FR-POINTS-01)
- `BASE_POINTS_DEDUCTED`: Deduction for delay/pause/reopen
- `STREAK_BONUS_AWARDED`: Clinic-validated streak bonus (FR-POINTS-02)
- `REDEMPTION_RESERVED`: Points deducted for redemption request
- `REDEMPTION_REFUNDED`: Points returned on rejection/expiry/cancellation

**Indexes**:
- PRIMARY KEY (`id`)
- INDEX (`patient_id`, `created_at DESC`)
- INDEX (`task_id`)

**Metadata Examples**:
```json
{
  "streak_chain_position": 2,
  "streak_bonus_tier": 14,
  "completion_date": "2026-01-15"
}
```

**Validation Rules**:
- Ledger is append-only (no updates/deletes)
- `balance_after` computed as: previous balance + `points_delta`
- Must maintain referential integrity (patient exists)

---

## Rewards & Redemptions Entities

### 13. Vendor

Represents a rewards vendor (e.g., "Amazon", "Local Pharmacy").

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PK | Unique vendor identifier |
| `clinic_id` | UUID | FK → Clinic, NOT NULL | Owning clinic |
| `name` | VARCHAR(255) | NOT NULL | Vendor name |
| `contact_info` | TEXT | NULL | Vendor contact details |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Record creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Record last update timestamp |

**Indexes**:
- PRIMARY KEY (`id`)
- INDEX (`clinic_id`)
- UNIQUE (`clinic_id`, `name`)

---

### 14. Reward

Represents a reward available for redemption.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PK | Unique reward identifier |
| `vendor_id` | UUID | FK → Vendor, NOT NULL | Vendor offering reward |
| `clinic_id` | UUID | FK → Clinic, NOT NULL | Owning clinic (denormalized for query perf) |
| `name` | VARCHAR(255) | NOT NULL | Reward name (patient-visible) |
| `description` | TEXT | NULL | Reward description |
| `points_cost` | INTEGER | NOT NULL, CHECK > 0 | Points required (patient-visible) |
| `monetary_value` | DECIMAL(10,2) | NOT NULL, CHECK >= 0 | Monetary value (admin-only, NOT shown to patients) |
| `quantity_available` | INTEGER | NOT NULL, CHECK >= 0 | Remaining quantity (limited stock) |
| `expires_at` | TIMESTAMP | NULL | Reward expiration date |
| `eligible_plan_id` | UUID | FK → FollowUpPlan, NULL | Optional: require patient enrolled in this plan |
| `eligible_pillar_id` | UUID | FK → Pillar, NULL | Optional: require patient completed ≥1 task in this pillar |
| `is_active` | BOOLEAN | NOT NULL, DEFAULT TRUE | Admin can disable reward |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Record creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Record last update timestamp |

**Eligibility Rules** (FR-REWARD-01):
- If `eligible_plan_id` is set: patient must be enrolled in that plan
- If `eligible_pillar_id` is set: patient must have completed ≥1 task in that pillar
- If both are set: **both conditions must be met** (AND logic)
- If neither is set: reward available to all patients in clinic

**Indexes**:
- PRIMARY KEY (`id`)
- INDEX (`clinic_id`, `is_active`, `expires_at`)
- INDEX (`vendor_id`)
- INDEX (`eligible_plan_id`)
- INDEX (`eligible_pillar_id`)

---

### 15. Redemption

Represents a patient's reward redemption request/approval flow.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PK | Unique redemption identifier |
| `patient_id` | UUID | FK → Patient, NOT NULL | Patient requesting redemption |
| `reward_id` | UUID | FK → Reward, NOT NULL | Reward being redeemed |
| `status` | VARCHAR(50) | NOT NULL, CHECK IN (statuses) | Redemption status (see below) |
| `points_cost` | INTEGER | NOT NULL | Points cost at request time (snapshot) |
| `eligibility_snapshot` | JSONB | NOT NULL | Eligibility criteria snapshot (FR-REDEEM-01) |
| `requested_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Request timestamp |
| `approved_at` | TIMESTAMP | NULL | Admin approval timestamp |
| `rejected_at` | TIMESTAMP | NULL | Admin rejection timestamp |
| `redeemed_at` | TIMESTAMP | NULL | Redemption fulfillment timestamp |
| `expired_at` | TIMESTAMP | NULL | Auto-expiration timestamp (FR-REDEEM-02) |
| `cancelled_at` | TIMESTAMP | NULL | Cancellation timestamp |
| `admin_notes` | TEXT | NULL | Admin notes (rejection reason, etc.) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Record creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Record last update timestamp |

**Redemption Statuses** (FR-REDEEM-01):
- `REQUESTED`: Patient requested, awaiting admin approval
- `APPROVED`: Admin approved, awaiting fulfillment
- `REJECTED`: Admin rejected
- `REDEEMED`: Fulfilled by clinic
- `CANCELLED_BY_PATIENT`: Patient cancelled request
- `CANCELLED_BY_CLINIC`: Clinic cancelled
- `EXPIRED`: Auto-expired (approved but not redeemed within 30 days)

**Eligibility Snapshot** (FR-REDEEM-01):
```json
{
  "patient_plan_id": 123,
  "pillar_completions": [1, 3, 5],
  "reward_eligible_plan_id": 123,
  "reward_eligible_pillar_id": 3,
  "eligible": true
}
```

**Indexes**:
- PRIMARY KEY (`id`)
- INDEX (`patient_id`, `status`, `requested_at DESC`)
- INDEX (`reward_id`, `status`)

**Tenant Isolation**: Inherited from `patient_id → clinic_id`

**Validation Rules**:
- Points deducted immediately on `REQUESTED` (via PointsLedger)
- Points refunded on `REJECTED`, `CANCELLED_*`, `EXPIRED` (via PointsLedger)
- Auto-expiration job runs daily: `UPDATE redemptions SET status='EXPIRED', expired_at=NOW() WHERE status='APPROVED' AND approved_at < NOW() - INTERVAL '30 days'`

---

## Audit & Compliance Entities

### 16. AuditLog

Immutable log of all critical system events (FR-COMPLIANCE-01).

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PK | Unique audit log identifier |
| `clinic_id` | UUID | FK → Clinic, NULL | Associated clinic (NULL for system-level events) |
| `user_id` | UUID | FK → User, NULL | User who triggered event (NULL for system events) |
| `event_type` | VARCHAR(100) | NOT NULL | Event type (see below) |
| `entity_type` | VARCHAR(50) | NULL | Affected entity type (e.g., "Task", "Redemption") |
| `entity_id` | UUID | NULL | Affected entity ID |
| `event_data` | JSONB | NOT NULL | Event-specific data (before/after snapshots, etc.) |
| `ip_address` | VARCHAR(45) | NULL | User IP address (IPv6 compatible) |
| `user_agent` | TEXT | NULL | User agent string |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Event timestamp (immutable) |
| `archived_at` | TIMESTAMP | NULL | Archive timestamp (set when moved to cold storage) |

**Event Types**:
- `AUTH_LOGIN_SUCCESS`, `AUTH_LOGIN_FAILED`, `AUTH_LOGOUT`
- `ADMIN_CLINIC_CREATED`, `ADMIN_CLINIC_UPDATED`
- `ADMIN_METHOD_CREATED`, `ADMIN_PILLAR_CREATED`, `ADMIN_PLAN_CREATED`
- `ADMIN_JOURNEY_STAGE_CREATED`, `ADMIN_JOURNEY_STAGE_UPDATED`
- `ADMIN_PATIENT_CREATED`, `ADMIN_PATIENT_UPDATED`
- `ADMIN_TASK_ASSIGNED`, `ADMIN_TASK_VALIDATED`
- `ADMIN_VENDOR_CREATED`, `ADMIN_REWARD_CREATED`, `ADMIN_REWARD_UPDATED`
- `ADMIN_REDEMPTION_APPROVED`, `ADMIN_REDEMPTION_REJECTED`
- `PATIENT_TASK_STATUS_CHANGED`
- `PATIENT_REDEMPTION_REQUESTED`, `PATIENT_REDEMPTION_CANCELLED`
- `SYSTEM_POINTS_AWARDED`, `SYSTEM_POINTS_REFUNDED`
- `SYSTEM_REDEMPTION_EXPIRED`

**Indexes**:
- PRIMARY KEY (`id`)
- INDEX (`clinic_id`, `created_at DESC`)
- INDEX (`user_id`, `created_at DESC`)
- INDEX (`event_type`, `created_at DESC`)
- INDEX (`archived_at`)

**Event Data Example**:
```json
{
  "task_id": "123e4567-e89b-12d3-a456-426614174000",
  "old_status": "A_FAZER",
  "new_status": "FEITO",
  "completed_at": "2026-01-17T14:30:00Z"
}
```

**Retention Policy**:
- Active: 5 years in PostgreSQL
- Archive: Export to S3 Glacier after 5 years
- Partitioning: By year (`created_at`)

---

## Summary Statistics

| Entity | Tenant Scoped? | Soft Delete? | Audit Logged? |
|--------|----------------|--------------|---------------|
| Clinic | Root tenant | No | Yes |
| User | Cross-tenant (admins) | No | Yes (auth events) |
| ClinicMembership | N/A | No | Yes |
| Patient | Yes (clinic_id) | No | Yes |
| Methodology | Yes (clinic_id) | No | Yes |
| Pillar | Yes (via methodology) | No | Yes |
| FollowUpPlan | Yes (clinic_id) | No | Yes |
| PlanPillar | Yes (via plan) | No | No |
| JourneyStage | Yes (clinic_id) | No | Yes |
| PatientJourney | Yes (via patient) | No | No |
| Task | Yes (via patient) | **Yes** (deleted_at) | Yes |
| PointsLedger | Yes (via patient) | No (immutable) | No (is audit log) |
| Vendor | Yes (clinic_id) | No | Yes |
| Reward | Yes (clinic_id) | No | Yes |
| Redemption | Yes (via patient) | No | Yes |
| AuditLog | Yes (clinic_id) | No | No (is audit log) |

**Total Tables**: 16 (+ join tables)

---

## Validation Rules

### Tenant Isolation
- All clinic-scoped tables have `clinic_id` foreign key
- Repository base class enforces `WHERE clinic_id = :active_clinic_id` on all queries
- Database constraints: `CHECK (clinic_id IS NOT NULL)` on tenant-scoped tables

### Referential Integrity
- All foreign keys use `ON DELETE RESTRICT` (no cascading deletes for audit trail)
- Soft delete used for Task, Redemption (via `deleted_at` timestamp)

### Immutability
- PointsLedger: append-only (no updates/deletes)
- AuditLog: append-only (no updates/deletes)

### State Machine Enforcement
- Task status transitions: Enforced at application layer (state machine)
- Redemption status transitions: Enforced at application layer

---

## Next Steps
1. Generate OpenAPI contracts in `/contracts/`
2. Implement SQLAlchemy ORM models from this spec
3. Create Alembic migrations
4. Implement seed data scripts
