import { useState } from 'react';
import { supabase } from '../supabaseClient'; // adjust path if needed

export default function CustomerForm({ customer, onSaved }) {
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const [form, setForm] = useState({
    customer_id: customer?.customer_id || '',
    full_name: customer?.full_name || '',
    contact_number: customer?.contact_number || '',
    address: customer?.address || ''
  });

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setErrors({ ...errors, [e.target.name]: '' });
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setIsLoading(true);
    setErrors({});

    try {
      let result;
      if (customer) {
        // UPDATE
        result = await supabase
          .from('customers')
          .update(form)
          .eq('customer_id', customer.customer_id);
      } else {
        // CREATE
        result = await supabase.from('customers').insert(form);
      }

      if (result.error) throw result.error;

      import { useToast } from './Toast'; // add at top

// inside component:
const toast = useToast();

// then in handleSubmit, after success:
toast.show(customer ? 'Customer updated!' : 'Customer added!', 'success');
onSaved?.();

  return (
    <form onSubmit={handleSubmit} className="space-y-4 p-4 border rounded-lg bg-white shadow-sm">
      <h3 className="font-bold text-lg">{customer ? 'Edit Customer' : 'Add New Customer'}</h3>

      {errors.general && <p className="text-red-600 bg-red-50 p-2 rounded">{errors.general}</p>}

      <div>
        <label className="block text-sm font-medium">Customer ID</label>
        <input
          name="customer_id"
          value={form.customer_id}
          onChange={handleChange}
          disabled={isLoading || !!customer}
          className="w-full border rounded p-2 mt-1 disabled:opacity-50"
        />
        {errors.customer_id && <p className="text-red-500 text-sm mt-1">{errors.customer_id}</p>}
      </div>

      <div>
        <label className="block text-sm font-medium">Full Name</label>
        <input
          name="full_name"
          value={form.full_name}
          onChange={handleChange}
          disabled={isLoading}
          className="w-full border rounded p-2 mt-1 disabled:opacity-50"
        />
        {errors.full_name && <p className="text-red-500 text-sm mt-1">{errors.full_name}</p>}
      </div>

      <div>
        <label className="block text-sm font-medium">Contact Number</label>
        <input
          name="contact_number"
          value={form.contact_number}
          onChange={handleChange}
          disabled={isLoading}
          className="w-full border rounded p-2 mt-1 disabled:opacity-50"
        />
        {errors.contact_number && <p className="text-red-500 text-sm mt-1">{errors.contact_number}</p>}
      </div>

      <div>
        <label className="block text-sm font-medium">Address</label>
        <textarea
          name="address"
          value={form.address}
          onChange={handleChange}
          disabled={isLoading}
          rows={2}
          className="w-full border rounded p-2 mt-1 disabled:opacity-50"
        />
        {errors.address && <p className="text-red-500 text-sm mt-1">{errors.address}</p>}
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className="bg-blue-600 text-white px-4 py-2 rounded font-medium disabled:opacity-50"
      >
        {isLoading ? '⏳ Saving…' : (customer ? 'Update Customer' : 'Add Customer')}
      </button>
    </form>
  );
}
