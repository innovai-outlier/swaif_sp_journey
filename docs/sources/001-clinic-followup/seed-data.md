# Seed Data Notes (Prototype)

## Clinics
- Contoso (training clinic) is preloaded.
- System supports creating additional clinics for other customers.

## Contoso Patients (10)
- 3 Top performers (high points, high streak)
- 4 Intermediate
- 3 Low performers ("less frequent" = lower scores)

## Rewards (examples)
Vendor: Contoso Clinic (and optionally one external vendor)

- NADH application
- Vitamin B12 application
- Gut regulation supplement bundle
- PepTStrong supplement
- Bonus benefit: discount/cashback/procedure credit
  - Note: no payments in the system; only redemption records and points consumption.

Each reward includes:
- points_cost
- monetary_value (admin-only)
- quantity_available (limited)
- expires_at
- eligibility: optional plan/pillar restriction
