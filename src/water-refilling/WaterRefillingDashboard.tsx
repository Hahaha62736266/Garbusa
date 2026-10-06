// src/water-refilling/WaterRefillingDashboard.tsx
'use client';

import { useState, useEffect } from 'react';
import { 
  Droplets, ShoppingCart, Truck, Users, BarChart3, Activity,
  Sun, Moon, Plus, Filter, RefreshCw
} from 'lucide-react';
import type { TabView, Customer, Product, Order, Collection, Expense, MeterReading, DailySummary } from './types/waterRefilling';
import { initialCustomers, initialProducts, initialOrders, initialCollections, initialExpenses, initialMeterReadings, initialDailySummary } from './data/mockWaterData';

// Sub-components
import { PosCounterView } from './components/PosCounterView';
import { OrdersDeliveryView } from './components/OrdersDeliveryView';
import { CustomerLedgerView } from './components/CustomerLedgerView';
import { StationMonitorView } from './components/StationMonitorView';
import { FinancialsView } from './components/FinancialsView';

// Modals
import { NewOrderModal } from './modals/NewOrderModal';
import { ReceiptModal } from './modals/ReceiptModal';
import { ContainerReturnModal } from './modals/ContainerReturnModal';
import { ExpenseModal } from './modals/ExpenseModal';
import { MeterReadingModal } from './modals/MeterReadingModal';

export default function WaterRefillingDashboard() {
  // Theme detection (integrates with repo's existing strategy)
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  useEffect(() => {
    const root = document.documentElement;
    const systemPrefers = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    const stored = localStorage.getItem('theme') as 'light' | 'dark' | null;
    const active = stored || systemPrefers;
    setTheme(active);
    root.classList.toggle('dark', active === 'dark');
  }, []);

  const toggleTheme = () => {
    const next = theme === 'light' ? 'dark' : 'light';
    setTheme(next);
    document.documentElement.classList.toggle('dark', next === 'dark');
    localStorage.setItem('theme', next);
  };

  // Active tab state
  const [activeTab, setActiveTab] = useState<TabView>('pos');

  // Core data state
  const [customers, setCustomers] = useState<Customer[]>(initialCustomers);
  const [products] = useState<Product[]>(initialProducts);
  const [orders, setOrders] = useState<Order[]>(initialOrders);
  const [collections, setCollections] = useState<Collection[]>(initialCollections);
  const [expenses, setExpenses] = useState<Expense[]>(initialExpenses);
  const [meterReadings, setMeterReadings] = useState<MeterReading[]>(initialMeterReadings);
  const [dailySummary, setDailySummary] = useState<DailySummary>(initialDailySummary);

  // Modal visibility
  const [newOrderModalOpen, setNewOrderModalOpen] = useState(false);
  const [receiptModalOpen, setReceiptModalOpen] = useState(false);
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);
  const [returnModalOpen, setReturnModalOpen] = useState(false);
  const [expenseModalOpen, setExpenseModalOpen] = useState(false);
  const [meterModalOpen, setMeterModalOpen] = useState(false);

  // Tab configuration with Lucide icons replacing emojis
  const tabs = [
    { key: 'pos' as TabView, label: 'POS Counter', icon: <ShoppingCart size={18} strokeWidth={1.5} /> },
    { key: 'orders' as TabView, label: 'Orders & Delivery', icon: <Truck size={18} strokeWidth={1.5} /> },
    { key: 'customers' as TabView, label: 'Customer Ledger', icon: <Users size={18} strokeWidth={1.5} /> },
    { key: 'monitor' as TabView, label: 'Station Monitor', icon: <Activity size={18} strokeWidth={1.5} /> },
    { key: 'financials' as TabView, label: 'Financials', icon: <BarChart3 size={18} strokeWidth={1.5} /> },
  ];

  // === Action Handlers ===
  const handleNewOrder = (order: Omit<Order, 'id'>) => {
    const newId = `O${String(orders.length + 1).padStart(3, '0')}`;
    setOrders(prev => [...prev, { ...order, id: newId }]);
    // Update summary
    setDailySummary(prev => ({
      ...prev,
      totalSales: prev.totalSales + order.totalAmount,
      ordersCount: prev.ordersCount + 1,
    }));
  };

  const handleMarkDelivered = (orderId: string) => {
    setOrders(prev => prev.map(o => 
      o.id === orderId ? { ...o, status: 'Delivered' } : o
    ));
  };

  const handleRecordReturn = (recorded: Omit<Collection, 'id'>) => {
    const newId = `CL${String(collections.length + 1).padStart(3, '0')}`;
    setCollections(prev => [...prev, { ...recorded, id: newId }]);
    // Update customer balance
    setCustomers(prev => prev.map(c => 
      c.id === recorded.customerId 
        ? { ...c, containerBalance: recorded.containerBalance }
        : c
    ));
  };

  const handleAddExpense = (exp: Omit<Expense, 'id'>) => {
    const newId = `E${String(expenses.length + 1).padStart(3, '0')}`;
    setExpenses(prev => [...prev, { ...exp, id: newId }]);
    setDailySummary(prev => ({
      ...prev,
      totalExpenses: prev.totalExpenses + exp.amount,
      netIncome: prev.netIncome - exp.amount,
    }));
  };

  const handleAddMeterReading = (reading: Omit<MeterReading, 'id'>) => {
    const newId = `M${String(meterReadings.length + 1).padStart(3, '0')}`;
    setMeterReadings(prev => [...prev, { ...reading, id: newId }]);
  };

  const handlePrintReceipt = (order: Order) => {
    setSelectedOrder(order);
    setReceiptModalOpen(true);
  };

  return (
    <div className={`min-h-screen transition-colors duration-200 ${
      theme === 'dark' ? 'bg-gray-950 text-gray-100' : 'bg-slate-50 text-slate-900'
    }`}>
      {/* Header */}
      <header className={`sticky top-0 z-40 border-b ${
        theme === 'dark' ? 'bg-gray-900/90 border-gray-800' : 'bg-white/90 border-slate-200'
      } backdrop-blur-sm`}>
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Droplets className="text-sky-500" size={28} />
            <div>
              <h1 className="text-xl font-bold tracking-tight">AquaFlow Tracker</h1>
              <p className={`text-sm ${theme === 'dark' ? 'text-gray-400' : 'text-slate-500'}`}>
                Water Refilling Station Management
              </p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={toggleTheme}
              className={`p-2 rounded-lg transition-colors ${
                theme === 'dark' ? 'hover:bg-gray-800' : 'hover:bg-slate-100'
              }`}
              aria-label="Toggle theme"
            >
              {theme === 'dark' ? <Sun size={18} /> : <Moon size={18} />}
            </button>
            <button
              onClick={() => setNewOrderModalOpen(true)}
              className="flex items-center gap-2 bg-sky-600 hover:bg-sky-500 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
            >
              <Plus size={16} /> New Order
            </button>
          </div>
        </div>
      </header>

      {/* Tab Navigation */}
      <div className="max-w-7xl mx-auto px-4 pt-4">
        <div className={`flex flex-wrap gap-1 border-b ${
          theme === 'dark' ? 'border-gray-800' : 'border-slate-200'
        }`}>
          {tabs.map(tab => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
                activeTab === tab.key
                  ? 'border-sky-500 text-sky-600 dark:text-sky-400'
                  : 'border-transparent text-slate-500 hover:text-slate-700 dark:text-gray-400 dark:hover:text-gray-200'
              }`}
            >
              {tab.icon}
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Main Content Area */}
      <main className="max-w-7xl mx-auto px-4 py-6">
        {activeTab === 'pos' && (
          <PosCounterView
            customers={customers}
            products={products}
            onNewOrder={handleNewOrder}
            theme={theme}
          />
        )}
        {activeTab === 'orders' && (
          <OrdersDeliveryView
            orders={orders}
            customers={customers}
            products={products}
            onMarkDelivered={handleMarkDelivered}
            onPrintReceipt={handlePrintReceipt}
            theme={theme}
          />
        )}
        {activeTab === 'customers' && (
          <CustomerLedgerView
            customers={customers}
            collections={collections}
            onRecordReturn={() => setReturnModalOpen(true)}
            theme={theme}
          />
        )}
        {activeTab === 'monitor' && (
          <StationMonitorView
            products={products}
            dailySummary={dailySummary}
            meterReadings={meterReadings}
            onAddReading={() => setMeterModalOpen(true)}
            theme={theme}
          />
        )}
        {activeTab === 'financials' && (
          <FinancialsView
            dailySummary={dailySummary}
            expenses={expenses}
            meterReadings={meterReadings}
            onAddExpense={() => setExpenseModalOpen(true)}
            theme={theme}
          />
        )}
      </main>

      {/* Modals */}
      <NewOrderModal
        open={newOrderModalOpen}
        onClose={() => setNewOrderModalOpen(false)}
        customers={customers}
        products={products}
        onSubmit={handleNewOrder}
        theme={theme}
      />
      <ReceiptModal
        open={receiptModalOpen}
        onClose={() => setReceiptModalOpen(false)}
        order={selectedOrder}
        customers={customers}
        products={products}
      />
      <ContainerReturnModal
        open={returnModalOpen}
        onClose={() => setReturnModalOpen(false)}
        customers={customers}
        orders={orders}
        onSubmit={handleRecordReturn}
        theme={theme}
      />
      <ExpenseModal
        open={expenseModalOpen}
        onClose={() => setExpenseModalOpen(false)}
        onSubmit={handleAddExpense}
        theme={theme}
      />
      <MeterReadingModal
        open={meterModalOpen}
        onClose={() => setMeterModalOpen(false)}
        onSubmit={handleAddMeterReading}
        theme={theme}
      />
    </div>
  );
}
