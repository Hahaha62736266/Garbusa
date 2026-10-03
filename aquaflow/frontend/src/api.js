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
  
  // Orders
  getOrders: () => fetchData('/orders'),
  createOrder: (order) => postData('/orders', order),
  updateOrderStatus: (id, status) => postData(`/orders/${id}/status`, { status }),
  updatePaymentStatus: (id, status) => postData(`/orders/${id}/payment`, { status }),
  
  // Inventory & Station
  getStationStatus: () => fetchData('/station'),
  updateMeters: (raw, purified) => postData('/station/meters', { raw, purified }),
  
  // Expenses
  getExpenses: () => fetchData('/expenses'),
  addExpense: (exp) => postData('/expenses', exp),
  
  // Container Returns
  recordReturn: (custId, slim, round) => 
    postData(`/customers/${custId}/return`, { slim_returned: slim, round_returned: round })
};
