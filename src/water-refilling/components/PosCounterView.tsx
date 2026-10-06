import { useState } from 'react';
import { ShoppingCart, Plus, X } from 'lucide-react';
import type { Customer, Product, Order } from '../types/waterRefilling';

interface Props {
  customers: Customer[];
  products: Product[];
  onNewOrder: (order: Omit<Order, 'id'>) => void;
  theme: 'light' | 'dark';
}

export function PosCounterView({ customers, products, onNewOrder, theme }: Props) {
  const [selectedCustomer, setSelectedCustomer] = useState('');
  const [selectedProduct, setSelectedProduct] = useState('');
  const [quantity, setQuantity] = useState(1);

  const product = products.find(p => p.id === selectedProduct);
  const total = product ? product.pricePerUnit * quantity : 0;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedCustomer || !selectedProduct) return;

    onNewOrder({
      customerId: selectedCustomer,
      productId: selectedProduct,
      quantity,
      totalAmount: total,
      orderDate: new Date().toISOString().split('T')[0],
      status: 'Pending',
      paymentStatus: 'Unpaid',
    });

    setSelectedCustomer('');
    setSelectedProduct('');
    setQuantity(1);
  };

  const cardClass = theme === 'dark'
    ? 'bg-gray-900 border-gray-800'
    : 'bg-white border-slate-200';

  const inputClass = theme === 'dark'
    ? 'bg-gray-800 border-gray-700 text-gray-100'
    : 'bg-slate-50 border-slate-200 text-slate-900';

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <ShoppingCart className="text-sky-500" size={24} />
        <h2 className="text-xl font-semibold">Quick POS — New Order</h2>
      </div>

      <form onSubmit={handleSubmit} className={`p-6 rounded-xl border ${cardClass} space-y-4`}>
        <div>
          <label className="block text-sm font-medium mb-1">Select Customer</label>
          <select
            value={selectedCustomer}
            onChange={e => setSelectedCustomer(e.target.value)}
            className={`w-full rounded-lg px-3 py-2 border ${inputClass}`}
            required
          >
            <option value="">— Choose customer —</option>
            {customers.map(c => (
              <option key={c.id} value={c.id}>
                {c.id} — {c.fullName} ({c.address})
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Select Product</label>
          <select
            value={selectedProduct}
            onChange={e => setSelectedProduct(e.target.value)}
            className={`w-full rounded-lg px-3 py-2 border ${inputClass}`}
            required
          >
            <option value="">— Choose product —</option>
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

        <div className={`p-4 rounded-lg ${theme === 'dark' ? 'bg-sky-900/30' : 'bg-sky-50'}`}>
          <p className="text-sm">Total Amount</p>
          <p className="text-2xl font-bold text-sky-600 dark:text-sky-400">
            ₱{total.toFixed(2)}
          </p>
        </div>

        <button
          type="submit"
          className="w-full bg-sky-600 hover:bg-sky-500 text-white py-2.5 rounded-lg font-medium transition-colors flex items-center justify-center gap-2"
        >
          <Plus size={18} /> Create Order
        </button>
      </form>
    </div>
  );
}
