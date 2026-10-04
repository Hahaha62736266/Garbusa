# AI Prompt Log — Week 10
**Lab**: Manual QA & Bug Hunting | Feature Freeze — Log Only
**Date**: 2026-10-05 | Team: 5 Members
**Requirement**: Log every prompt used for test scaffolding — do not omit

---

## Log Table
| # | Timestamp | Prompt / AI Request | AI Tool Used | Output Received | Used In |
|---|---|---|---|---|---|
| 1 | 07:38 | Build a test matrix for a water management app (AquaFlow/Garbusa): list features as rows; columns = happy path, boundary, invalid, empty/null, permissions. Include status key and severity labels P0/P1/P2. Save as Markdown. | Assistant | Initial test matrix structure | `/docs/test-matrix.md` Task 1 |
| 2 | 07:41 | Expand that test matrix with full, ready-to-run test cases for every cell — no vague descriptions. Include login, registration, dashboard, water readings, farmer profiles, reports, settings, search, Supabase sync, UI, adversarial & network. Assign to 5 members. | Assistant | Full test cases + assignment sheet | `/docs/test-matrix.md` Task 2–4 |
| 3 | 07:44 | Provide filled ai-notes/week-10.md log with example prompts matching today's lab work — formatted and ready to commit. | Assistant | This file | `/docs/ai-notes/week-10.md` |
| 4 |  | 🔄 Add your own prompts below as you work — copy & extend this row | — | — | — |
| 5 |  |  |  |  |  |
| 6 |  |  |  |  |  |

---

## Prompt Reference — Common Ones You May Use Today
Add these to the table above if you run them:

### Automated Test Scaffolding
> "Write JavaScript/Jest test cases for login validation: reject blank email, reject blank password, reject duplicate email registration. Keep it simple — cover critical paths only."

### Bug Report Drafting
> "Turn these reproduction steps into a concise bug report title + description suitable for a GitHub issue — include expected vs actual result and P0/P1/P2 recommendation."

### Adversarial Test Ideas
> "List 10 weird/aggressive inputs I should throw at form fields to break a web app — include XSS patterns, emoji, oversized text, special chars, and edge numbers."

### Network / Offline Testing
> "How to simulate slow 3G and offline in Chrome DevTools — what should I check to make sure the app degrades gracefully?"

---

## End-of-Lab Confirmation
- [ ] All prompts logged above — no blanks
- [ ] Timestamp column filled for every entry
- [ ] File committed with message: `docs: add week-10 AI prompt log`
- [ ] Reviewed by team lead before submitting

---

## Reminder
- AI is for **scaffolding/test ideas only** — you design the QA, you run the tests
- Do NOT use AI to fix bugs this week — log only
- Every team member adds their own prompts — do not leave this file to one person
