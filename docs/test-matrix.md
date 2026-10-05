
# Test Matrix — AquaFlow / Garbusa Water Management
**Lab**: Week 10 — Manual QA & Bug Hunting
**Date**: 2026-10-05 | **Team**: 5 Members | **Phase**: Feature Freeze — Log Only, Do Not Fix

## Scenario Definitions
| Code | Scenario | Description |
|---|---|---|
| ✅ H | Happy Path | Valid inputs, normal conditions — must succeed |
| ⚠️ B | Boundary | Min/max limits, edge values, exact thresholds — must handle gracefully |
| ❌ I | Invalid | Bad format, impossible values, wrong types — must reject clearly |
| ⬜ E | Empty/Null | Blank, missing, zero-length — must not crash |
| 🔐 P | Permissions | Unauthorized role, wrong access level — must block |

## Status Key
| Mark | Meaning |
|---|---|
| ✅ PASS | Works as expected |
| ❌ FAIL | Bug found — log in Task 5 |
| ⚪ N/A | Not applicable |
| ⏳ TBD | Not yet tested |

## Severity Labels
- **P0** = Critical — core broken / data loss / security breach
- **P1** = High — major broken, workaround exists
- **P2** = Low — cosmetic / minor / rare

#1 — P0-001 Login accepts blank password
#2 — P1-001 Accepts negative reading values
---

## Full Test Matrix with Pre‑Written Cases

| # | Feature / Module | ✅ H — Happy Path | ⚠️ B — Boundary | ❌ I — Invalid | ⬜ E — Empty / Null | 🔐 P — Permissions | Status | Bug Ref |
|---|---|---|---|---|---|---|---|---|

| 1 | **Login** | Enter valid email + correct password → dashboard loads, session active | Email = max length (254 chars); password = exactly min/max length; mixed case email → login succeeds | Wrong password; non-existent email; email without `@`; password only whitespace → error message | Email blank; password blank; both fields empty → **REQUIRED — BUT ACCEPTS BLANK PASSWORD** | Login as deactivated/disabled account; viewer tries admin login → access denied | ❌ | #1 — P0-001 Login accepts blank password → grants access |

| 2 | **Registration** | Unique email + strong pass + valid name → account created, confirmation sent | All fields at exact max length; phone = min/max digits; password exactly min length → success | Duplicate email; password too short; invalid phone chars; email with spaces → clear error | Name blank; email blank; phone blank; all fields empty → required field prompts | Attempt to register directly as admin role; duplicate username → role blocked / rejected | ⏳ | |

| 3 | **Dashboard Load** | Logged in as valid user → all metrics/charts render within 3s | 500+ records; rapid refresh; date range = 12 months → loads without freezing | Tampered session token; corrupted local storage; invalid dashboard URL → graceful error / redirect login | New account with 0 data → "No records yet" friendly message, no spinner hang | Direct URL to another user’s dashboard; guest tries admin panel → 403 Forbidden / redirect | ⏳ | |

| 4 | **Water Reading Submit** | Numeric value + valid date → saves, appears in list immediately | Reading = min allowed; reading = max allowed; same timestamp entry; leap day (Feb 29) → accepted / handled | Negative value; text/emoji in value; future date; duplicate same reading → **REJECTED — ACTUALLY ACCEPTS -15** | Value blank; date blank; both empty → required prompts, no save | Viewer tries submit; user edits another’s reading → submit button hidden / error on save | ❌ | #2 — P1-001 Accepts negative value → saves to DB |

| 5 | **Farmer Profile** | Complete valid form → profile listed, searchable | Name/address at max length; special chars `&-'.,` in fields; longest valid region name → saves correctly | Duplicate ID; invalid contact format; impossible region code → rejected | Name blank; contact blank; location blank → required prompts shown | Regular user creates profile; viewer edits profile → action denied / button hidden | ⏳ | |

| 6 | **Reports Export** | Valid date range + farmer filter → PDF/CSV downloads correctly | Range = 1 day; range = max allowed span; single record only → generates file | End date before start date; non-existent farmer ID; format = `xml` or `html` → rejected / no data message | No filters selected; no matching records → "No data available" message, empty file not broken | User exports restricted report; downloads others’ data → 403 or blank filtered file | ⏳ | |

| 7 | **Profile Update** | New display name + valid email → changes persist after refresh | Password exactly min length; display name = max chars; no changes submitted → saves / no error | Mismatched password confirm; invalid email format; forbidden chars in name → rejected | All fields cleared & submitted → required prompts; leave unchanged → save succeeds | Update another user’s profile; attempt elevate own role → changes ignored / access denied | ⏳ | |

| 8 | **Search & Filter** | Partial/valid keyword → matching results shown instantly | Exact match; 1‑char search; very long search string; all filters cleared → correct results | SQL‑like input `' OR 1=1--`; script tags; non‑existent term → no injection, empty result not crash | Empty search; whitespace only → shows all / prompt, no crash | Search for hidden/restricted records → results omitted from list | ⏳ | |

| 9 | **Supabase Sync** | Submit valid entry → appears in DB & UI within 1s | Concurrent rapid saves; near row limit; slow/weak connection → retries / queues, no loss | Direct API POST with bad schema; duplicate key; wrong data type → rejected | Null payload; missing required column → rejected, no empty row created | Write to table without permission; read others’ private rows → RLS blocks / returns empty | ⏳ | |

| 10 | **UI Navigation** | Click all links → correct page loads; back/forward work | Min window width; rotate mobile; quick consecutive clicks → responsive, no duplication | Tampered URL `/user/notexist`; deep link to deleted record → 404 page shown gracefully | Page loading with empty dataset → layout intact, no broken elements | Type admin route directly in browser → redirect / 403 | ⏳ | |

| 11 | **Adversarial / Network** | — | Submit then immediately refresh; double‑click submit button; go back mid‑process → no duplicate / no orphan | Input: `😎🔥<script>alert(1)</script>`; huge number (1e308); 10KB text in short field → escaped / rejected | — | — | ⏳ | |

| 12 | **Offline / Slow Network** | — | Network throttled to Slow 3G; offline during submit → shows "working…", recovers when back online | Submit fully offline → clear "Check connection" message, no silent failure | — | — | ⏳ | |

---

## Bug Log Template — Task 5
Copy & fill for EVERY ❌ FAIL:
