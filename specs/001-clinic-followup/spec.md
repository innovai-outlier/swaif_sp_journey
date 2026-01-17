# Spec: Multi-Clinic Follow-up Plans, Gamification, and Rewards

## Overview
This feature set enables medical clinics to configure follow-up methodologies and plans, define patient journeys, assign gamified tasks, compute points, and allow points-based reward redemption.

v1 supports **multiple clinics**. **Contoso** is seeded as a training clinic. Additional clinics can be created for other customers.

## Goals
- Enable Clinic Admins to configure Methodology → Pillars → Follow-up Plans → Journey Stages.
- Support patient adherence via tasks, deterministic scoring, and clinic-validated streak bonuses.
- Provide rewards catalog and redemption flow without payments.
- Provide admin analytics for adherence segmentation (quartiles).
- Ensure tenant isolation across clinics.
- Ensure all UI text comes from locale label packs (pt-BR default).

## Non-Goals
- Payments or checkout
- EHR/EMR integrations
- Vendor self-service portal in v1
- Complex staff roles beyond Clinic Admin and Patient
- Password reset and account lockout flows (v2)
- Task templates (v2)
- Runtime locale switcher UI (v2); locale is set via environment variable
- Admin UI for retention policy management (v2); policies configured via database seed/migration
- Admin user invitation flow (v2); initial admins seeded via migration

## Users & Roles
### Clinic Admin
- Full access within the clinics they administer:
  - manage clinics (create/edit)
  - manage methods, pillars, plans, journey stages
  - manage patients, tasks, scoring visibility, and validations
  - manage vendors, rewards, redemptions
  - view analytics and full histories

### Patient
- Restricted to their clinic context:
  - view tasks, statuses, deadlines
  - mark task status changes
  - view points and streak bonus results
  - browse rewards by points and request redemption
- Must never see monetary values.

## Clarifications

### Session 2026-01-17
- Q: FR-AUTH-01 specifies "email + password" authentication but doesn't clarify the session management approach, logout mechanism, or whether admin and patient sessions should have different timeout policies. Which authentication pattern should be implemented? → A: Email + password with session management and standard logout
- Q: FR-TASK-01 states "Clinic Admin SHALL assign tasks to patients" but doesn't clarify whether patients can create their own tasks or if task creation is exclusively an admin function. What is the task creation authority model? → A: Admin-only task creation; patients can only view and update status
- Q: FR-ANALYTICS-01 requires adherence analytics with quartile computation over "last 30 days (configurable per clinic)" but doesn't specify the data aggregation strategy. Should analytics be computed real-time, pre-aggregated, or use another approach? → A: Hybrid: real-time for current day + batch for historical data
- Q: FR-POINTS-02 states "Clinic Admin SHALL validate completion; streak bonus is granted only after validation" but FR-TASK-02/03 allow patients to transition tasks to FEITO. How should validation interact with task status workflow? → A: Patient can mark FEITO; validation is separate admin action that unlocks streak bonus
- Q: FR-REDEEM-01 describes redemption workflow but doesn't specify what happens if a patient requests a redemption that exceeds their available points balance. What is the point insufficiency handling strategy? → A: Block redemption request if insufficient points; show clear error message
- Q: The spec describes task status transitions and point calculations but doesn't specify the data retention behavior when a patient or admin cancels a task. This affects audit trail completeness, compliance reporting, and whether historical analytics include cancelled tasks. What is the task deletion/retention strategy? → A: Soft delete with audit trail
- Q: FR-REWARD-01 specifies reward eligibility rules with eligible_plan_id and eligible_pillar_id (both optional), but doesn't address how the system should handle rewards when a patient's plan changes mid-journey. This impacts whether previously requested redemptions remain valid and whether reward eligibility is evaluated at request time vs. redemption time. What is the eligibility evaluation strategy? → A: Snapshot eligibility at request time
- Q: FR-COMPLIANCE-01 requires audit logs for multiple event types but doesn't specify log retention duration or archival strategy. This is critical for LGPD compliance, storage planning, and determining when logs can be safely purged or archived. What is the audit log retention policy? → A: Retain 5 years active + archive older
- Q: FR-ANALYTICS-01 specifies "last 30 days (configurable per clinic)" for adherence analytics but doesn't specify the minimum allowable configuration range. Without bounds, clinics could set unreasonably short periods that produce meaningless quartiles, or very long periods that impact performance. What is the allowable analytics period configuration range? → A: 7 to 90 days configurable
- Q: FR-POINTS-02 describes streak bonus calculation based on "consecutive eligible completions (in completion order)" but doesn't specify how the system should handle ties when multiple tasks complete on the same day. This affects the determinism of streak calculation and whether order-of-completion within a day matters. How should same-day completions be handled for streak calculation? → A: Same-day completions count as single chain link

## Functional Requirements

### FR-CLINIC-01 Multi-Clinic
- System SHALL support 1+ clinics.
- System SHALL seed a training clinic named “Contoso”.
- Clinic Admin SHALL be able to create additional clinics.
- System SHALL enforce tenant isolation: data from clinic A must not be visible in clinic B.

### FR-AUTH-01 Authentication
- Users SHALL authenticate via email + password.
- System SHALL implement session management with standard logout functionality.
- System SHALL log all authentication events (login, logout, failed attempts) for audit compliance.
- Clinic Admins may be members of multiple clinics; patients belong to exactly one clinic.

### FR-METHOD-01 Methodologies and Pillars
- Clinic Admin SHALL create Methodologies and associated Pillars.

### FR-PLAN-01 Follow-up Plans
- Clinic Admin SHALL create Follow-up Plans linked to a Methodology and select Pillars.

### FR-JOURNEY-01 Patient Journey
- Clinic Admin SHALL define ordered Journey Stages (lead → close → follow-up).

### FR-TASK-01 Task Assignment
- Clinic Admin SHALL assign tasks to patients with due dates (direct assignment only in v1).
- Task creation is restricted to Clinic Admins only; patients cannot create tasks.
- Patient SHALL view their assigned tasks and change statuses only.

### FR-TASK-02 Task Statuses
Supported statuses:
- A_FAZER, FEITO, EM_ATRASO, PAUSADO, RETOMADO, CANCELADO_PELO_PACIENTE, CANCELADO_PELA_CLINICA

### FR-TASK-03 Task Status Transitions
Valid transitions:
- A_FAZER → FEITO | EM_ATRASO | PAUSADO | CANCELADO_PELO_PACIENTE | CANCELADO_PELA_CLINICA
- EM_ATRASO → FEITO | PAUSADO | CANCELADO_PELO_PACIENTE | CANCELADO_PELA_CLINICA
- PAUSADO → RETOMADO | CANCELADO_PELO_PACIENTE | CANCELADO_PELA_CLINICA
- RETOMADO → FEITO | EM_ATRASO | PAUSADO | CANCELADO_PELO_PACIENTE | CANCELADO_PELA_CLINICA
- FEITO, CANCELADO_* are terminal states.

### FR-TASK-04 Task Deletion and Retention
- System SHALL implement soft delete for all cancelled tasks (CANCELADO_PELO_PACIENTE, CANCELADO_PELA_CLINICA).
- Cancelled tasks SHALL be marked as deleted but retained in the database with complete audit trail.
- Cancelled tasks SHALL remain queryable for analytics, compliance reporting, and historical analysis.
- System SHALL include cancelled task metrics in adherence analytics (FR-ANALYTICS-01).

### FR-POINTS-01 Base Scoring
- Each assigned task starts with max 100 points.
- Final base points (starting from 100):
  - Done without delay/pause/reopen: 100 (no deduction)
  - Done with delay: 80 (−20)
  - Done with pause/reopen without delay: 75 (−25)
  - Done with pause/reopen with delay: 60 (−40)
  - Cancelled by patient: 0 (all points lost)
  - Cancelled by clinic: no change (patient retains current points)

### FR-POINTS-02 Streak Bonus (Clinic Validated)
- Completion strictly before due date (`completion_at < due_at`) is eligible for streak bonus.
- Bonus per completion starts at 10 points.
- Consecutive eligible completions (in completion order) increase bonus by +2 each link (10, 12, 14, ...).
- Multiple tasks completed on the same day count as a single chain link; all same-day completions share the same bonus tier.
- If chain breaks, the next eligible bonus resets to 10.
- Patient can transition task to FEITO status; base points (per FR-POINTS-01) are awarded immediately upon status change.
- Streak bonus eligibility requires separate Clinic Admin validation action; streak bonus points are granted only after validation.
- Validation is decoupled from task status: a task can remain in FEITO status while awaiting validation.

### FR-REWARD-01 Rewards Catalog
- Clinic Admin SHALL create Vendors and Rewards.
- Reward fields include:
  - points_cost (patient-visible)
  - monetary_value (admin-only)
  - quantity_available (limited)
  - expires_at
  - eligibility rules:
    - `eligible_plan_id` (optional): patient must be enrolled in this plan
    - `eligible_pillar_id` (optional): patient must have completed ≥1 task in this pillar
    - If both are set, **both conditions must be met** (AND logic)
    - If neither is set, reward is available to all patients in the clinic

### FR-REDEEM-01 Redemption Workflow
- Patient SHALL request a redemption.
- System SHALL block redemption requests if patient has insufficient points balance and display a clear error message.
- System SHALL snapshot reward eligibility criteria at redemption request time (patient's current plan and pillar completion history).
- Plan changes after redemption request SHALL NOT affect eligibility of pending redemptions.
- Points are reserved (deducted) immediately upon successful redemption request.
- Clinic Admin SHALL approve or reject redemption.
- System SHALL track redemption statuses.

Recommended statuses:
- REQUESTED, APPROVED, REJECTED, REDEEMED, CANCELLED_BY_PATIENT, CANCELLED_BY_CLINIC, EXPIRED

### FR-REDEEM-02 Redemption Expiration
- Redemptions in status APPROVED that are not marked REDEEMED within 30 days SHALL be automatically transitioned to EXPIRED by a scheduled background job (daily).
- On EXPIRED, points SHALL be refunded to the patient via a compensating ledger entry.

### FR-ANALYTICS-01 Adherence Analytics
- Admin SHALL see adherence segmentation based on quartiles computed over a configurable analytics period (default: 30 days, range: 7 to 90 days per clinic).
- System SHALL use hybrid aggregation: real-time computation for current day data + daily batch aggregation for historical data (updated via scheduled job).
- Metrics include:
  - Total points accumulated
  - Streak bonus accumulation
  - Counts of delayed, paused, and cancelled tasks
- Quartile thresholds are computed dynamically per clinic based on patient distribution.
- Admin dashboard SHALL display:
  - Summary cards: Total patients, Average points, Period range (configurable days)
  - Adherence table with columns: Patient Name, Quartile (Q1/Q2/Q3/Q4), Total Points, Streak Points, Tasks Completed, Tasks Delayed, Tasks Paused, Tasks Cancelled
  - Quartile distribution indicator showing count of patients in each quartile
  - Filter/sort controls: by quartile, by points (ascending/descending), by name

### FR-I18N-01 UI Labels
- System SHALL not hardcode any UI text.
- System SHALL load all UI labels/messages from locale files (pt-BR default).
- System SHALL support adding new locales later with fallback to pt-BR.
- Locale is set via environment variable (APP_LOCALE) at application startup.
- Changing locale requires application restart in v1 (runtime locale switcher deferred to v2 per Non-Goals).

### FR-COMPLIANCE-01 LGPD, Audit, Retention
- System SHALL maintain audit logs for:
  - auth events
  - admin config changes
  - task status changes
  - points ledger changes
  - redemptions lifecycle
- System SHALL retain audit logs in active storage for 5 years from creation date.
- System SHALL archive audit logs older than 5 years to cold storage for long-term compliance.
- System SHALL implement a data retention policy and support soft delete.

## Acceptance Criteria (Pass/Fail)
1) Multi-clinic:
   - Admin can create a new clinic in addition to seeded Contoso.
   - Data in clinic X is not visible in clinic Y.
2) Setup:
   - Admin creates 1 Methodology with ≥3 Pillars, ≥1 Follow-up Plan, and ≥3 Journey Stages.
3) Tasks:
   - Admin assigns tasks to patients; patients see and update statuses.
4) Scoring:
   - Base points follow the specified deduction rules.
   - Streak bonus is granted only after admin validation and follows the chain (+2) rule.
5) Rewards:
   - Rewards enforce quantity/expiry/eligibility; patient view shows points-only.
6) Redemptions:
   - Patient can request; admin can approve/reject; points are consumed consistently.
7) UI labels:
   - All UI text originates from label packs; switching locale is possible (fallback to pt-BR).
8) LGPD:
   - Audit logs exist for critical actions and are retained per policy.

## Sources
- `docs/sources/001-clinic-followup/initial-intake.md`
- `docs/sources/001-clinic-followup/seed-data.md`
