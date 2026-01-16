# Initial Intake (Consolidated)

## Product Summary
A multi-clinic software solution for medical clinics to configure follow-up plans and patient journeys, assign gamified tasks to patients, compute points (base + streak bonus), and allow points-based reward redemptions. No payments are processed.

## Core Modules
1) Methodology & Follow-up Plans
- Clinic Admin defines a Methodology (named method) and its Pillars.
- Clinic Admin creates Follow-up Plans linked to a Methodology and Pillars.

2) Patient Journey
- Clinic Admin defines a Journey from lead capture → first close → post-close follow-up.
- Journey is represented as ordered stages.

3) Gamification (Tasks + Points)
- Patients receive tasks with due dates and statuses.
- Base task points start at 100 and are deducted based on delay/pause/reopen/cancellation.
- Clinic validates completion for streak bonus.

Task statuses (domain language):
- A_FAZER (todo)
- FEITO (done)
- EM_ATRASO (delayed)
- PAUSADO (paused)
- RETOMADO (reopen)
- CANCELADO_PELO_PACIENTE (canceled by patient)
- CANCELADO_PELA_CLINICA (canceled by clinic)

Base scoring (per assigned task):
- Start: 100 points
- Done with no delay/pause/reopen: -0 (final 100)
- Done with delay: -20 (final 80)
- Done with pause/reopen without delay: -25 (final 75)
- Done with pause/reopen with delay: -40 (final 60)
- Patient cancels: subtract all remaining points (final 0)
- Clinic cancels: patient keeps current remaining points (no penalty)

Streak bonus (clinic-validated):
- Each completion yields bonus points.
- If task is completed before due date AND completions are consecutive (in completion order), bonus forms a chain: 10, 12, 14, 16, ...
- If chain breaks, next bonus resets to 10.

4) Rewards (Marketplace-like, no payments)
- Rewards can be offered by vendors, including the clinic.
- Rewards have monetary value (admin-only), points cost (patient-visible), limited quantity, expiry date, and eligibility rules.
- Patient can request redemption; clinic approves.
- Vendor implicitly accepts clinic-approved redemptions.

5) Analytics (Admin)
- Adherence insights based on quartile distribution over performance and signals (streak accumulation, delays, pauses, cancellations).

## Roles & Access
- Clinic Admin: full visibility into all patients and histories; configures everything.
- Patient: sees tasks, statuses, points, and rewards-by-points only; cannot see monetary values.

## Internationalization / UI Labels
- No UI strings can be hardcoded.
- All UI labels/messages must come from a locale label pack file, initially pt-BR.
- UI must be able to load other locales later (fallback to pt-BR).

## Tech Constraints
- Streamlit UI (neutral palette; logo placeholder top-left)
- Dockerized execution
- PostgreSQL storage
- OOP Python with Pydantic models
- LGPD baseline: audit logs + data retention
