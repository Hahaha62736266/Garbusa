import { useState, useEffect } from 'react';
import { supabase } from '../supabaseClient'; // adjust path if needed
import { useToast } from './Toast';

const toast = useToast();

// after submit success:
toast.show(order ? 'Order updated!' : 'Order created!', 'success');

export default function OrderForm({ order, onSaved }) {
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const [customers, setCustomers] = useState([]);
  const [products, setProducts] = useState([]);
  const [form, setForm] = useState({
    order_id: order?.order_id || '',
    customer_id: order?.customer_id || '',
    product_id: order?.product_id || '',
    quantity: order?.quantity || '',
    total_amount: order?.total_amount || '',
    order_date: order?.order_date || new Date().toISOString().split('T')[0] // YYYY-MM-DD
  });

  // Load dropdown options
  useEffect(() => {
    const fetchRefs = async () => {
      const [cRes, pRes] = await Promise.all([
        supabase.from('customers').select('customer_id, full_name').order('full_name'),
        supabase.from('products').select('product_id, product_name').order('product_name')
      ]);
      if (cRes.data) setCustomers(cRes.data);
      if (pRes.data) setProducts(pRes.data);
    };
    fetchRefs();
  }, []);

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
      if (order) {
        // UPDATE
        result = await supabase
          .from('orders')
          .update(form)
          .eq('order_id', order.order_id);
      } else {
        // CREATE
        result = await supabase.from('orders').insert(form);
      }

      if (result.error) throw result.error;

      onSaved?.();
      if (!order) {
        setForm({
          order_id: '', customer_id: '', product_id: '',
          quantity: '', total_amount: '',
          order_date: new Date().toISOString().split('T')[0]
        });
      }
    } catch (err) {
      console.error(err);
      if (err.code === '23505') {
        setErrors({ order_id: 'This Order ID already exists' });
      } else if (err.code === '23502') {
        const field = err.message.match(/column "([^"]+)"/)?.[1];
        if (field) setErrors({ [field]: `${field.replace('_', ' ')} is required` });
      } else if (err.code === 'PGRST116') {
        setErrors({ general: 'Order not found — it may have been deleted' });
      } else {
        setErrors({ general: 'Something went wrong. Check your connection and try again.' });
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 p-4 border rounded-lg bg-white shadow-sm">
      <h3 className="font-bold text-lg">{order ? 'Edit Order' : 'Create New Order'}</h3>

      {errors.general && <p className="text-red-600 bg-red-50 p-2 rounded">{errors.general}</p>}

      <div>
        <label className="block text-sm font-medium">Order ID</label>
        <input
          name="order_id"
          value={form.order_id}
          onChange={handleChange}
          disabled={isLoading || !!order}
          className="w-full border rounded p-2 mt-1 disabled:opacity-50"
          placeholder="e.g. ORD-001"
        />
        {errors.order_id && <p className="text-red-500 text-sm mt-1">{errors.order_id}</p>}
      </div>

      <div>
        <label className="block text-sm font-medium">Customer</label>
        <select
          name="customer_id"
          value={form.customer_id}
          onChange={handleChange}
          disabled={isLoading}
          className="w-full border rounded p-2 mt-1 disabled:opacity-50"
        >
          <option value="">— Select Customer —</option>
          {customers.map(c => (
            <option key={c.customer_id} value={c.customer_id}>
              {c.full_name} ({c.customer_id})
            </option>
          ))}
        </select>
        {errors.customer_id && <p className="text-red-500 text-sm mt-1">{errors.customer_id}</p>}
      </div>

      <div>
        <label className="block text-sm font-medium">Product</label>
        <select
          name="product_id"
          value={form.product_id}
          onChange={handleChange}
          disabled={isLoading}
          className="w-full border rounded p-2 mt-1 disabled:opacity-50"
        >
          <option value="">— Select Product —</option>
          {products.map(p => (
            <option key={p.product_id} value={p.product_id}>
              {p.product_name} ({p.product_id})
            </option>
          ))}
        </select>
        {errors.product_id && <p className="text-red-500 text-sm mt-1">{errors.product_id}</p>}
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium">Quantity</label>
          <input
            type="number"
            name="quantity"
            value={form.quantity}
            onChange={handleChange}
            disabled={isLoading}
            className="w-full border rounded p-2 mt-1 disabled:opacity-50"
            min="1"
          />
          {errors.quantity && <p className="text-red-500 text-sm mt-1">{errors.quantity}</p>}
        </div>
        <div>
          <label className="block text-sm font-medium">Total Amount (₱)</label>
          <input
            type="number"
            step="0.01"
            name="total_amount"
            value={form.total_amount}
            onChange={handleChange}
            disabled={isLoading}
            className="w-full border rounded p-2 mt-1 disabled:opacity-50"
            min="0"
          />
          {errors.total_amount && <p className="text-red-500 text-sm mt-1">{errors.total_amount}</p>}
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium">Order Date</label>
        <input
          type="date"
          name="order_date"
          value={form.order_date}
          onChange={handleChange}
          disabled={isLoading}
          className="w-full border rounded p-2 mt-1 disabled:opacity-50"
        />
        {errors.order_date && <p className="text-red-500 text-sm mt-1">{errors.order_date}</p>}
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className="bg-green-600 text-white px-4 py-2 rounded font-medium disabled:opacity-50"
      >
        {isLoading ? '⏳ Saving…' : (order ? 'Update Order' : 'Create Order')}
      </button>
    </form>
  );
}
