import { Activity, Droplets, Gauge, PlusCircle } from 'lucide-react';
import type { Product, DailySummary, MeterReading } from '../types/waterRefilling';

interface Props {
  products: Product[];
  dailySummary: DailySummary;
  meterReadings: MeterReading[];
  onAddReading: () => void;
  theme: 'light' | 'dark';
}

export function StationMonitorView({ products, dailySummary, meterReadings, onAddReading, theme }: Props) {
  const cardClass = theme === 'dark' ? 'bg-gray-900 border-gray-800' : 'bg-white border-slate-200';

  const statCards = [
    { label: 'Total Sales', value: `₱${dailySummary.totalSales.toFixed(2)}`, icon: <Droplets size={20} />, color: 'text-sky-500' },
    { label: 'Orders Today', value: dailySummary.ordersCount.toString(), icon: <Activity size={20} />, color: 'text-emerald-500' },
    { label: 'Containers Out', value: dailySummary.containersOut.toString(), icon: <Gauge size={20} />, color: 'text-amber-500' },
    { label: 'Net Income', value: `₱${dailySummary.netIncome.toFixed(2)}`, icon: <Droplets size={20} />, color: dailySummary.netIncome >= 0 ? 'text-emerald-500' : 'text-red-500' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <Activity className="text-sky-500" size={24} />
        <h2 className="text-xl font-semibold">Station Monitor & Inventory</h2>
      </div>

      {/* Stats Row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map(stat => (
          <div key={stat.label} className={`p-4 rounded-xl border ${cardClass}`}>
            <div className={`${stat.color} mb-2`}>{stat.icon}</div>
            <p className="text-sm text-slate-500 dark:text-gray-400">{stat.label}</p>
            <p className="text-lg font-bold mt-1">{stat.value}</p>
          </div>
        ))}
      </div>

      {/* Product Inventory */}
      <div className={`p-5 rounded-xl border ${cardClass}`}>
        <h3 className="font-semibold mb-4">Product Stock Levels</h3>
        <div className="space-y-3">
          {products.map(p => (
            <div key={p.id} className="space-y-1.5">
              <div className="flex justify-between text-sm">
                <span className="font-medium">{p.name}</span>
                <span className="text-slate-500">{p.stockAvailable} units</span>
              </div>
              <div className={`w-full h-2 rounded-full ${theme === 'dark' ? 'bg-gray-800' : 'bg-slate-100'}`}>
                <div
                  className={`h-2 rounded-full transition-all ${
                    p.stockAvailable >= 100 ? 'bg-emerald-500' :
                    p.stockAvailable >= 50 ? 'bg-sky-500' : 'bg-amber-500'
                  }`}
                  style={{ width: `${Math.min(100, (p.stockAvailable / 120) * 100)}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Water Meter Readings */}
      <div className={`p-5 rounded-xl border ${cardClass}`}>
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-semibold">Water Meter Readings</h3>
          <button
            onClick={onAddReading}
            className="flex items-center gap-1.5 text-sm bg-sky-600 hover:bg-sky-500 text-white px-3 py-1.5 rounded-lg transition-colors"
          >
            <PlusCircle size={14} /> New Reading
          </button>
        </div>

        {meterReadings.length === 0 ? (
          <p className="text-slate-500 italic">No meter readings recorded.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className={theme === 'dark' ? 'bg-gray-800 text-gray-300' : 'bg-slate-50 text-slate-600'}>
                  <th className="px-3 py-2 text-left">Date</th>
                  <th className="px-3 py-2 text-right">Previous</th>
                  <th className="px-3 py-2 text-right">Current</th>
                  <th className="px-3 py-2 text-right">m³ Used</th>
                  <th className="px-3 py-2 text-right">Cost/m³</th>
                  <th className="px-3 py-2 text-right">Total Cost</th>
                </tr>
              </thead>
              <tbody>
                {meterReadings.map(m => (
                  <tr key={m.id} className={`border-t ${theme === 'dark' ? 'border-gray-800' : 'border-slate-200'}`}>
                    <td className="px-3 py-2">{m.date}</td>
                    <td className="px-3 py-2 text-right">{m.previousReading}</td>
                    <td className="px-3 py-2 text-right font-medium">{m.currentReading}</td>
                    <td className="px-3 py-2 text-right">{m.cubicMetersUsed} m³</td>
                    <td className="px-3 py-2 text-right">₱{m.costPerCubicMeter.toFixed(2)}</td>
                    <td className="px-3 py-2 text-right font-medium">₱{m.totalCost.toFixed(2)}</td>
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
