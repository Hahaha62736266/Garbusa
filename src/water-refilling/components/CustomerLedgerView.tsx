import { Users, BookOpen, PlusCircle } from 'lucide-react';
import type { Customer, Collection } from '../types/waterRefilling';

interface Props {
  customers: Customer[];
  collections: Collection[];
  onRecordReturn: () => void;
  theme: 'light' | 'dark';
}

export function CustomerLedgerView({ customers, collections, onRecordReturn, theme }: Props) {
  const cardClass = theme === 'dark' ? 'bg-gray-900 border-gray-800' : 'bg-white border-slate-200';
  const tableHeader = theme === 'dark' ? 'bg-gray-800 text-gray-300' : 'bg-slate-50 text-slate-600';
  const tableCell = theme === 'dark' ? 'border-gray-800' : 'border-slate-200';

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Users className="text-sky-500" size={24} />
          <h2 className="text-xl font-semibold">Customer Ledger & Container Balances</h2>
        </div>
        <button
          onClick={onRecordReturn}
          className="flex items-center gap-2 bg-sky-600 hover:bg-sky-500 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
        >
          <PlusCircle size={16} /> Record Return
        </button>
      </div>

      <div className={`rounded-xl border overflow-hidden ${cardClass}`}>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className={tableHeader}>
                <th className="px-4 py-3 text-left font-medium">ID</th>
                <th className="px-4 py-3 text-left font-medium">Full Name</th>
                <th className="px-4 py-3 text-left font-medium">Contact</th>
                <th className="px-4 py-3 text-left font-medium">Address</th>
                <th className="px-4 py-3 text-center font-medium">Owned Jugs</th>
                <th className="px-4 py-3 text-center font-medium">Current Balance</th>
                <th className="px-4 py-3 text-left font-medium">Registered</th>
              </tr>
            </thead>
            <tbody>
              {customers.map(c => (
                <tr key={c.id} className={`border-t ${tableCell}`}>
                  <td className="px-4 py-3 font-mono font-medium">{c.id}</td>
                  <td className="px-4 py-3 font-medium">{c.fullName}</td>
                  <td className="px-4 py-3">{c.contactNumber}</td>
                  <td className="px-4 py-3 text-xs">{c.address}</td>
                  <td className="px-4 py-3 text-center">{c.containerOwned}</td>
                  <td className="px-4 py-3 text-center">
                    <span className={`inline-block w-8 h-8 rounded-full text-sm font-bold leading-8 ${
                      c.containerBalance > 0
                        ? 'bg-amber-500/20 text-amber-600 dark:text-amber-400'
                        : 'bg-emerald-500/20 text-emerald-600 dark:text-emerald-400'
                    }`}>
                      {c.containerBalance}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-xs">{c.registrationDate}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className={`rounded-xl border p-5 ${cardClass}`}>
        <h3 className="flex items-center gap-2 font-semibold mb-4">
          <BookOpen size={18} /> Recent Collection Logs
        </h3>
        {collections.length === 0 ? (
          <p className="text-slate-500 italic">No collection records yet.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className={tableHeader}>
                  <th className="px-3 py-2 text-left">ID</th>
                  <th className="px-3 py-2 text-left">Customer</th>
                  <th className="px-3 py-2 text-center">Returned</th>
                  <th className="px-3 py-2 text-center">Released</th>
                  <th className="px-3 py-2 text-center">Balance</th>
                  <th className="px-3 py-2 text-left">Date</th>
                  <th className="px-3 py-2 text-left">By</th>
                </tr>
              </thead>
              <tbody>
                {collections.map(cl => {
                  const cust = customers.find(c => c.id === cl.customerId);
                  return (
                    <tr key={cl.id} className={`border-t ${tableCell}`}>
                      <td className="px-3 py-2 font-mono">{cl.id}</td>
                      <td className="px-3 py-2">{cust?.fullName || cl.customerId}</td>
                      <td className="px-3 py-2 text-center">{cl.emptyJugsReturned}</td>
                      <td className="px-3 py-2 text-center">{cl.filledJugsReleased}</td>
                      <td className="px-3 py-2 text-center font-medium">{cl.containerBalance}</td>
                      <td className="px-3 py-2">{cl.collectionDate}</td>
                      <td className="px-3 py-2">{cl.collectedBy}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
