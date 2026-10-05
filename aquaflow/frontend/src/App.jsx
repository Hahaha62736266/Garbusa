import { useState } from 'react';
import CustomerForm from './components/CustomerForm';
import CustomerList from './components/CustomerList';
import OrderForm from './components/OrderForm';
import OrderList from './components/OrderList';

export default function App() {
  const [activeTab, setActiveTab] = useState('customers');
  const [refreshKey, setRefreshKey] = useState(0);

  const handleSaved = () => {
    setRefreshKey(prev => prev + 1); // auto-refresh lists after create/edit
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold text-gray-800">💧 Aquaflow Tracker</h1>
          <p className="text-sm text-gray-500">Garbusa — Farm & Order Management</p>
        </div>
      </header>

      {/* Navigation Tabs */}
      <div className="max-w-7xl mx-auto px-4 mt-4">
        <div className="flex border-b bg-white rounded-t-lg overflow-hidden">
          {[
            { id: 'customers', label: '👤 Customers' },
            { id: 'orders', label: '📦 Orders' }
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-6 py-3 font-medium transition-colors ${
                activeTab === tab.id
                  ? 'border-b-2 border-blue-600 text-blue-600 bg-blue-50'
                  : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-6">
        {activeTab === 'customers' && (
          <div className="space-y-6">
            <CustomerForm key={`form-${refreshKey}`} onSaved={handleSaved} />
            <CustomerList key={`list-${refreshKey}`} />
          </div>
        )}

        {activeTab === 'orders' && (
          <div className="space-y-6">
            <OrderForm key={`form-${refreshKey}`} onSaved={handleSaved} />
            <OrderList key={`list-${refreshKey}`} />
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="mt-12 py-4 text-center text-xs text-gray-400">
        Aquaflow Tracker • Garbusa Project
      </footer>
    </div>
  );
}
