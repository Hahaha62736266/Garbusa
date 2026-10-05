import { useState, useEffect } from 'react';
import { supabase } from '../supabaseClient';
import { useToast } from './Toast';

const toast = useToast();

import { LoadingSkeleton, ErrorMessage, EmptyState } from './FeedbackStates';

// Replace your loading block with:
if (isLoading) return <LoadingSkeleton count={3} />;

// Replace your error block with:
if (error) return <ErrorMessage message={error.message} onRetry={error.canRetry ? loadOrders : null} />;

// Replace your empty block with:
if (orders.length === 0) return <EmptyState message="No orders yet. Create your first order above." />;

// after delete succeeds:
toast.show('Customer deleted', 'success');

export default function OrderList() {
  const [orders, setOrders] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [deletingId, setDeletingId] = useState(null);
  const [confirmDeleteId, setConfirmDeleteId] = useState(null);

  const loadOrders = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const { data, error: err } = await supabase
        .from('orders')
        .select(`
          order_id,
          customer_id,
          product_id,
          quantity,
          total_amount,
          order_date
        `)
        .order('order_date', { ascending: false });

      if (err) throw err;
      setOrders(data || []);
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

  const handleDelete = async (order_id) => {
    if (confirmDeleteId !== order_id) {
      setConfirmDeleteId(order_id);
      return;
    }

    setDeletingId(order_id);
    setConfirmDeleteId(null);

    try {
      const { error: err } = await supabase
        .from('orders')
        .delete()
        .eq('order_id', order_id);

      if (err) throw err;
      setOrders(orders.filter(o => o.order_id !== order_id));
    } catch (err) {
      alert("Couldn't delete order. Please try again.");
    } finally {
      setDeletingId(null);
    }
  };

  // Loading skeleton
  if (isLoading) {
    return (
      <div className="p-4 space-y-3">
        {[1,2,3].map(i => (
          <div key={i} className="h-14 bg-gray-200 rounded animate-pulse" />
        ))}
      </div>
    );
  }

  // Error state
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

  // Empty state
  if (orders.length === 0) {
    return <p className="p-6 text-gray-500 text-center">No orders yet. Create your first order above.</p>;
  }

  // List
  return (
    <div className="p-4">
      <h3 className="font-bold text-lg mb-4">Orders ({orders.length})</h3>
      <div className="overflow-x-auto">
        <table className="w-full border text-sm">
          <thead className="bg-gray-50">
            <tr>
              <th className="p-2 text-left">Order ID</th>
              <th className="p-2 text-left">Customer ID</th>
              <th className="p-2 text-left">Product ID</th>
              <th className="p-2 text-left">Qty</th>
              <th className="p-2 text-left">Total</th>
              <th className="p-2 text-left">Date</th>
              <th className="p-2 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            {orders.map(o => (
              <tr key={o.order_id} className="border-t">
                <td className="p-2 font-mono text-xs">{o.order_id}</td>
                <td className="p-2">{o.customer_id}</td>
                <td className="p-2">{o.product_id}</td>
                <td className="p-2">{o.quantity}</td>
                <td className="p-2 font-medium">₱{Number(o.total_amount).toFixed(2)}</td>
                <td className="p-2">{o.order_date}</td>
                <td className="p-2">
                  {confirmDeleteId !== o.order_id ? (
                    <button
                      onClick={() => handleDelete(o.order_id)}
                      disabled={deletingId === o.order_id}
                      className="text-red-600 text-sm"
                    >
                      {deletingId === o.order_id ? '⏳ Deleting…' : 'Delete'}
                    </button>
                  ) : (
                    <span className="space-x-2">
                      <button
                        onClick={() => handleDelete(o.order_id)}
                        disabled={deletingId === o.order_id}
                        className="text-red-600 font-bold text-sm"
                      >
                        Yes, Delete
                      </button>
                      <button onClick={() => setConfirmDeleteId(null)} className="text-gray-500 text-sm">
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
    </div>
  );
}
