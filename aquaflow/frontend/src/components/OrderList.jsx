import { useState, useEffect } from 'react';
import { supabase } from '../supabaseClient';
import { useToast } from './Toast';
import { messages } from '../utils/messages';
import { LoadingSkeleton, ErrorMessage, EmptyState } from './FeedbackStates';

export default function OrderList() {
  const toast = useToast();
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
        .select('order_id, customer_id, product_id, quantity, total_amount, order_date')
        .order('order_date', { ascending: false });

      if (err) throw err;
      setOrders(data || []);
    } catch (err) {
      setError({ message: messages.global.network, canRetry: true });
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
      toast.show(messages.success.orderDeleted);
    } catch (err) {
      toast.show(messages.global.generic, 'error');
    } finally {
      setDeletingId(null);
    }
  };

  if (isLoading) return <LoadingSkeleton count={3} />;

  if (error) return <ErrorMessage message={error.message} onRetry={error.canRetry ? loadOrders : null} />;

  if (orders.length === 0) return <EmptyState message="No orders yet. Create your first order above." />;

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
                      className="text-red-600 text-sm disabled:opacity-50"
                    >
                      {deletingId === o.order_id ? messages.loading.deleting : 'Delete'}
                    </button>
                  ) : (
                    <span className="space-x-2">
                      <button
                        onClick={() => handleDelete(o.order_id)}
                        disabled={deletingId === o.order_id}
                        className="text-red-600 font-bold text-sm disabled:opacity-50"
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
