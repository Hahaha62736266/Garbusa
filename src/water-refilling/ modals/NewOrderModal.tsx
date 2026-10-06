import { useState } from 'react';
import { X } from 'lucide-react';
import type { Customer, Product, Order } from '../types/waterRefilling';

interface Props {
  open: boolean;
  onClose: () => void;
  customers: Customer[];
  products: Product[];
  onSubmit: (order: Omit<Order, 'id'>) => void;
  theme: 'light' | 'dark';
}

export function NewOrderModal({ open, onClose, customers, products, onSubmit, theme }: Props) {
  const [customerId, setCustomerId] = useState('');
  const [productId, setProductId] = useState('');
  const [quantity, setQuantity] = useState(1);

  if (!open) return null;

  const product = products.find(p => p.id === productId);
  const total = product ? product.pricePerUnit * quantity : 0;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({
      customerId,
      productId,
      quantity,
      totalAmount: total,
      orderDate: new Date().toISOString().split('T')[0],
      status: 'Pending',
      paymentStatus: 'Unpaid',
    });
    setCustomerId('');
    setProductId('');
    setQuantity(1);
    onClose();
  };

  const overlayBg = theme === 'dark' ? 'bg-black/60' : 'bg-black/40';
  const modalBg = theme === 'dark' ? 'bg-gray-900 border-gray-800' : 'bg-white border-slate-200';
  const inputClass = theme === 'dark' ? 'bg-gray-800 border-gray-700' : 'bg-slate-50 border-slate-200';

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className={`absolute inset-0 ${overlayBg}`} onClick={onClose} />
      <div className={`relative w-full max-w-md rounded-xl border p-6 ${modalBg}`}>
        <div className="flex items-center justify-between mb-5">
          <h3 className="text-lg font-semibold">New Order</h3>
          <button onClick={onClose} className="p-1 rounded hover:bg-slate-100 dark:hover:bg-gray-800">
            <X size={18} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Customer</label>
            <select
              value={customerId}
              onChange={e => setCustomerId(e.target.value)}
              className={`w-full rounded-lg px-3 py-2 border ${inputClass}`}
              required
            >
              <option value="">— Select —</option>
              {customers.map(c => (
                <option key={c.id} value={c.id}>{c.id} — {c.fullName}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Product</label>
            <select
              value={productId}
              onChange={e => setProductId(e.target.value)}
              className={`w-full rounded-lg px-3 py-2 border ${inputClass}`}
              required
            >
              <option value="">— Select —</option>
              {products.map(p => (
                <option key={p.id} value={p.id}>
                  {p.id} — {p.name} — ₱{p.pricePerUnit.toFixed(2)}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Quantity</label>
            <input
              type="number"
              min={1}
              value={quantity}
              onChange={e => setQuantity(parseInt(e.target.value) || 1)}
              className={`w-full rounded-lg px-3 py-2 border ${inputClass}`}
            />
          </div>

          <div className={`p-3 rounded-lg ${theme === 'dark' ? 'bg-sky-900/30' : 'bg-sky-50'}`}>
            <p className="text-sm">Total: <span className="font-bold text-lg">₱{total.toFixed(2)}</span></p>
          </div>

          <div className="flex gap-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className={`flex-1 py-2 rounded-lg border ${inputClass}`}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="flex-1 bg-sky-600 hover:bg-sky-500 text-white py-2 rounded-lg font-medium"
            >
              Create Order
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
