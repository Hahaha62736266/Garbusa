// Centralized messages — no raw codes shown to users
export const messages = {
  loading: {
    saving: '⏳ Saving…',
    updating: '⏳ Updating…',
    deleting: '⏳ Deleting…',
    loading: '⏳ Loading data…'
  },
  success: {
    customerCreated: '✅ Customer added successfully!',
    customerUpdated: '✅ Customer details updated!',
    customerDeleted: '✅ Customer removed.',
    orderCreated: '✅ Order created successfully!',
    orderUpdated: '✅ Order updated!',
    orderDeleted: '✅ Order removed.'
  },
  field: {
    required: (field) => `${field} is required.`,
    min: (field, min) => `${field} must be at least ${min}.`,
    number: (field) => `${field} must be a valid number.`,
    duplicate: (field) => `${field} is already in use — please use a different value.`
  },
  global: {
    notFound: '⚠️ Record not found. It may have been removed.',
    network: '📶 Connection issue — check your internet and try again.',
    server: '⚠️ Something went wrong on our end. Please try again later.',
    generic: '❌ Unable to complete action. Please review your entries and retry.',
    retryPrompt: '🔄 Retry'
  }
};

// Map Supabase/HTTP error codes → user-friendly messages
export const interpretError = (err, fieldLabels = {}) => {
  if (!err) return null;

  // Validation / missing fields
  if (err.code === '23502' || err.status === 422) {
    const match = err.message?.match(/column "([^"]+)"/);
    const rawField = match?.[1] || 'value';
    const fieldName = fieldLabels[rawField] || rawField.replace('_', ' ');
    return { type: 'field', field: rawField, text: messages.field.required(fieldName) };
  }

  // Duplicate key
  if (err.code === '23505') {
    const match = err.message?.match(/\(([^)]+)\)/);
    const rawField = match?.[1] || 'field';
    const fieldName = fieldLabels[rawField] || rawField.replace('_', ' ');
    return { type: 'field', field: rawField, text: messages.field.duplicate(fieldName) };
  }

  // Not found
  if (err.code === 'PGRST116' || err.status === 404) {
    return { type: 'global', text: messages.global.notFound };
  }

  // Network / fetch failed
  if (err.message === 'Failed to fetch' || err.code === 'NETWORK_ERROR') {
    return { type: 'global', text: messages.global.network, canRetry: true };
  }

  // Server error
  if (err.status >= 500 || err.code === '500') {
    return { type: 'global', text: messages.global.server, canRetry: true };
  }

  // Fallback
  return { type: 'global', text: messages.global.generic, canRetry: true };
};
