// PASTE THIS ENTIRE BLOCK — your list component
import { useState, useEffect } from 'react';
import { useToast } from './Toast';

const toast = useToast();

// after delete succeeds:
toast.show('Order deleted', 'success');
export default function OrderList() {
  const [orders, setOrders] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [deletingId, setDeletingId] = useState(null);
  const [confirmDeleteId, setConfirmDeleteId] = useState(null);

  // Load list
  const loadOrders = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const res = await fetch('/api/orders');
      if (!res.ok) throw new Error('Load failed');
      setOrders(await res.json());
    } catch (err) {
      setError({
        message: 'Failed to load orders. Check your connection.',
        canRetry: true
      });
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => { loadOrders(); }, []);

  // Delete handler
  const handleDelete = async (id) => {
    if (confirmDeleteId !== id) {
      setConfirmDeleteId(id); // ask first
      return;
    }

    setDeletingId(id);
    setConfirmDeleteId(null);

    try {
      const res = await fetch(`/api/orders/${id}`, { method: 'DELETE' });
      if (!res.ok) throw new Error('Delete failed');
      setOrders(orders.filter(o => o.id !== id));
    } catch (err) {
      alert("Couldn't delete order. Please try again.");
    } finally {
      setDeletingId(null);
    }
  };

  // ---- Loading skeleton ----
  if (isLoading) {
    return (
      <div className="space-y-3 p-4">
        {[1,2,3].map(i => (
          <div key={i} className="h-14 bg-gray-200 rounded animate-pulse" />
        ))}
      </div>
    );
  }

  // ---- Error state ----
  if (error) {
    return (
      <div className="p-6 text-center">
        <p className="text-red-600 mb-3">{error.message}</p>
        {error.canRetry && (
          <button onClick={loadOrders} className="px-4 py-2 bg-blue-600 text-white rounded">
            🔄 Retry
          </button>
        )}
      </div>
    );
  }

  // ---- Empty state ----
  if (orders.length === 0) {
    return <p className="p-6 text-gray-500">No orders found.</p>;
  }

  // ---- List ----
  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Orders</h2>
      <table className="w-full border">
        <thead>
          <tr className="bg-gray-100">
            <th className="p-2 text-left">Order No</th>
            <th className="p-2 text-left">Customer</th>
            <th className="p-2 text-left">Amount</th>
            <th className="p-2 text-left">Actions</th>
          </tr>
        </thead>
        <tbody>
          {orders.map(order => (
            <tr key={order.id} className="border-t">
              <td className="p-2">{order.orderNo}</td>
              <td className="p-2">{order.customer}</td>
              <td className="p-2">₱{order.amount}</td>
              <td className="p-2">
                {confirmDeleteId !== order.id ? (
                  <button
                    onClick={() => handleDelete(order.id)}
                    disabled={deletingId === order.id}
                    className="text-red-600"
                  >
                    {deletingId === order.id ? '⏳ Deleting…' : 'Delete'}
                  </button>
                ) : (
                  <span className="space-x-2">
                    <button
                      onClick={() => handleDelete(order.id)}
                      disabled={deletingId === order.id}
                      className="text-red-600 font-bold"
                    >
                      Yes, Delete
                    </button>
                    <button onClick={() => setConfirmDeleteId(null)} className="text-gray-500">
                      Cancel
                    </button>
                  </span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
