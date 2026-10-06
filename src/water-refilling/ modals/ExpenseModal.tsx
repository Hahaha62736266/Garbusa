import { useState } from 'react';
import { X } from 'lucide-react';
import type { Expense } from '../types/waterRefilling';

interface Props {
  open: boolean;
  onClose: () => void;
  onSubmit: (expense: Omit<Expense, 'id'>) => void;
  theme: 'light' | 'dark';
}

export function ExpenseModal({ open, onClose, onSubmit, theme }: Props) {
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
  const [category, setCategory] = useState('');
  const [description, setDescription] = useState('');
  const [amount, setAmount] = useState(0);

  if (!open) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({ date, category, description, amount });
    setDate(new Date().toISOString().split('T')[0]);
    setCategory('');
    setDescription('');
    setAmount(0);
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
          <h3 className="text-lg font-semibold">Record Expense</h3>
          <button onClick={onClose} className="p-1 rounded hover:bg-slate-100 dark:hover:bg-gray-800">
            <X size={18} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Date</label>
            <input
              type="date"
              value={date}
              onChange={e => setDate(e.target.value)}
              className={`w-full rounded-lg px-3 py-2 border ${inputClass}`}
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Category</label>
            <select
              value={category}
              onChange={e => setCategory(e.target.value)}
              className={`w-full rounded-lg px-3 py-2 border ${inputClass}`}
              required
            >
              <option value="">— Select —</option>
              <option value="Electricity">Electricity</option>
              <option value="Water">Water Utility</option>
              <option value="Supplies">Supplies</option>
              <option value="Maintenance">Maintenance</option>
              <option value="Wages">Wages</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Description</label>
            <input
              type="text"
              value={description}
              onChange={e => setDescription(e.target.value)}
              placeholder="Brief description"
              className={`w-full rounded-lg px-3 py-2 border ${inputClass}`}
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Amount (₱)</label>
            <input
              type="number"
              min={0}
              step="0.01"
              value={amount || ''}
              onChange={e => setAmount(parseFloat(e.target.value) || 0)}
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
              Save Expense
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
