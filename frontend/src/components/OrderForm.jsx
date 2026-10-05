// PASTE THIS ENTIRE BLOCK — replaces or inserts into your form component
import { useState } from 'react';

export default function OrderForm({ initialData, onSubmitSuccess }) {
  const [isLoading, setIsLoading] = useState(false);
  const [fieldErrors, setFieldErrors] = useState({});
  const [formData, setFormData] = useState({
    orderNo: initialData?.orderNo || '',
    customer: initialData?.customer || '',
    amount: initialData?.amount || ''
    // add your other fields here
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setFieldErrors({}); // clear old errors

    try {
      const res = await fetch(
        initialData ? `/api/orders/${initialData.id}` : '/api/orders',
        {
          method: initialData ? 'PUT' : 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData)
        }
      );

      const data = await res.json();

      if (!res.ok) {
        if (res.status === 422) throw { status: 422, errors: data.errors };
        if (res.status === 404) throw { status: 404 };
        throw new Error('Server error');
      }

      onSubmitSuccess?.();
      setFormData({ orderNo: '', customer: '', amount: '' }); // reset on create
    } catch (err) {
      if (err?.status === 422) {
        setFieldErrors(err.errors); // show per-field messages
      } else if (err?.status === 404) {
        alert('Order not found — it may have been deleted');
      } else {
        alert('Something went wrong. Please check your connection and try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Order No */}
      <div>
        <label>Order No</label>
        <input
          name="orderNo"
          value={formData.orderNo}
          onChange={handleChange}
          disabled={isLoading}
          className="w-full border p-2 rounded"
        />
        {fieldErrors.orderNo && (
          <p className="text-red-500 text-sm mt-1">{fieldErrors.orderNo}</p>
        )}
      </div>

      {/* Customer */}
      <div>
        <label>Customer</label>
        <input
          name="customer"
          value={formData.customer}
          onChange={handleChange}
          disabled={isLoading}
          className="w-full border p-2 rounded"
        />
        {fieldErrors.customer && (
          <p className="text-red-500 text-sm mt-1">{fieldErrors.customer}</p>
        )}
      </div>

      {/* Amount */}
      <div>
        <label>Amount</label>
        <input
          name="amount"
          type="number"
          value={formData.amount}
          onChange={handleChange}
          disabled={isLoading}
          className="w-full border p-2 rounded"
        />
        {fieldErrors.amount && (
          <p className="text-red-500 text-sm mt-1">{fieldErrors.amount}</p>
        )}
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className="bg-blue-600 text-white px-4 py-2 rounded"
      >
        {isLoading ? '⏳ Saving…' : (initialData ? 'Update Order' : 'Create Order')}
      </button>
    </form>
  );
}
