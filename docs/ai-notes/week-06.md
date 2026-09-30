# Week 06 — AI Usage Log
**Project:** Garbusa / Aquaflow Tracker
**Date:** 2026-09-30
**Focus:** Task 3 — Render States; Task 4 — AI Scaffolding & Review

---

## 🤖 Prompt Log

### Prompt 1 — Scaffold State Templates
> *"Write a Jinja2 template for a customer list page with 3 conditional states: empty (zero records), loading (spinner while fetching), and error (message on failure). Use Flask templating, match a clean modern design, and include JavaScript to simulate loading state."*

**AI Output:**
- Complete `list.html` structure with `{% if %}` conditionals
- CSS class naming system (`empty-state__title`, `loading-container`, etc.)
- JavaScript DOM ready handler with simulated delay

**Reviewed & Fixed:** ✅
- Added `extends "base.html"` to inherit shared layout
- Corrected variable names to match project (`customers` → not `items`)
- Fixed loading display logic to only show when no data
- Added proper page title and navigation links
- Adjusted button styling to match existing `.af-btn` system

**Status:** AI-scaffolded → human-reviewed → corrected → deployed ✅

---

### Prompt 2 — Generate State Styles
> *"Write CSS for empty/loading/error states. Use theme colors: primary #2563eb, success #16a34a, error #dc2626. Spinner should animate smoothly. Empty state: dashed border, centered icon + message. Error: red left border banner."*

**AI Output:**
- Spinner animation using `@keyframes spin`
- Empty state layout with flex centering
- Error state with accent border

**Reviewed & Fixed:** ✅
- Standardized class names to BEM format
- Adjusted padding/margin values to match wireframe spacing
- Removed unused properties; kept styles lean
- Verified responsive behavior on mobile widths

**Status:** AI-generated → human-tweaked → merged ✅

---

### Prompt 3 — Route Error Handling
> *"Update a Flask route to catch exceptions, pass error message to template, return HTTP 500 status."*

**AI Output:**
- `try/except` block wrapping controller call
- `render_template(..., error=str(e)), 500` pattern

**Reviewed & Fixed:** ✅
- Wrapped existing `customers_page()` route without breaking imports
- Preserved existing API routes — no regression
- Tested: raises exception → error banner displays ✅

**Status:** AI-assisted → integrated manually ✅

---

## 📊 Component Attribution

| Component | Source | Notes |
|---|---|---|
| `screens.css` — State styles | 🤖 AI-generated + ✏️ Modified | Tweaked spacing, standardized classes |
| `list.html` — Base structure | 🤖 AI-scaffolded + ✏️ Modified | Added base layout, fixed var names, nav |
| `list.html` — Loading JS | 🤖 AI-generated + ✏️ Modified | Adjusted trigger logic |
| `list.html` — Empty/Error blocks | 🤖 AI-scaffolded + ✏️ Reviewed | Verified against wireframe |
| `app.py` — Route logic | ✍️ Hand-written / AI-assisted | Integrated into existing app |
| `index.html` Dashboard | ✍️ Hand-written | Custom design |
| `create.html` Form | ✍️ Hand-written | Full control flow |

---

## 🧠 Reflection — How AI Helped
- **Speed:** Scaffolded template structure in seconds vs. 15+ min writing from scratch
- **Consistency:** Generated consistent class naming system early → easier to maintain
- **Learning:** Saw `animation` + `@keyframes` pattern → reused elsewhere
- **Ownership:** Every AI output reviewed; all changes understood and tested. No "black box" code merged.

---

## ✅ Verification
- [ ] Empty state visible with 0 records → **Yes**
- [ ] Loading spinner appears briefly → **Yes**
- [ ] Error state shows on exception → **Yes**
- [ ] All AI prompts recorded → **Yes**
- [ ] Attribution table complete → **Yes**
- [ ] Pushed to feature branch → **Yes**
