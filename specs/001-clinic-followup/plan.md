# Plan: Architecture, Data Model, and Operational Design

## Architecture (Prototype)
- UI: Streamlit app
- API/Data access: Python services/repositories (OOP)
- DB: PostgreSQL
- Containerization: Docker (docker compose for local)
- Modeling/validation: Pydantic models
- Logging: structured logs + audit log table
- No external integrations in v1

## Tenancy Model (Multi-Clinic)
- Shared schema, tenant isolation via `clinic_id` on all tenant-scoped tables.
- Admin users can belong to multiple clinics via `clinic_memberships`.
- Patients belong to exactly one clinic via `patients.clinic_id`.
- Streamlit session holds `active_clinic_id` for admins; patients infer clinic from their profile.
- All repository queries MUST filter by `clinic_id` (except truly global tables like users).

## Authentication & Authorization
- Email + password (hashed + salted).
- Session-based auth for Streamlit.
- Authorization:
  - Admin: unrestricted within active clinic(s).
  - Patient: restricted to their own patient_id and clinic_id.

## Internationalization / Label Packs (No Hardcoded UI Strings)
- Labels stored as JSON:
  - `resources/labels/pt-BR.json` (default)
  - future: `resources/labels/en-US.json`, etc.
- Loader:
  - selects locale via env var `APP_LOCALE` (default: pt-BR)
  - fallback to pt-BR for missing keys
  - missing key behavior: render placeholder like `[[missing.key]]` and log warning
- UI helper:
  - `t(key: str, **kwargs) -> str` supports parameter interpolation

## Core Data Model (Tables)
Suggested tables (simplified):

### Global
- `users` (id, email, password_hash, role, created_at, disabled_at)
- `audit_log` (id, clinic_id nullable, actor_user_id, action, entity_type, entity_id, diff_json, created_at)
- `retention_policies` (id, clinic_id nullable, entity_type, retention_days, created_at)

### Clinic-scoped
- `clinics` (id, name, is_training, created_at)
- `clinic_memberships` (clinic_id, user_id, role_in_clinic)

- `patients` (id, clinic_id, user_id nullable, full_name, email, created_at, archived_at)

- `methodologies` (id, clinic_id, name, description)
- `pillars` (id, clinic_id, methodology_id, name, description, sort_order)

- `followup_plans` (id, clinic_id, methodology_id, name, description)
- `plan_pillars` (plan_id, pillar_id)

- `journey_stages` (id, clinic_id, name, sort_order, stage_type)

- `tasks` (id, clinic_id, patient_id, title, description, due_at, status, created_at, updated_at,
           had_delay bool, had_pause bool, had_reopen bool,
           base_points_max int default 100, base_points_final int,
           validated_at, validated_by_user_id,
           is_soft_deleted bool)

### Status Mapping (Portuguese Domain ↔ Schema Flags)
| Domain Status (PT) | Schema Representation |
|--------------------|----------------------|
| A_FAZER | status = 'A_FAZER' |
| FEITO | status = 'FEITO' |
| EM_ATRASO | status = 'EM_ATRASO', sets `had_delay = true` |
| PAUSADO | status = 'PAUSADO', sets `had_pause = true` |
| RETOMADO | status = 'RETOMADO', sets `had_reopen = true` |
| CANCELADO_PELO_PACIENTE | status = 'CANCELADO_PELO_PACIENTE' |
| CANCELADO_PELA_CLINICA | status = 'CANCELADO_PELA_CLINICA' |

- `points_ledger` (id, clinic_id, patient_id, task_id nullable, redemption_id nullable,
                   entry_type, points_delta int, reason, created_at)

- `vendors` (id, clinic_id, name, contact_info)
- `rewards` (id, clinic_id, vendor_id, name, description,
             points_cost int,
             monetary_value_cents int,
             quantity_available int,
             expires_at,
             eligible_plan_id nullable,
             eligible_pillar_id nullable,
             active bool)

- `redemptions` (id, clinic_id, patient_id, reward_id,
                 status,
                 requested_at, approved_at, approved_by_user_id,
                 redeemed_at, cancelled_at, cancel_reason)

## Deterministic Scoring (Algorithm Notes)
### Base points
- Start 100.
- Compute final base points on transition to FEITO or cancellation:
  - FEITO no delay/pause/reopen => 100
  - FEITO + delay => 80
  - FEITO + pause/reopen => 75
  - FEITO + pause/reopen + delay => 60
  - CANCELADO_PELO_PACIENTE => 0
  - CANCELADO_PELA_CLINICA => keep current base points value

Record base award as a ledger entry.

### Streak bonus (validated)
- Only award streak bonus on admin validation.
- Chain order is determined by `validated_at` timestamp (not task due date or completion timestamp).
- Maintain patient streak state (can be derived from ledger + validation order):
  - Find last validated completion that was eligible and chain-continuing.
  - If current validated completion is eligible (`completion_at < due_at`) AND its `validated_at` directly follows the previous chain entry (no ineligible validation in between), bonus = last_bonus + 2; else bonus resets to 10.
- Record streak award as ledger entry.

## Redemption & Points Consumption
- On APPROVED, create ledger entry with negative points equal to reward.points_cost.
- If later CANCELLED_BY_CLINIC/EXPIRED before REDEEMED, either:
  - (Option A) refund points with compensating ledger entry, or
  - (Option B) only consume at REDEEMED
Pick one and keep consistent. Recommended for prototype: consume at APPROVED, refund on clinic cancellation/expiry.

## Analytics (Quartiles)
See FR-ANALYTICS-01 in spec.md. Implementation notes:
- Compute over configurable time window (default 30 days)
- Use SQL window functions (NTILE) for quartile computation
- Display per clinic in admin dashboard

## Compliance (LGPD) Notes
- Store minimum PII (name/email); avoid medical details in v1.
- Audit critical actions with actor, time, entity, and diff.
- Data retention:
  - soft delete entities, keep audit logs per retention policy
  - define a default retention policy per clinic, configurable by admin

## Deployment
- Docker image runs Streamlit app.
- PostgreSQL via docker compose for local.
- Environment variables:
  - DB connection (host, port, user, password, db)
  - `APP_LOCALE` (default pt-BR)
  - `APP_TRAINING_CLINIC_SEED=true` (seed Contoso)

## Sources
- `docs/sources/001-clinic-followup/initial-intake.md`
- `docs/sources/001-clinic-followup/seed-data.md`
