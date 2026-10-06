import { useState } from 'react';
import { X } from 'lucide-react';
import type { Customer, Order, Collection } from '../types/waterRefilling';

interface Props {
  open: boolean;
  onClose: () => void;
  customers: Customer[];
  orders: Order[];
  onSubmit: (record: Omit<Collection, 'id'>) => void;
  theme: 'light' | 'dark';
}

export function ContainerReturnModal({ open, onClose, customers, orders, onSubmit, theme }: Props) {
  const [customerId, setCustomerId] = useState('');
  const [orderId, setOrderId] = useState('');
  const [emptyReturned, setEmptyReturned] = useState(0);
  const [filledReleased, setFilledReleased] = useState(0);
  const [collectedBy, setCollectedBy] = useState('');

  if (!open) return null;

  const customer = customers.find(c => c.id === customerId);
  const newBalance = customer ? customer.containerBalance - emptyReturned + filledReleased : 0;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({
      customerId,
      orderId: orderId || undefined,
      emptyJugsReturned: emptyReturned,
      filledJugsReleased: filledReleased,
      containerBalance: newBalance,
      collectionDate: new Date().toISOString().split('T')[0],
      collectedBy,
    });
    setCustomerId('');
    setOrderId('');
    setEmptyReturned(0);
    setFilledReleased(0);
    setCollectedBy('');
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
          <h3 className="text-lg font-semibold">Record Container Return & Exchange</h3>
          <button onClick={onClose} className="p-1 rounded hover:bg-slate-100 dark:hover:bg-gray-800">
            <X size={18} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Customer *</label>
            <select
              value={customerId}
              onChange={e => setCustomerId(e.target.value)}
              className={`w-full rounded-lg px-3 py-2 border ${inputClass}`}
              required
            >
              <option value="">— Select —</option>
              {customers.map(c => (
                <option key={c.id} value={c.id}>
                  {c.id} — {c.fullName} (Balance: {c.containerBalance})
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Related Order (optional)</label>
            <select
              value={orderId}
              onChange={e => setOrderId(e.target.value)}
              className={`w-full rounded-lg px-3 py-2 border ${inputClass}`}
            >
              <option value="">— None —</option>
              {orders.filter(o => o.status === 'Pending').map(o => (
                <option key={o.id} value={o.id}>{o.id} — ₱{o.totalAmount.toFixed(2)}</option>
              ))}
            </select>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Empty Jugs Returned</label>
              <input
                type="number"
                min={0}
                value={emptyReturned}
                onChange={e => setEmptyReturned(parseInt(e.target.value) || 0)}
                className={`w-full rounded-lg px-3 py-2 border ${inputClass}`}
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Filled Jugs Released</label>
              <input
                type="number"
                min={0}
                value={filledReleased}
                onChange={e => setFilledReleased(parseInt(e.target.value) || 0)}
                className={`w-full rounded-lg px-3 py-2 border ${inputClass}`}
              />
            </div>
          </div>

          <div className={`p-3 rounded-lg ${theme === 'dark' ? 'bg-sky-900/30' : 'bg-sky-50'}`}>
            <p className="text-sm">New Container Balance: <span className="font-bold text-lg">{newBalance}</span></p>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Collected By *</label>
            <input
              type="text"
              value={collectedBy}
              onChange={e => setCollectedBy(e.target.value)}
              placeholder="Staff name"
              className={`w-full rounded-lg px-3 py-2 border ${inputClass}`}
              required
            />
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
              Save Record
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
