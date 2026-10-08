# Component Documentation — Phase 3

## Reusable Building Blocks

### StationCard
**File**: `components/StationCard.jsx`
**Used on**: Dashboard, ListView, DetailView
**Purpose**: Standard display card — one source of truth
**States**:
- Normal: Shows name, location, status, last update
- Loading: `?.` guards → "Loading..." placeholders
- Empty: Graceful fallbacks for missing fields
**AI**: Generated

### LoadingSpinner
**File**: `components/LoadingSpinner.jsx`
**Used on**: All async actions
**Purpose**: Visual feedback during pending requests
**Behavior**: Disables submit button while active
**AI**: Generated

### ErrorMessage
**File**: `components/ErrorMessage.jsx`
**Used on**: All failure paths
**Purpose**: Consistent styling + human-friendly text
**Props**: `type` → `validation`|`notfound`|`server`|`network`
**AI**: Modified — text refined to project voice

### SuccessBanner
**File**: `components/SuccessBanner.jsx`
**Used on**: Create/Update/Delete confirmations
**Purpose**: Clear positive feedback
**Auto-hide**: 3 seconds or dismiss button
**AI**: Generated

### FormWrapper
**File**: `components/FormWrapper.jsx`
**Used on**: CreateStationForm, EditStationForm
**Purpose**: Shared layout, disabled state during submit
**AI**: Hand-written

## Page-Level Views

| View | File | States Handled | AI? |
|---|---|---|---|
| List / Index | `ListView.jsx` | Loading, Empty, Data, Error | Modified |
| Detail | `DetailView.jsx` | Loading, 404, Data, Error | Generated |
| Create | `CreateView.jsx` | Form, Submitting, Success, Validation Errors | Generated |
| Edit | `EditView.jsx` | Loading, 404, Form, Submitting, Success | Generated |

## Form Bindings
- **Create**: `POST /api/station` → async → onSuccess() redirects to Detail
- **Update**: `PUT /api/station/:id` → async → onSuccess() refreshes in place
- **Delete**: `DELETE /api/station/:id` → async → onSuccess() redirects to List
- All prevent double-submit → button disabled while loading
