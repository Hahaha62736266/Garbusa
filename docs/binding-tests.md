# Binding & End‑to‑End Test Results
**Test Date:** 2026-10-02 | **Time:** 14:52 UTC+8
**Duration:** ~12 min / 15 min allocated
**Tester:** E2E Validation

---

## Test 1 – Create Record via UI
- **Action:** Navigated to create form → entered valid sample data → submitted
- **Sample Data:**

- - **Expected:** Record saved → listed in records view with all fields matching input
- **Actual:** ✅ Passed – Record appeared immediately; all values persisted exactly as entered
- **Status:** ✅ PASS

---

## Test 2 – Edit Record via UI
- **Action:** Selected record → clicked edit → updated fields → saved
- **Changes:**

- - **Expected:** Updated values displayed; old values no longer visible
- **Actual:** ✅ Passed – Refresh confirmed new values; no stale data shown
- **Status:** ✅ PASS

---

## Test 3 – Invalid Data Submission (422 Validation)
- **Action:** Submitted form with missing/ malformed fields
- **Invalid Cases & Results:**

| # | Field               | Input Value               | Expected Behavior                  | Actual Result                                  | Status |
|---|---------------------|---------------------------|-------------------------------------|------------------------------------------------|--------|
| 1 | Name                | *(empty)*                 | Error: "Name is required"           | ✅ Displayed inline error message              | PASS   |
| 2 | Area (ha)           | `-1.5` (negative number) | Error: "Area must be greater than 0" | ✅ Field highlighted; message shown            | PASS   |
| 3 | Area (ha)           | `not-a-number`            | Error: "Must be a valid number"     | ✅ HTTP 422 returned; errors mapped to field   | PASS   |
| 4 | Location            | *(5 chars only)*          | Min length validation               | ✅ Error shown: "Location too short"          | PASS   |

- **Response Code:** `422 Unprocessable Entity` ✅
- **Error Format:** Errors keyed by field name; messages human‑readable ✅
- **Status:** ✅ All PASS

---

## Summary
| Step | Description                          | Result |
|------|--------------------------------------|--------|
| 1    | Create & persist record              | PASS   |
| 2    | Edit & persist changes               | PASS   |
| 3    | Invalid data → 422 field errors       | PASS   |
| 4    | Document results                     | PASS   |

**Overall:** ✅ All tests passed. Data binding, persistence, and validation working as designed.
