// ==========================================
// AquaFlow API Client — Connects React → Flask
// ==========================================
const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000/api';

// Helper: GET
async function fetchData(endpoint) {
  const res = await fetch(`${API_BASE}${endpoint}`);
  if (!res.ok) throw new Error(`API Error: ${res.status}`);
  return res.json();
}

// Helper: POST
async function postData(endpoint, payload) {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error(`API Error: ${res.status}`);
  return res.json();
}

export const api = {
  // Customers
  getCustomers: () => fetchData('/customers'),
  updateCustomer: (id, data) => postData(`/customers/${id}`, data),
  recordReturn: (custId, slimReturned, roundReturned) =>
    postData(`/customers/${custId}/return`, { slim_returned: slimReturned, round_returned: roundReturned }),

  // Orders
  getOrders: () => fetchData('/orders'),
  createOrder: (order) => postData('/orders', order),
  updateOrderStatus: (id, status) => postData(`/orders/${id}/status`, { status }),
  updatePaymentStatus: (id, paymentStatus) => postData(`/orders/${id}/payment`, { payment_status: paymentStatus }),

  // Station & Monitor
  getStationStatus: () => fetchData('/station'),
  updateMeters: (rawReading, purifiedReading) =>
    postData('/station/meters', { raw_water_meter: rawReading, purified_water_meter: purifiedReading }),

  // Expenses
  getExpenses: () => fetchData('/expenses'),
  addExpense: (expense) => postData('/expenses', expense),
};
