# Component Inventory — Aquaflow Tracker
> Generated: 2026-09-30 | Lab: Building Your Views

## Reusable Components
1. **Navbar** — Global navigation, role, logout
2. **PageHeader** — Title + subtitle + action button
3. **CustomerCard** — Profile summary with gallon balance
4. **OrderListItem** — Single order row (MOST REUSED)
5. **StatusBadge** — Dynamic status label
6. **ProductCard** — Product info with stock
7. **CollectionLogItem** — Container exchange record
8. **DataTable** — Sortable, paginated table wrapper
9. **FormGroup** — Consistent input layout with validation
10. **EmptyState** — "No data" friendly view
11. **LoadingSpinner** — Async feedback
12. **ErrorAlert** — Inline error with retry
13. **Footer** — Attribution & version

## Screen Mapping
- Dashboard → Navbar, PageHeader, OrderListItem, CustomerCard, StatusBadge, Footer
- Customers → Navbar, PageHeader, CustomerCard, DataTable, EmptyState, LoadingSpinner, Footer
- Products → Navbar, PageHeader, ProductCard, StatusBadge, DataTable, ErrorAlert, Footer
- Orders → Navbar, PageHeader, OrderListItem, StatusBadge, DataTable, LoadingSpinner, EmptyState, Footer
- New Order → Navbar, PageHeader, FormGroup, ProductCard, Footer
- Collections → Navbar, PageHeader, CollectionLogItem, StatusBadge, DataTable, ErrorAlert, Footer
- Profile → Navbar, PageHeader, CustomerCard, OrderListItem, CollectionLogItem, FormGroup, Footer
- Reports → Navbar, PageHeader, DataTable, LoadingSpinner, EmptyState, Footer

## Priority Build Order
1. OrderListItem (highest reuse — appears on 5+ screens)
2. StatusBadge
3. Navbar
4. PageHeader
5. Empty/Loading/Error states
6. CustomerCard, ProductCard, CollectionLogItem
7. DataTable, FormGroup
8. Footer
