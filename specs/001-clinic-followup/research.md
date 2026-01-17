# Research: Technical Decisions for Multi-Clinic Follow-up System

**Feature**: 001-clinic-followup  
**Date**: 2026-01-17  
**Status**: Phase 0 Complete

## Overview
This document records the research findings and technology decisions for building a multi-tenant clinic follow-up system with gamification, scoring, and rewards. All NEEDS CLARIFICATION items from Technical Context have been resolved.

---

## 1. Authentication & Session Management

### Decision
Email + password authentication with server-side session management using FastAPI + Starlette sessions.

### Rationale
- **Security**: Server-side sessions are more secure than JWT for this use case (no token in localStorage, easier revocation)
- **Multi-clinic support**: Session can store active clinic context for admins with multiple clinic memberships
- **Logout**: Native session invalidation via session deletion
- **Audit**: All auth events (login, logout, failed attempts) logged to audit table

### Alternatives Considered
- **JWT tokens**: Rejected due to revocation complexity and unnecessary for server-rendered Streamlit UI
- **OAuth2**: Overkill for v1 (no external identity providers required)

### Implementation Notes
- Use `passlib` with bcrypt for password hashing
- Store sessions in PostgreSQL (not Redis) to minimize infrastructure dependencies
- Session timeout: 24h for patients, 8h for admins (configurable)
- Include `last_activity` timestamp for idle timeout

---

## 2. Multi-Tenant Architecture (Clinic Isolation)

### Decision
Row-level tenant isolation with `clinic_id` foreign key on all tenant-scoped tables. Enforce filtering at repository layer.

### Rationale
- **Simplicity**: Single database, single schema, no schema-per-tenant complexity
- **Scale**: Suitable for 10 clinics with 1000 patients each
- **Audit**: Easier to implement cross-tenant compliance queries
- **Cost**: No need for separate databases per tenant

### Alternatives Considered
- **Schema-per-tenant**: Rejected due to migration complexity and limited scale requirements
- **Database-per-tenant**: Rejected due to operational overhead for 10 clinics

### Implementation Notes
- Create `TenantAwareRepository` base class enforcing `clinic_id` filter on all queries
- Add database constraint `CHECK (clinic_id IS NOT NULL)` on tenant-scoped tables
- Add integration tests verifying no cross-tenant data leakage
- Include `clinic_id` in composite indexes for query performance

---

## 3. Hybrid Analytics Aggregation

### Decision
Real-time computation for current day + daily batch aggregation for historical data (7-90 days configurable).

### Rationale
- **Performance**: Pre-aggregated metrics avoid full table scans on every dashboard load
- **Freshness**: Real-time for current day ensures up-to-date visibility
- **Flexibility**: Configurable period (7-90 days) per clinic meets FR-ANALYTICS-01

### Alternatives Considered
- **Fully real-time**: Rejected due to performance concerns at scale (10k tasks/patient/year)
- **Fully batch**: Rejected due to staleness (users expect current-day visibility)

### Implementation Notes
- Create `analytics_snapshots` table storing daily aggregates per clinic per patient
- Scheduled job (cron/Celery) runs at midnight UTC to aggregate previous day
- Dashboard queries: `SELECT ... FROM analytics_snapshots WHERE date >= clinic.analytics_start_date UNION ALL <real-time query for today>`
- Quartile computation: Sort all patients by total points in period, divide into 4 equal groups

---

## 4. Internationalization (i18n) Strategy

### Decision
JSON-based label packs with runtime locale resolution via environment variable. No database storage of labels.

### Rationale
- **Simplicity**: File-based labels are easier to version control and review
- **Performance**: Labels loaded once at startup (no database round-trips)
- **Fallback**: Missing keys return `pt-BR` value + warning log (never crash)

### Alternatives Considered
- **Database-stored labels**: Rejected due to unnecessary complexity for v1 (no admin UI for label management)
- **gettext (.po/.pot files)**: Rejected due to overkill for JSON-friendly stack

### Implementation Notes
- Structure: `resources/labels/{locale}.json` (e.g., `pt-BR.json`, `en-US.json`)
- Load via `APP_LOCALE` env var (default: `pt-BR`)
- Helper function: `t(key, **kwargs)` for interpolation (e.g., `t('welcome', name=user.name)`)
- Add linter rule to detect hardcoded strings in `.py` files (best-effort via regex)

---

## 5. Soft Delete & Audit Retention

### Decision
Soft delete with `deleted_at` timestamp. Audit logs retained 5 years in active storage, then archived to cold storage (S3 Glacier).

### Rationale
- **Compliance**: LGPD requires audit trail for 5 years
- **Recovery**: Soft delete allows admin to recover accidentally cancelled tasks
- **Analytics**: Cancelled tasks must be queryable (FR-TASK-04)

### Alternatives Considered
- **Hard delete**: Rejected due to audit and analytics requirements
- **Retain forever**: Rejected due to storage costs and LGPD principle of data minimization

### Implementation Notes
- Add `deleted_at TIMESTAMP NULL` to `tasks`, `redemptions` tables
- All queries default to `WHERE deleted_at IS NULL` (use explicit `include_deleted=True` flag for audits)
- Archive job: Export audit logs older than 5 years to S3 Glacier, mark as archived in DB
- Archived logs remain queryable via separate admin tool (out of scope for v1)

---

## 6. Scoring Engine: Deterministic Streak Logic

### Decision
Streak bonus chain increments by +2 per consecutive eligible completion. Same-day completions count as a single chain link.

### Rationale
- **Determinism**: Spec requires predictable scoring (no random elements)
- **Fairness**: Same-day rule prevents double-counting when multiple tasks complete on one day
- **Auditability**: All bonus calculations logged to `points_ledger` with metadata

### Alternatives Considered
- **Individual chain increments per same-day task**: Rejected per spec clarification (same-day tasks share bonus tier)
- **Time-based ordering within same day**: Rejected as unnecessary complexity (spec says same-day = single link)

### Implementation Notes
- Query eligible completions: `SELECT ... WHERE completion_at < due_at AND validated_at IS NOT NULL ORDER BY completion_at ASC`
- Group by date: `DATE(completion_at)` to identify same-day clusters
- Increment logic: `bonus = 10 + (chain_position * 2)` where `chain_position` is 0-indexed cluster count
- Break detection: Any non-eligible completion (late, cancelled) resets chain
- Store chain metadata in `points_ledger.metadata` JSONB field for debugging

---

## 7. Redemption Eligibility: Snapshot at Request Time

### Decision
Snapshot patient's plan and pillar completion history at redemption request time. Store in `redemptions.eligibility_snapshot` JSONB field.

### Rationale
- **Fairness**: Patient's eligibility should not change if admin changes their plan mid-redemption
- **Traceability**: Admin can see what conditions were met at request time
- **Spec requirement**: FR-REDEEM-01 specifies "snapshot eligibility at request time"

### Alternatives Considered
- **Re-evaluate at approval time**: Rejected due to fairness concerns (patient's situation may change)

### Implementation Notes
- On redemption request:
  ```json
  {
    "patient_plan_id": 123,
    "pillar_completions": [1, 3, 5],
    "reward_eligible_plan_id": 123,
    "reward_eligible_pillar_id": 3,
    "eligible": true
  }
  ```
- Admin approval flow checks snapshot, not current state
- If reward criteria change after request, existing redemptions are unaffected

---

## 8. FastAPI + Streamlit Architecture

### Decision
Single monolithic application with FastAPI backend (REST API) and Streamlit frontend (admin + patient UIs).

### Rationale
- **Simplicity**: No need for separate frontend framework (React/Vue) for v1
- **Rapid prototyping**: Streamlit enables quick UI iteration
- **Authentication**: Shared session store between FastAPI and Streamlit
- **Deployment**: Single Docker container, easier ops

### Alternatives Considered
- **FastAPI + React**: Rejected due to increased complexity and dev time for v1
- **Pure Streamlit (no REST API)**: Rejected due to lack of clear API contracts for future integrations

### Implementation Notes
- FastAPI serves REST API at `/api/*`
- Streamlit runs on same app (mounted at `/` for admin, `/patient` for patients)
- Shared SQLAlchemy session and auth middleware
- OpenAPI docs auto-generated at `/api/docs`

---

## 9. Testing Strategy

### Decision
Three-tier testing: Unit (pytest), Integration (pytest + TestClient), Contract (OpenAPI validation).

### Rationale
- **Coverage**: Unit tests for business logic (scoring, eligibility), integration for API + DB, contract for API stability
- **Speed**: Unit tests run in <5s, integration in <30s
- **Confidence**: Contract tests catch breaking API changes

### Alternatives Considered
- **E2E Selenium tests**: Deferred to v2 (manual acceptance testing sufficient for v1)

### Implementation Notes
- Unit: Test scoring engine, eligibility logic, i18n fallback
- Integration: Test repositories with real PostgreSQL (TestContainer or Docker Compose)
- Contract: Use `schemathesis` to validate all API endpoints against OpenAPI spec
- CI gate: 80% code coverage minimum

---

## 10. Data Retention & Archival

### Decision
Active audit logs (5 years) in PostgreSQL. Archive older logs to S3 Glacier via scheduled job.

### Rationale
- **Compliance**: LGPD requires 5-year retention
- **Cost**: Active storage is expensive for rarely-accessed old logs
- **Query performance**: Pruning old logs improves query speed

### Alternatives Considered
- **Retain all logs in PostgreSQL**: Rejected due to storage costs
- **Immediate archive (1 year active)**: Rejected due to audit access patterns (3-year window commonly queried)

### Implementation Notes
- Table partitioning by year for `audit_logs` table
- Monthly job: Export logs older than 5 years to S3 Glacier (Parquet format)
- Mark as archived: `UPDATE audit_logs SET archived_at = NOW() WHERE created_at < NOW() - INTERVAL '5 years'`
- Archived logs queried via admin tool (Athena/Presto over S3)

---

## Summary of Key Decisions

| Area | Decision | Key Rationale |
|------|----------|---------------|
| Auth | Server-side sessions (FastAPI/Starlette) | Security, multi-clinic context, native logout |
| Tenancy | Row-level with `clinic_id` filter | Simplicity, suitable scale (10 clinics) |
| Analytics | Hybrid (real-time today + batch historical) | Balance performance and freshness |
| i18n | JSON label packs, env var locale | Simple, version-controlled, fast |
| Deletion | Soft delete with `deleted_at` | Audit, recovery, analytics requirements |
| Scoring | Deterministic streak (+2 increment, same-day = 1 link) | Spec requirement, fairness, auditability |
| Redemption | Snapshot eligibility at request time | Fairness, traceability |
| Stack | FastAPI + Streamlit monolith | Rapid v1, shared auth, simple deployment |
| Testing | Unit + Integration + Contract | Coverage, speed, API stability |
| Retention | 5y active (PostgreSQL) + archive (S3 Glacier) | LGPD compliance, cost optimization |

---

## Next Steps (Phase 1)
1. Generate `data-model.md` with entity definitions
2. Create OpenAPI contracts in `/contracts/`
3. Generate `quickstart.md` with setup instructions
4. Update `.github/copilot-instructions.md` with technology stack
