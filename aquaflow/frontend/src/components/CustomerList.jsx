import { useState, useEffect } from 'react';
import { supabase } from '../supabaseClient';
import { useToast } from './Toast';
import { messages } from '../utils/messages';
import { LoadingSkeleton, ErrorMessage, EmptyState } from './FeedbackStates';

export default function CustomerList() {
  const toast = useToast();
  const [customers, setCustomers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [deletingId, setDeletingId] = useState(null);
  const [confirmDeleteId, setConfirmDeleteId] = useState(null);

  const loadCustomers = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const { data, error: err } = await supabase
        .from('customers')
        .select('*')
        .order('full_name');

      if (err) throw err;
      setCustomers(data || []);
    } catch (err) {
      setError({ message: messages.global.network, canRetry: true });
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => { loadCustomers(); }, []);

  const handleDelete = async (customer_id) => {
    if (confirmDeleteId !== customer_id) {
      setConfirmDeleteId(customer_id);
      return;
    }

    setDeletingId(customer_id);
    setConfirmDeleteId(null);

    try {
      const { error: err } = await supabase
        .from('customers')
        .delete()
        .eq('customer_id', customer_id);

      if (err) throw err;
      setCustomers(customers.filter(c => c.customer_id !== customer_id));
      toast.show(messages.success.customerDeleted);
    } catch (err) {
      toast.show(messages.global.generic, 'error');
    } finally {
      setDeletingId(null);
    }
  };

  if (isLoading) return <LoadingSkeleton count={3} />;

  if (error) return <ErrorMessage message={error.message} onRetry={error.canRetry ? loadCustomers : null} />;

  if (customers.length === 0) return <EmptyState message="No customers yet. Add your first customer above." />;

  return (
    <div className="p-4">
      <h3 className="font-bold text-lg mb-4">Customers ({customers.length})</h3>
      <div className="overflow-x-auto">
        <table className="w-full border text-sm">
          <thead className="bg-gray-50">
            <tr>
              <th className="p-2 text-left">Customer ID</th>
              <th className="p-2 text-left">Full Name</th>
              <th className="p-2 text-left">Contact</th>
              <th className="p-2 text-left">Address</th>
              <th className="p-2 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            {customers.map(c => (
              <tr key={c.customer_id} className="border-t">
                <td className="p-2 font-mono text-xs">{c.customer_id}</td>
                <td className="p-2 font-medium">{c.full_name}</td>
                <td className="p-2">{c.contact_number}</td>
                <td className="p-2 max-w-xs truncate">{c.address}</td>
                <td className="p-2">
                  {confirmDeleteId !== c.customer_id ? (
                    <button
                      onClick={() => handleDelete(c.customer_id)}
                      disabled={deletingId === c.customer_id}
                      className="text-red-600 text-sm disabled:opacity-50"
                    >
                      {deletingId === c.customer_id ? messages.loading.deleting : 'Delete'}
                    </button>
                  ) : (
                    <span className="space-x-2">
                      <button
                        onClick={() => handleDelete(c.customer_id)}
                        disabled={deletingId === c.customer_id}
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
