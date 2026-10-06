import { BarChart3, PlusCircle, TrendingUp, TrendingDown, DollarSign } from 'lucide-react';
import type { DailySummary, Expense, MeterReading } from '../types/waterRefilling';

interface Props {
  dailySummary: DailySummary;
  expenses: Expense[];
  meterReadings: MeterReading[];
  onAddExpense: () => void;
  theme: 'light' | 'dark';
}

export function FinancialsView({ dailySummary, expenses, meterReadings, onAddExpense, theme }: Props) {
  const cardClass = theme === 'dark' ? 'bg-gray-900 border-gray-800' : 'bg-white border-slate-200';

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <BarChart3 className="text-sky-500" size={24} />
          <h2 className="text-xl font-semibold">Financial Overview</h2>
        </div>
        <button
          onClick={onAddExpense}
          className="flex items-center gap-2 bg-sky-600 hover:bg-sky-500 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
        >
          <PlusCircle size={16} /> Add Expense
        </button>
      </div>

      {/* Daily Summary */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className={`p-4 rounded-xl border ${cardClass}`}>
          <div className="flex items-center gap-2 text-emerald-500 mb-2">
            <TrendingUp size={18} />
          </div>
          <p className="text-sm text-slate-500 dark:text-gray-400">Total Sales</p>
          <p className="text-lg font-bold">₱{dailySummary.totalSales.toFixed(2)}</p>
        </div>
        <div className={`p-4 rounded-xl border ${cardClass}`}>
          <div className="flex items-center gap-2 text-sky-500 mb-2">
            <DollarSign size={18} />
          </div>
          <p className="text-sm text-slate-500 dark:text-gray-400">Collections</p>
          <p className="text-lg font-bold">₱{dailySummary.totalCollections.toFixed(2)}</p>
        </div>
        <div className={`p-4 rounded-xl border ${cardClass}`}>
          <div className="flex items-center gap-2 text-red-500 mb-2">
            <TrendingDown size={18} />
          </div>
          <p className="text-sm text-slate-500 dark:text-gray-400">Expenses</p>
          <p className="text-lg font-bold">₱{dailySummary.totalExpenses.toFixed(2)}</p>
        </div>
        <div className={`p-4 rounded-xl border ${cardClass} ${
          dailySummary.netIncome >= 0
            ? 'border-emerald-500/50 bg-emerald-500/5'
            : 'border-red-500/50 bg-red-500/5'
        }`}>
          <p className="text-sm text-slate-500 dark:text-gray-400">Net Income</p>
          <p className={`text-lg font-bold ${
            dailySummary.netIncome >= 0 ? 'text-emerald-600 dark:text-emerald-400' : 'text-red-600 dark:text-red-400'
          }`}>
            ₱{dailySummary.netIncome.toFixed(2)}
          </p>
        </div>
      </div>

      {/* Expense Table */}
      <div className={`p-5 rounded-xl border ${cardClass}`}>
        <h3 className="font-semibold mb-4">Expense Log</h3>
        {expenses.length === 0 ? (
          <p className="text-slate-500 italic">No expenses recorded.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className={theme === 'dark' ? 'bg-gray-800 text-gray-300' : 'bg-slate-50 text-slate-600'}>
                  <th className="px-3 py-2 text-left">Date</th>
                  <th className="px-3 py-2 text-left">Category</th>
                  <th className="px-3 py-2 text-left">Description</th>
                  <th className="px-3 py-2 text-right">Amount</th>
                </tr>
              </thead>
              <tbody>
                {expenses.map(e => (
                  <tr key={e.id} className={`border-t ${theme === 'dark' ? 'border-gray-800' : 'border-slate-200'}`}>
                    <td className="px-3 py-2">{e.date}</td>
                    <td className="px-3 py-2 font-medium">{e.category}</td>
                    <td className="px-3 py-2">{e.description}</td>
                    <td className="px-3 py-2 text-right font-medium">₱{e.amount.toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Water Cost Summary */}
      <div className={`p-5 rounded-xl border ${cardClass}`}>
        <h3 className="font-semibold mb-4">Water Utility Cost</h3>
        {meterReadings.length === 0 ? (
          <p className="text-slate-500 italic">No meter readings yet.</p>
        ) : (
          <div className="space-y-3">
            {meterReadings.map(m => (
              <div key={m.id} className="flex justify-between items-center text-sm">
                <span>{m.date} · {m.cubicMetersUsed} m³</span>
                <span className="font-medium">₱{m.totalCost.toFixed(2)}</span>
              </div>
            ))}
            <div className="flex justify-between items-center pt-3 border-t font-semibold">
              <span>Total Water Cost</span>
              <span>₱{meterReadings.reduce((s, m) => s + m.totalCost, 0).toFixed(2)}</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
