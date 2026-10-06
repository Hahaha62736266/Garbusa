import { useState, useMemo } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

function FinancialsView({ isDark, cardBg, subText, orders, expenses, onOpenAddExpense }) {
  const [selectedMonth, setSelectedMonth] = useState('all');

  // Build list of available months from data
  const availableMonths = useMemo(() => {
    const months = new Set();
    [...orders, ...expenses].forEach(item => {
      const date = new Date(item.date || item.createdAt);
      if (!isNaN(date.getTime())) {
        months.add(date.toISOString().slice(0, 7)); // YYYY-MM
      }
    });
    return Array.from(months).sort().reverse();
  }, [orders, expenses]);

  // Filter by selected month
  const filteredOrders = useMemo(() => {
    if (selectedMonth === 'all') return orders;
    return orders.filter(o => {
      const date = new Date(o.date || o.createdAt);
      return !isNaN(date.getTime()) && date.toISOString().slice(0, 7) === selectedMonth;
    });
  }, [orders, selectedMonth]);

  const filteredExpenses = useMemo(() => {
    if (selectedMonth === 'all') return expenses;
    return expenses.filter(e => {
      const date = new Date(e.date);
      return !isNaN(date.getTime()) && date.toISOString().slice(0, 7) === selectedMonth;
    });
  }, [expenses, selectedMonth]);

  // Calculations
  const totalRevenue = filteredOrders.reduce((sum, o) => sum + (o.paymentStatus === 'Paid' ? o.totalAmount : 0), 0);
  const totalExpenses = filteredExpenses.reduce((sum, e) => sum + e.amount, 0);
  const netProfit = totalRevenue - totalExpenses;

  // Chart data: daily profit for selected month
  const chartData = useMemo(() => {
    const daily = {};
    filteredOrders.forEach(o => {
      if (o.paymentStatus !== 'Paid') return;
      const d = new Date(o.date || o.createdAt).toLocaleDateString('en-PH', { day: '2-digit', month: 'short' });
      daily[d] = daily[d] || { revenue: 0, expenses: 0 };
      daily[d].revenue += o.totalAmount;
    });
    filteredExpenses.forEach(e => {
      const d = new Date(e.date).toLocaleDateString('en-PH', { day: '2-digit', month: 'short' });
      daily[d] = daily[d] || { revenue: 0, expenses: 0 };
      daily[d].expenses += e.amount;
    });
    return Object.entries(daily).map(([date, vals]) => ({
      date,
      profit: vals.revenue - vals.expenses
    }));
  }, [filteredOrders, filteredExpenses]);

  return (
    <div className="space-y-6">
      {/* Month Filter */}
      <div className="flex items-center justify-between">
        <h2 className={`text-xl font-bold ${isDark ? 'text-white' : 'text-gray-900'}`}>Financial Overview</h2>
        <select
          value={selectedMonth}
          onChange={(e) => setSelectedMonth(e.target.value)}
          className={`px-3 py-2 rounded-lg border text-sm ${
            isDark ? 'bg-gray-800 border-gray-700 text-white' : 'bg-white border-gray-300 text-gray-900'
          }`}
        >
          <option value="all">All Time</option>
          {availableMonths.map(m => (
            <option key={m} value={m}>{m}</option>
          ))}
        </select>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className={`p-5 rounded-xl shadow-sm ${cardBg}`}>
          <h3 className={`text-sm font-medium ${subText}`}>Total Revenue</h3>
          <p className="text-2xl font-bold mt-1 text-green-500">
            ₱{totalRevenue.toLocaleString('en-PH', { minimumFractionDigits: 2 })}
          </p>
        </div>

        <div className={`p-5 rounded-xl shadow-sm ${cardBg}`}>
          <h3 className={`text-sm font-medium ${subText}`}>Total Expenses</h3>
          <p className="text-2xl font-bold mt-1 text-red-500">
            ₱{totalExpenses.toLocaleString('en-PH', { minimumFractionDigits: 2 })}
          </p>
        </div>

        <div className={`p-5 rounded-xl shadow-sm ${cardBg}`}>
          <h3 className={`text-sm font-medium ${subText}`}>Net Profit</h3>
          <p className={`text-2xl font-bold mt-1 ${netProfit >= 0 ? 'text-green-500' : 'text-red-500'}`}>
            ₱{netProfit.toLocaleString('en-PH', { minimumFractionDigits: 2 })}
          </p>
        </div>
      </div>

      {/* Profit Trend Chart */}
      <div className={`p-5 rounded-xl shadow-sm ${cardBg}`}>
        <h3 className={`text-lg font-semibold mb-4 ${isDark ? 'text-white' : 'text-gray-900'}`}>Profit Trend</h3>
        {chartData.length > 0 ? (
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke={isDark ? '#374151' : '#e5e7eb'} />
              <XAxis dataKey="date" stroke={isDark ? '#9ca3af' : '#6b7280'} fontSize={12} />
              <YAxis stroke={isDark ? '#9ca3af' : '#6b7280'} fontSize={12} />
              <Tooltip
                formatter={(value) => [`₱${value.toLocaleString('en-PH', { minimumFractionDigits: 2 })}`, 'Net Profit']}
                contentStyle={{
                  backgroundColor: isDark ? '#1f2937' : '#fff',
                  border: 'none', borderRadius: '8px',
                  color: isDark ? '#fff' : '#111'
                }}
              />
              <Line
                type="monotone"
                dataKey="profit"
                stroke="#10b981"
                strokeWidth={3}
                dot={{ fill: '#10b981', strokeWidth: 2 }}
                activeDot={{ r: 6 }}
              />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <p className={subText}>No data available for the selected period.</p>
        )}
      </div>

      {/* Expenses Table */}
      <div className={`p-5 rounded-xl shadow-sm ${cardBg}`}>
        <div className="flex items-center justify-between mb-4">
          <h3 className={`text-lg font-semibold ${isDark ? 'text-white' : 'text-gray-900'}`}>Expense Records</h3>
          <button
            onClick={onOpenAddExpense}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium transition-colors"
          >
            + Add Expense
          </button>
        </div>

        {filteredExpenses.length === 0 ? (
          <p className={subText}>No expenses recorded for this period.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className={`border-b ${isDark ? 'border-gray-700' : 'border-gray-200'}`}>
                  <th className={`py-2 text-sm font-medium ${subText}`}>Description</th>
                  <th className={`py-2 text-sm font-medium ${subText}`}>Amount</th>
                  <th className={`py-2 text-sm font-medium ${subText}`}>Date</th>
                </tr>
              </thead>
              <tbody>
                {filteredExpenses.map((expense, idx) => (
                  <tr key={idx} className={`border-b ${isDark ? 'border-gray-800' : 'border-gray-100'}`}>
                    <td className={`py-3 text-sm ${isDark ? 'text-white' : 'text-gray-900'}`}>
                      {expense.description}
                    </td>
                    <td className="py-3 text-sm text-red-500 font-medium">
                      ₱{expense.amount.toLocaleString('en-PH', { minimumFractionDigits: 2 })}
                    </td>
                    <td className={`py-3 text-sm ${subText}`}>
                      {new Date(expense.date).toLocaleDateString('en-PH')}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default FinancialsView;