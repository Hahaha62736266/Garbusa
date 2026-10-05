import { useState, useEffect } from 'react';
import { supabase } from '../supabaseClient';

export default function CustomerList() {
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
      setError({ message: 'Failed to load customers. Check your connection.', canRetry: true });
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
    } catch (err) {
      alert("Couldn't delete customer. Please try again.");
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
          <button onClick={loadCustomers} className="px-4 py-2 bg-blue-600 text-white rounded">
            🔄 Retry
          </button>
        )}
      </div>
    );
  }

  // Empty state
  if (customers.length === 0) {
    return <p className="p-6 text-gray-500 text-center">No customers yet. Add your first customer above.</p>;
  }

  // List
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
                      className="text-red-600 text-sm"
                    >
                      {deletingId === c.customer_id ? '⏳ Deleting…' : 'Delete'}
                    </button>
                  ) : (
                    <span className="space-x-2">
                      <button
                        onClick={() => handleDelete(c.customer_id)}
                        disabled={deletingId === c.customer_id}
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
