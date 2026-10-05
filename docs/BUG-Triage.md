# Bug Triage & Sprint Priority Summary
**Project**: AquaFlow Water Refilling Station Management
**Lab**: Week 10 — QA & Bug Hunting
**Date**: 2026-10-05
**Phase**: Feature Freeze → Fix Sprint

---

## Priority Legend
| Label | Meaning | Fix Order |
|---|---|---|
| **P0 — Critical** | Security breach / core function dead / data loss → FIX FIRST | 🔴 1st |
| **P1 — High** | Major feature broken / calculation wrong → Fix this week | 🟠 2nd |
| **P2 — Low** | Cosmetic / UX polish / rare edge → Fix last | 🟢 3rd |

---

## 🔴 P0 — Critical (Fix Immediately — Blocking Defense)
> Address before anything else. These affect security or core access.

| # | Bug Title | Row | Impact | Est. Effort |
|---|---|---|---|---|
| #1 | Login accepts blank password — grants full dashboard access | 1 | **Security** — anyone can log in without password | 15 min |

### Action Plan — P0
- [ ] Add required field validation on password input
- [ ] Block login request when password is empty
- [ ] Re-test: blank password → stays on login with error message

---

## 🟠 P1 — High (Fix This Week — Core Functionality)
> Major data integrity or user experience issues. Must fix before demo.

| # | Bug Title | Row | Impact | Est. Effort |
|---|---|---|---|---|
| #2 | Water reading accepts negative values → saves to DB | 4 | **Data integrity** — totals become negative | 20 min |
| #4 | Registration allows duplicate username → conflict | 2 | **Account integrity** — duplicate accounts | 25 min |
| #5 | Dashboard infinite load with large dataset | 3 | **Performance** — unusable with real data | 1–2 hr |
| #6 | Customer Profile saves with blank address → search broken | 5 | **Data quality** — customer records incomplete | 20 min |
| #7 | Password update accepts mismatched confirmation → lockout risk | 7 | **Usability/Security** — user gets locked out | 20 min |
| #9 | Concurrent rapid saves → duplicate entries | 9 | **Data integrity** — inflated readings | 30 min |

### Action Plan — P1
- [ ] **Data validation**: min/max checks on readings; required address field; password match check
- [ ] **Uniqueness**: username/customer name duplicate check on register
- [ ] **Performance**: add pagination or lazy loading to dashboard; optimize query
- [ ] **Concurrency**: disable button on submit; add unique constraint on reading timestamp+user
- [ ] Re-test each → mark closed in GitHub → update matrix Status ✅

---

## 🟢 P2 — Low (Polish Last — Does Not Block Defense)
> Cosmetic, UX feedback, edge cases. Can ship then iterate.

| # | Bug Title | Row | Impact | Est. Effort |
|---|---|---|---|---|
| #3 | "Export CSV" button overlaps on mobile ≤ 480px | 6 | Layout only — function works | 15 min |
| #8 | Special/empty search → no "No results" message | 8 | UX clarity — safe but confusing | 15 min |
| #10 | Direct admin route → blank page, no permission message | 10 | UX clarity — not secure issue since content blocked | 20 min |
| #11 | Double-click submit → duplicate entries created | 11 | UX — annoyance | 15 min |

### Action Plan — P2
- [ ] Mobile responsive CSS fixes
- [ ] Empty/no-results state messages in search
- [ ] Route guard redirect + friendly error text
- [ ] Disable submit button on click until response returns

---

## 📈 Sprint Summary
| Severity | Count | Est. Total Effort | Target Status |
|---|---|---|---|
| P0 | 1 | 15 min | Done first |
| P1 | 6 | ~4 hr | Complete by mid-week |
| P2 | 4 | ~1.5 hr | Polish last |
| **Total** | **11** | **~5.5 hr** | Ready for defense |

---

## ✅ Closing Checklist — Before Defense
- [ ] All P0 → P1 fixed & pushed to `main`
- [ ] All issues closed in GitHub
- [ ] `docs/test-matrix.md` updated: Status ✅ + Bug Ref = Fixed/Closed
- [ ] Brief notes added: How you fixed each → for defense explanation
- [ ] Final test pass by all members → sign-off

---

## 💡 Defense Talking Points
> Be ready to say:
- "We found **11 issues** during Week 10 QA — 1 critical security, 6 high-impact data/performance, 4 UX polish"
- "P0 blank password was highest priority — immediate validation fix"
- "Dashboard performance will scale with pagination — that's why it's P1"
- "P2 items are cosmetic — app functions correctly; those are polish tasks"
- "We did **not** fix during Week 10 per lab instructions — logged only"
