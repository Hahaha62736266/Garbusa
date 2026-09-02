       [CLIENT REQUEST]
             │
             ▼
    ┌──────────────────┐
    │   ROUTE LAYER    │ ← routes/*.py — maps URL → handler
    └────────┬─────────┘
             │
    ┌────────▼─────────┐
    │  VALIDATION      │ ← middleware/validation.py
    │  → Return 422    │   if bad data
    └────────┬─────────┘ ✅ Clean data attached to request.validatedBody
             │
    ┌────────▼─────────┐
    │ AUTHORIZATION    │ ← middleware/validation.py (DELETE only)
    │  → Return 403    │   if not owner
    └────────┬─────────┘ ✅ Permission granted
             │
    ┌────────▼─────────┐
    │  CONTROLLER      │ ← controllers/*_controller.py — THIN
    │  request.validatedBody
    │  → Model.save()
    └────────┬─────────┘
             │
    ┌────────▼─────────┐
    │  DATA LAYER      │ ← models/*_model.py — DB work
    └────────┬─────────┘
             │
    ┌────────▼─────────┐
    │   RESPONSE       │ ← { status, data, error }
    └───────────────────┘
