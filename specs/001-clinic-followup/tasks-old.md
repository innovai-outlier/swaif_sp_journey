# Tasks: Implementation Checklist (Dependency-Ordered)

> Each item is intended to be checkable. Keep the prototype scope tight.

## 0) Repo & Tooling
- [ ] Initialize Python project structure (src/, tests/, resources/, specs/, docs/)
- [ ] Add Dockerfile + docker-compose (app + postgres)
- [ ] Add env var configuration management

## 1) Data & Migrations
- [ ] Define PostgreSQL schema (tables in plan.md)
- [ ] Add migration tool (e.g., Alembic) and initial migrations
- [ ] Add seed scripts:
  - [ ] Seed Contoso clinic (`is_training=true`)
  - [ ] Seed 10 patients with tiered scores
  - [ ] Seed rewards and vendors

## 2) Domain Models (OOP + Pydantic)
- [ ] Create Pydantic models for: Clinic, User, Patient, Methodology, Pillar, Plan, Stage, Task, Reward, Redemption, LedgerEntry
- [ ] Enforce enum constraints for task statuses and redemption statuses

## 3) Multi-Clinic Tenancy & Auth
- [ ] Implement email/password auth with secure hashing
- [ ] Implement clinic memberships for admins
- [ ] Implement active clinic context in Streamlit session
- [ ] Enforce clinic_id scoping in all repositories (no cross-clinic leakage)
- [ ] Add tests for tenant isolation

## 4) Internationalization (NO HARDCODED UI STRINGS)
- [ ] Create label pack structure: `resources/labels/<locale>.json`
- [ ] Implement LabelService:
  - [ ] load selected locale (env `APP_LOCALE`) with pt-BR fallback
  - [ ] missing key placeholder + warning log
  - [ ] `t(key, **kwargs)` interpolation
- [ ] Replace ALL Streamlit UI text with label keys
- [ ] Add a simple regression check:
  - [ ] grep/lint gate for hardcoded UI strings (best-effort)
  - [ ] unit test for missing-key behavior

## 5) Admin UI — Clinic Setup
- [ ] Admin: clinic selector (if member of >1 clinic)
- [ ] Admin: create clinic flow
- [ ] Admin: manage methodology + pillars
- [ ] Admin: manage follow-up plans (link methodology + pillars)
- [ ] Admin: manage journey stages

## 6) Admin UI — Patients, Tasks, Validation
- [ ] Admin: patient list + patient detail
- [ ] Admin: assign patient to journey stage
- [ ] Admin: advance patient through journey stages (manual progression)
- [ ] Admin: assign tasks to patient (title, description, due date)
- [ ] Admin: view task history and status timeline
- [ ] Admin: validate completion for streak bonus

## 7) Patient UI — Tasks and Progress
- [ ] Patient: task list with filters (status, due date)
- [ ] Patient: update task status transitions
- [ ] Patient: view points balance + recent ledger entries (read-only)

## 8) Scoring Engine
- [ ] Implement base scoring computation on status changes
- [ ] Implement streak bonus computation on validation events
- [ ] Persist all points changes to points_ledger
- [ ] Add unit tests covering examples:
  - [ ] 5 consecutive before-due-date validations => bonuses: 10+12+14+16+18 (chain increments: 0+2+2+2+2)
  - [ ] broken chain example => bonuses: 10+10+10+12+10 (chain increments: 0+0+0+2+0); chain breaks when an ineligible validation occurs between eligible ones

## 9) Rewards & Redemptions
- [ ] Admin: vendor management
- [ ] Admin: reward CRUD (quantity, expiry, eligibility, monetary_value admin-only)
- [ ] Patient: browse eligible rewards (points-only view)
- [ ] Patient: request redemption
- [ ] Admin: approve/reject redemption
- [ ] Implement points consumption + refund rules consistently
- [ ] Add tests for quantity/expiry/eligibility enforcement

## 10) Analytics (Quartiles)
- [ ] Compute adherence metrics per clinic:
  - [ ] quartiles for streak accumulation
  - [ ] counts for delayed/paused/cancelled
- [ ] Admin dashboard visualizations (simple tables/indicators)

## 11) Compliance (LGPD)
- [ ] Implement audit logging for key events:
  - [ ] admin config changes
  - [ ] task status changes
  - [ ] validations
  - [ ] ledger entries
  - [ ] redemptions
- [ ] Implement retention policy scaffolding (configurable) + soft delete utilities

## 12) Quality Gates
- [ ] End-to-end smoke flow:
  - [ ] create clinic (non-Contoso)
  - [ ] create plan/method/pillars
  - [ ] add patient
  - [ ] assign task
  - [ ] patient completes
  - [ ] admin validates
  - [ ] patient redeems reward
- [ ] Security sanity checks (tenant isolation + role checks)
- [ ] Performance sanity for lists (pagination or limits)
