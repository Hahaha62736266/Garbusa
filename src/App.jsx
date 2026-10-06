import React, { useState } from 'react';

// Custom inline SVG icons to eliminate third-party package dependencies during Render builds
const DropletIcon = ({ className = "w-5 h-5", ...props }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" {...props}>
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 2.69l5.66 5.66a8 8 0 11-11.31 0z"></path>
  </svg>
);

const FlaskIcon = ({ className = "w-5 h-5", ...props }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" {...props}>
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19.5 21a1.5 1.5 0 001.5-1.5v-1a2 2 0 00-.5-1.33L15 11V5h1a1 1 0 000-2H8a1 1 0 000 2h1v6l-5.5 7.17A2 2 0 003 18.5v1A1.5 1.5 0 004.5 21h15z"></path>
  </svg>
);

const PackageIcon = ({ className = "w-5 h-5", ...props }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" {...props}>
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
  </svg>
);

const PlusIcon = ({ className = "w-5 h-5", ...props }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" {...props}>
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4"></path>
  </svg>
);

const ShoppingBagIcon = ({ className = "w-5 h-5", ...props }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" {...props}>
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path>
  </svg>
);

const TruckIcon = ({ className = "w-5 h-5", ...props }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" {...props}>
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0zM13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 01-1 1H9m4-1h2.586a1 1 0 01.707.293l3.414 3.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a1 1 0 001 1h1m-4 0a1 1 0 001-1"></path>
  </svg>
);

const UsersIcon = ({ className = "w-5 h-5", ...props }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" {...props}>
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path>
  </svg>
);

const ActivityIcon = ({ className = "w-5 h-5", ...props }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" {...props}>
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
  </svg>
);

const DollarSignIcon = ({ className = "w-5 h-5", ...props }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" {...props}>
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V6m0 8v2m0-8c-1.11 0-2.08-.402-2.599-1M12 16c1.657 0 3-.895 3-2s-1.343-2-3-2-3-.895-3-2 1.343-2 3-2m0 8c-1.11 0-2.08-.402-2.599-1"></path>
  </svg>
);

const XIcon = ({ className = "w-5 h-5", ...props }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" {...props}>
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
  </svg>
);

export default function App() {
  // Navigation Tabs state
  const [activeTab, setActiveTab] = useState('pos'); // 'pos', 'deliveries', 'ledger', 'monitor', 'financials'

  // Modals state
  const [isNewOrderModalOpen, setIsNewOrderModalOpen] = useState(false);
  const [isAddExpenseModalOpen, setIsAddExpenseModalOpen] = useState(false);
  const [isAddCustomerModalOpen, setIsAddCustomerModalOpen] = useState(false);
  const [selectedReceiptOrder, setSelectedReceiptOrder] = useState(null);

  // Telemetry state
  const [tankLevel, setTankLevel] = useState(3800);
  const tankCapacity = 5000;
  const [tdsLevel, setTdsLevel] = useState(12);
  const [phLevel, setPhLevel] = useState(7.4);

  // Orders State
  const [orders, setOrders] = useState([
    {
      id: 'ORD-1092',
      customer: 'Maria Santos',
      type: 'Delivery',
      time: '10:15 AM',
      items: '3x 5-Gal Slim Container Refill, 1x 5-Gal Round Container Refill',
      amount: 140,
      paymentStatus: 'Paid (GCash)',
      paymentType: 'Paid',
      status: 'Out for Delivery',
      date: 'Today'
    },
    {
      id: 'ORD-1093',
      customer: 'Garbusa Eatery',
      type: 'Delivery',
      time: '10:42 AM',
      items: '5x 5-Gal Slim Container Refill, 4x Alkaline Water Bottle 1L',
      amount: 275,
      paymentStatus: 'Unpaid (Pay Later)',
      paymentType: 'Unpaid',
      status: 'Refill in Progress',
      date: 'Today'
    },
    {
      id: 'ORD-1094',
      customer: 'Walk-in Customer',
      type: 'Walk-in',
      time: '11:05 AM',
      items: '2x 5-Gal Round Container Refill',
      amount: 70,
      paymentStatus: 'Paid (Cash)',
      paymentType: 'Paid',
      status: 'Completed',
      date: 'Today'
    }
  ]);

  // Container Refill Price Rates
  const refillRates = [
    { name: '5-Gallon Slim Refill', desc: 'Purified drinking water with handle', price: 35, icon: '🍶' },
    { name: '5-Gallon Round Refill', desc: 'Standard dispenser bottleneck', price: 35, icon: '🪣' },
    { name: 'Container Dispenser Set', desc: 'New container + Initial Refill', price: 250, icon: '🚰' },
    { name: 'Alkaline Water Bottle 1L', desc: 'High pH mineralized drinking bottle', price: 25, icon: '🍾' },
    { name: 'Container Cap / Seal Replace', desc: 'Sanitary replacement cap', price: 5, icon: '🔘' },
  ];

  // Customers Ledger Initial Data
  const [customers, setCustomers] = useState([
    { id: 'CUST-001', name: 'Maria Santos', contact: '0917-123-4567', address: 'Poblacion Zone 2, Maramag', slimBorrowed: 3, roundBorrowed: 1, totalOrders: 14 },
    { id: 'CUST-002', name: 'Garbusa Eatery', contact: '0988-555-0192', address: 'Public Market, Maramag', slimBorrowed: 15, roundBorrowed: 5, totalOrders: 42 },
    { id: 'CUST-003', name: 'Walk-in Customer', contact: 'N/A', address: 'Counter Refill', slimBorrowed: 0, roundBorrowed: 0, totalOrders: 110 }
  ]);

  // Expenses State
  const [expenses, setExpenses] = useState([
    { id: 'EXP-101', description: 'Purification Filter Replacement', amount: 1200, category: 'Maintenance', date: '2026-10-02' },
    { id: 'EXP-102', description: 'Delivery Motorcycle Gas', amount: 350, category: 'Fuel', date: '2026-10-04' },
    { id: 'EXP-103', description: 'Sanitizing Seal Caps Bulk', amount: 450, category: 'Supplies', date: '2026-10-05' }
  ]);

  // Computed Metrics
  const todayRevenue = orders
    .filter(o => o.paymentType === 'Paid')
    .reduce((sum, o) => sum + o.amount, 0);

  const activeRefillsCount = orders.filter(o => o.status !== 'Completed').length;
  const walkInCount = orders.filter(o => o.type === 'Walk-in').length;
  const deliveryCount = orders.filter(o => o.type === 'Delivery').length;

  const handleCreateOrder = (e) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const newOrd = {
      id: `ORD-${1095 + orders.length}`,
      customer: formData.get('customer') || 'Walk-in Customer',
      type: formData.get('type') || 'Walk-in',
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      items: formData.get('items') || '1x 5-Gal Refill',
      amount: Number(formData.get('amount')) || 35,
      paymentStatus: formData.get('paymentStatus') || 'Paid (Cash)',
      paymentType: formData.get('paymentStatus')?.includes('Unpaid') ? 'Unpaid' : 'Paid',
      status: formData.get('type') === 'Delivery' ? 'Out for Delivery' : 'Refill in Progress',
      date: 'Today'
    };

    setOrders([newOrd, ...orders]);
    setIsNewOrderModalOpen(false);
  };

  const handleAddCustomer = (e) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const newCust = {
      id: `CUST-00${customers.length + 1}`,
      name: formData.get('fullName') || 'New Customer',
      contact: formData.get('contact') || 'N/A',
      address: formData.get('address') || 'Maramag',
      slimBorrowed: 0,
      roundBorrowed: 0,
      totalOrders: 0
    };
    setCustomers([...customers, newCust]);
    setIsAddCustomerModalOpen(false);
  };

  const handleAddExpense = (e) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const newExp = {
      id: `EXP-${104 + expenses.length}`,
      description: formData.get('description') || 'Station Expense',
      amount: Number(formData.get('amount')) || 0,
      category: formData.get('category') || 'General',
      date: new Date().toISOString().split('T')[0]
    };
    setExpenses([newExp, ...expenses]);
    setIsAddExpenseModalOpen(false);
  };

  const getStatusBadgeClass = (status) => {
    switch (status) {
      case 'Out for Delivery':
        return 'bg-[#0f2942] text-[#38bdf8] border border-[#1e40af]/50';
      case 'Refill in Progress':
        return 'bg-[#3b2d0d] text-[#facc15] border border-[#a16207]/50';
      case 'Completed':
        return 'bg-[#064e3b]/50 text-[#34d399] border border-[#059669]/50';
      default:
        return 'bg-slate-800 text-slate-300';
    }
  };

  return (
    <div style={{ backgroundColor: '#060c19', color: '#f1f5f9', minHeight: '100vh', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      {/* Header Bar */}
      <header className="bg-[#091326] border-b border-slate-800/80 px-4 lg:px-8 py-3.5 flex flex-col lg:flex-row lg:items-center justify-between gap-4 sticky top-0 z-30 shadow-xl">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-cyan-600/20 border border-cyan-500/40 flex items-center justify-center text-cyan-400 shadow-inner">
            <DropletIcon className="w-6 h-6 text-cyan-400" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="font-bold text-base md:text-lg tracking-wider text-white">
                GARBUSA WATER REFILLING STATION
              </h1>
              <span className="text-[10px] font-bold bg-[#092c48] text-cyan-400 border border-cyan-500/30 px-2 py-0.5 rounded-md tracking-wider">
                WRSMS v3.2
              </span>
            </div>
            <p className="text-xs text-slate-400 flex items-center gap-1.5 mt-0.5">
              <span>Poblacion, Maramag</span>
              <span className="text-slate-600">•</span>
              <span>Station Operator: <strong className="text-emerald-400 font-medium">On-Duty</strong></span>
            </p>
          </div>
        </div>

        {/* Header Stats */}
        <div className="flex flex-wrap items-center gap-6 text-xs border-t lg:border-t-0 pt-2 lg:pt-0 border-slate-800">
          <div className="flex flex-col">
            <span className="text-slate-400 text-[11px]">Today's Revenue</span>
            <span className="text-cyan-400 font-extrabold text-base">₱{todayRevenue.toLocaleString()}</span>
          </div>

          <div className="h-7 w-[1px] bg-slate-800 hidden sm:block"></div>

          <div className="flex flex-col">
            <span className="text-slate-400 text-[11px]">Purified Tank</span>
            <span className="text-slate-100 font-bold text-xs">
              <strong className="text-cyan-400 text-sm">{tankLevel.toLocaleString()}</strong> / {tankCapacity.toLocaleString()} L
            </span>
          </div>

          <div className="h-7 w-[1px] bg-slate-800 hidden sm:block"></div>

          <div className="flex flex-col">
            <span className="text-slate-400 text-[11px]">Borrowed Containers</span>
            <span className="text-amber-400 font-bold text-xs">
              26 Slim • 8 Rd
            </span>
          </div>

          <button
            onClick={() => setIsNewOrderModalOpen(true)}
            className="ml-auto lg:ml-2 bg-[#0284c7] hover:bg-[#0369a1] text-white font-medium text-xs px-4 py-2.5 rounded-lg shadow-lg shadow-cyan-600/20 transition flex items-center gap-1.5 cursor-pointer"
          >
            <PlusIcon className="w-4 h-4" />
            New Order / Refill
          </button>
        </div>
      </header>

      {/* Navigation Tab Menu */}
      <nav className="bg-[#091326]/90 backdrop-blur border-b border-slate-800 px-4 lg:px-8 overflow-x-auto">
        <div className="flex gap-2 min-w-max py-2">
          <button
            onClick={() => setActiveTab('pos')}
            className={`px-4 py-2 rounded-lg text-xs font-bold flex items-center gap-2 transition cursor-pointer ${
              activeTab === 'pos'
                ? 'bg-[#0284c7] text-white shadow-md border border-cyan-400/40'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
            }`}
          >
            <ShoppingBagIcon className="w-4 h-4" />
            POS & Counter
          </button>

          <button
            onClick={() => setActiveTab('deliveries')}
            className={`px-4 py-2 rounded-lg text-xs font-bold flex items-center gap-2 transition cursor-pointer ${
              activeTab === 'deliveries'
                ? 'bg-[#0284c7] text-white shadow-md border border-cyan-400/40'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
            }`}
          >
            <TruckIcon className="w-4 h-4" />
            Active Deliveries & Orders
            <span className="ml-1 bg-amber-500 text-slate-950 font-black text-[10px] px-1.5 py-0.2 rounded-full">
              {activeRefillsCount}
            </span>
          </button>

          <button
            onClick={() => setActiveTab('ledger')}
            className={`px-4 py-2 rounded-lg text-xs font-bold flex items-center gap-2 transition cursor-pointer ${
              activeTab === 'ledger'
                ? 'bg-[#0284c7] text-white shadow-md border border-cyan-400/40'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
            }`}
          >
            <UsersIcon className="w-4 h-4" />
            Customer Container Ledger
          </button>

          <button
            onClick={() => setActiveTab('monitor')}
            className={`px-4 py-2 rounded-lg text-xs font-bold flex items-center gap-2 transition cursor-pointer ${
              activeTab === 'monitor'
                ? 'bg-[#0284c7] text-white shadow-md border border-cyan-400/40'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
            }`}
          >
            <ActivityIcon className="w-4 h-4" />
            Purification & Tank Monitor
          </button>

          <button
            onClick={() => setActiveTab('financials')}
            className={`px-4 py-2 rounded-lg text-xs font-bold flex items-center gap-2 transition cursor-pointer ${
              activeTab === 'financials'
                ? 'bg-[#0284c7] text-white shadow-md border border-cyan-400/40'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
            }`}
          >
            <DollarSignIcon className="w-4 h-4" />
            Sales & Expenses
          </button>
        </div>
      </nav>

      {/* Main Dashboard Layout */}
      <main className="p-4 lg:p-8 max-w-[1500px] mx-auto space-y-6">
        {/* Metric Cards Row */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Card 1: Tank Level */}
          <div className="bg-[#0b1730] border border-slate-800/80 rounded-2xl p-4 flex justify-between items-center relative overflow-hidden shadow-sm">
            <div>
              <p className="text-[11px] font-bold tracking-wider text-slate-400 uppercase">
                STATION TANK LEVEL
              </p>
              <div className="mt-1 flex items-baseline gap-2">
                <span className="text-2xl font-black text-cyan-400 tracking-tight">{tankLevel}</span>
                <span className="text-xs text-slate-300 font-semibold">Liters</span>
              </div>
              <p className="text-[11px] text-cyan-400/80 mt-1 font-medium">
                Capacity: {tankCapacity.toLocaleString()} L ({Math.round((tankLevel/tankCapacity)*100)}% Full)
              </p>
            </div>
            <div className="w-11 h-11 rounded-full bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400">
              <DropletIcon className="w-6 h-6" />
            </div>
          </div>

          {/* Card 2: Water Quality */}
          <div className="bg-[#0b1730] border border-slate-800/80 rounded-2xl p-4 flex justify-between items-center relative overflow-hidden shadow-sm">
            <div>
              <p className="text-[11px] font-bold tracking-wider text-slate-400 uppercase">
                WATER QUALITY INDEX
              </p>
              <div className="mt-1 flex items-baseline gap-2">
                <span className="text-2xl font-black text-emerald-400 tracking-tight">{tdsLevel}</span>
                <span className="text-xs text-slate-300 font-semibold">PPM (TDS)</span>
              </div>
              <p className="text-[11px] text-emerald-400/80 mt-1 font-medium">
                pH Level: {phLevel} (Optimal)
              </p>
            </div>
            <div className="w-11 h-11 rounded-full bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
              <FlaskIcon className="w-6 h-6" />
            </div>
          </div>

          {/* Card 3: Active Refills */}
          <div className="bg-[#0b1730] border border-slate-800/80 rounded-2xl p-4 flex justify-between items-center relative overflow-hidden shadow-sm">
            <div>
              <p className="text-[11px] font-bold tracking-wider text-slate-400 uppercase">
                ACTIVE REFILLS TODAY
              </p>
              <div className="mt-1 flex items-baseline gap-2">
                <span className="text-2xl font-black text-blue-400 tracking-tight">{orders.length}</span>
                <span className="text-xs text-slate-300 font-semibold">Orders</span>
              </div>
              <p className="text-[11px] text-slate-400 mt-1 font-medium">
                Walk-in: {walkInCount} • Delivery: {deliveryCount}
              </p>
            </div>
            <div className="w-11 h-11 rounded-full bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-400">
              <PackageIcon className="w-6 h-6" />
            </div>
          </div>

          {/* Card 4: Quick Action */}
          <button
            onClick={() => setIsNewOrderModalOpen(true)}
            className="border-2 border-dashed border-cyan-500/30 bg-[#0b1730]/40 hover:bg-[#0b1730] hover:border-cyan-400 rounded-2xl p-4 flex flex-col items-center justify-center text-center transition group cursor-pointer"
          >
            <div className="w-10 h-10 rounded-full bg-cyan-500/20 text-cyan-400 flex items-center justify-center group-hover:scale-110 transition">
              <PlusIcon className="w-6 h-6" />
            </div>
            <span className="mt-2 text-xs font-bold text-cyan-300 group-hover:text-cyan-200">
              Create New Counter Order
            </span>
          </button>
        </div>

        {/* Tab 1: POS & Counter View */}
        {activeTab === 'pos' && (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* Rates Table */}
            <div className="lg:col-span-4 bg-[#0b1730] border border-slate-800 rounded-2xl p-5 flex flex-col justify-between shadow-md">
              <div>
                <div className="flex items-center justify-between pb-4 mb-4 border-b border-slate-800">
                  <h2 className="font-bold text-slate-100 text-sm tracking-wide">
                    Container Refill Rates
                  </h2>
                  <span className="text-[10px] bg-slate-800 text-slate-300 px-2.5 py-0.5 rounded-full border border-slate-700 font-semibold">
                    Garbusa Standard
                  </span>
                </div>

                <div className="space-y-3">
                  {refillRates.map((rate, idx) => (
                    <div
                      key={idx}
                      className="p-3 bg-[#060e21] border border-slate-800/80 rounded-xl flex items-center justify-between hover:border-slate-700 transition"
                    >
                      <div className="flex items-center gap-3">
                        <div className="w-9 h-9 rounded-lg bg-slate-800/80 flex items-center justify-center text-lg">
                          {rate.icon}
                        </div>
                        <div>
                          <p className="text-xs font-bold text-slate-200">{rate.name}</p>
                          <p className="text-[10px] text-slate-400 mt-0.5">{rate.desc}</p>
                        </div>
                      </div>
                      <span className="text-sm font-black text-cyan-400 ml-2">
                        ₱{rate.price}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              <button
                onClick={() => setIsNewOrderModalOpen(true)}
                className="w-full mt-6 bg-[#00a8e8] hover:bg-[#0092cd] text-slate-950 font-extrabold text-xs py-3 rounded-xl transition shadow-lg shadow-cyan-500/20 cursor-pointer"
              >
                Open Full POS Counter Terminal
              </button>
            </div>

            {/* Live Stream Orders Table */}
            <div className="lg:col-span-8 bg-[#0b1730] border border-slate-800 rounded-2xl p-5 shadow-md flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between pb-4 mb-4 border-b border-slate-800">
                  <div>
                    <div className="flex items-center gap-2">
                      <h2 className="font-bold text-slate-100 text-sm tracking-wide">
                        Live Terminal Order Stream
                      </h2>
                      <span className="text-[10px] text-emerald-400 flex items-center gap-1 bg-emerald-950/60 border border-emerald-500/30 px-2 py-0.5 rounded-full font-bold">
                        <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span> Live Feed
                      </span>
                    </div>
                    <p className="text-xs text-slate-400 mt-0.5">
                      Real-time status tracking for current counter and delivery orders
                    </p>
                  </div>
                </div>

                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs">
                    <thead>
                      <tr className="text-slate-400 border-b border-slate-800/80 text-[11px] uppercase font-bold">
                        <th className="pb-3 pr-2">Order ID</th>
                        <th className="pb-3 px-2">Customer</th>
                        <th className="pb-3 px-2">Items</th>
                        <th className="pb-3 px-2">Amount</th>
                        <th className="pb-3 px-2">Status</th>
                        <th className="pb-3 pl-2 text-right">Action</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800/50">
                      {orders.map((order) => (
                        <tr key={order.id} className="hover:bg-slate-800/20 transition">
                          <td className="py-3.5 pr-2 font-mono font-bold text-cyan-400 text-xs">
                            {order.id}
                          </td>
                          <td className="py-3.5 px-2">
                            <div className="font-bold text-slate-200">{order.customer}</div>
                            <div className="text-[10px] text-slate-400">
                              {order.type} • {order.time}
                            </div>
                          </td>
                          <td className="py-3.5 px-2 text-slate-300 max-w-[200px] truncate" title={order.items}>
                            {order.items}
                          </td>
                          <td className="py-3.5 px-2">
                            <div className="font-extrabold text-slate-100">₱{order.amount}</div>
                            <div className={`text-[10px] font-bold ${order.paymentType === 'Paid' ? 'text-emerald-400' : 'text-amber-400'}`}>
                              {order.paymentStatus}
                            </div>
                          </td>
                          <td className="py-3.5 px-2">
                            <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold whitespace-nowrap ${getStatusBadgeClass(order.status)}`}>
                              {order.status}
                            </span>
                          </td>
                          <td className="py-3.5 pl-2 text-right">
                            <button
                              onClick={() => setSelectedReceiptOrder(order)}
                              className="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 rounded-md text-[11px] font-semibold transition cursor-pointer"
                            >
                              Receipt
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Tab 2: Deliveries Tab */}
        {activeTab === 'deliveries' && (
          <div className="bg-[#0b1730] border border-slate-800 rounded-2xl p-6 shadow-md">
            <div className="flex flex-col md:flex-row md:items-center justify-between pb-4 mb-6 border-b border-slate-800 gap-4">
              <div>
                <h2 className="font-bold text-lg text-slate-100">Deliveries & Dispatch Center</h2>
                <p className="text-xs text-slate-400">Track container dispatches across Poblacion & Maramag</p>
              </div>
              <button
                onClick={() => setIsNewOrderModalOpen(true)}
                className="bg-cyan-600 hover:bg-cyan-500 text-white text-xs px-4 py-2 rounded-lg font-semibold flex items-center gap-1.5 self-start cursor-pointer"
              >
                <PlusIcon className="w-4 h-4" /> Schedule New Delivery
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {orders.filter(o => o.type === 'Delivery').map((order) => (
                <div key={order.id} className="bg-[#060e21] border border-slate-800 p-4 rounded-xl space-y-3">
                  <div className="flex justify-between items-start">
                    <div>
                      <span className="text-xs font-mono font-bold text-cyan-400">{order.id}</span>
                      <h3 className="font-bold text-slate-200 text-sm mt-0.5">{order.customer}</h3>
                    </div>
                    <span className={`px-2 py-0.5 rounded-full text-[10px] font-semibold ${getStatusBadgeClass(order.status)}`}>
                      {order.status}
                    </span>
                  </div>
                  <p className="text-xs text-slate-300">{order.items}</p>
                  <div className="flex items-center justify-between text-xs text-slate-400 pt-2 border-t border-slate-800">
                    <span>Amount: <strong className="text-slate-100">₱{order.amount}</strong> ({order.paymentStatus})</span>
                    <button 
                      onClick={() => {
                        setOrders(orders.map(o => o.id === order.id ? {...o, status: 'Completed'} : o));
                      }}
                      className="px-3 py-1 bg-emerald-600/20 text-emerald-300 border border-emerald-500/30 rounded text-[11px] font-medium hover:bg-emerald-600/30 cursor-pointer"
                    >
                      Mark Completed
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Tab 3: Customer Ledger Tab */}
        {activeTab === 'ledger' && (
          <div className="bg-[#0b1730] border border-slate-800 rounded-2xl p-6 shadow-md space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between pb-4 border-b border-slate-800 gap-4">
              <div>
                <h2 className="font-bold text-lg text-slate-100">Customer Container Ledger</h2>
                <p className="text-xs text-slate-400">Track slim & round borrowed container balances</p>
              </div>
              <button
                onClick={() => setIsAddCustomerModalOpen(true)}
                className="bg-cyan-600 hover:bg-cyan-500 text-white text-xs px-4 py-2 rounded-lg font-semibold flex items-center gap-1.5 self-start cursor-pointer"
              >
                <PlusIcon className="w-4 h-4" /> Add New Customer
              </button>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="text-slate-400 border-b border-slate-800 uppercase font-bold">
                    <th className="pb-3">ID</th>
                    <th className="pb-3">Customer Name</th>
                    <th className="pb-3">Contact</th>
                    <th className="pb-3">Address</th>
                    <th className="pb-3">Slim Borrowed</th>
                    <th className="pb-3">Round Borrowed</th>
                    <th className="pb-3 text-right">Total Refills</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {customers.map((cust) => (
                    <tr key={cust.id} className="hover:bg-slate-800/20">
                      <td className="py-3 font-mono font-bold text-cyan-400">{cust.id}</td>
                      <td className="py-3 font-bold text-slate-200">{cust.name}</td>
                      <td className="py-3 text-slate-400">{cust.contact}</td>
                      <td className="py-3 text-slate-300">{cust.address}</td>
                      <td className="py-3 text-amber-400 font-bold">{cust.slimBorrowed} pcs</td>
                      <td className="py-3 text-blue-400 font-bold">{cust.roundBorrowed} pcs</td>
                      <td className="py-3 text-right font-bold text-slate-200">{cust.totalOrders}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Tab 4: Purification Monitor Tab */}
        {activeTab === 'monitor' && (
          <div className="bg-[#0b1730] border border-slate-800 rounded-2xl p-6 shadow-md space-y-6">
            <div className="pb-4 border-b border-slate-800">
              <h2 className="font-bold text-lg text-slate-100">Purification & Tank Telemetry</h2>
              <p className="text-xs text-slate-400">Real-time water quality monitoring and tank levels</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-[#060e21] p-5 rounded-2xl border border-slate-800 space-y-4">
                <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider">Main Tank Storage</h3>
                <div className="relative w-full bg-slate-800 rounded-xl h-12 overflow-hidden flex items-center border border-slate-700">
                  <div 
                    className="bg-gradient-to-r from-cyan-600 to-blue-500 h-full transition-all duration-500"
                    style={{ width: `${(tankLevel / tankCapacity) * 100}%` }}
                  ></div>
                  <span className="absolute inset-0 flex items-center justify-center text-xs font-black text-white drop-shadow">
                    {tankLevel} / {tankCapacity} Liters ({Math.round((tankLevel/tankCapacity)*100)}%)
                  </span>
                </div>
              </div>

              <div className="bg-[#060e21] p-5 rounded-2xl border border-slate-800 space-y-4">
                <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider">Sensors & Quality</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div className="p-3 bg-slate-900 rounded-xl border border-slate-800">
                    <span className="text-[10px] text-slate-400 uppercase font-bold">TDS Level</span>
                    <p className="text-xl font-black text-emerald-400 mt-1">{tdsLevel} PPM</p>
                  </div>
                  <div className="p-3 bg-slate-900 rounded-xl border border-slate-800">
                    <span className="text-[10px] text-slate-400 uppercase font-bold">pH Balance</span>
                    <p className="text-xl font-black text-cyan-400 mt-1">{phLevel}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Tab 5: Financials Tab */}
        {activeTab === 'financials' && (
          <div className="bg-[#0b1730] border border-slate-800 rounded-2xl p-6 shadow-md space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between pb-4 border-b border-slate-800 gap-4">
              <div>
                <h2 className="font-bold text-lg text-slate-100">Financial Ledger & Expenses</h2>
                <p className="text-xs text-slate-400">Track revenue sales and station expenses</p>
              </div>
              <button
                onClick={() => setIsAddExpenseModalOpen(true)}
                className="bg-cyan-600 hover:bg-cyan-500 text-white text-xs px-4 py-2 rounded-lg font-semibold flex items-center gap-1.5 self-start cursor-pointer"
              >
                <PlusIcon className="w-4 h-4" /> Log Expense
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-[#060e21] p-4 rounded-xl border border-slate-800">
                <span className="text-xs text-slate-400 font-semibold">Today Revenue</span>
                <p className="text-2xl font-black text-cyan-400 mt-1">₱{todayRevenue}</p>
              </div>
              <div className="bg-[#060e21] p-4 rounded-xl border border-slate-800">
                <span className="text-xs text-slate-400 font-semibold">Expenses Logged</span>
                <p className="text-2xl font-black text-rose-400 mt-1">
                  ₱{expenses.reduce((s, e) => s + e.amount, 0)}
                </p>
              </div>
              <div className="bg-[#060e21] p-4 rounded-xl border border-slate-800">
                <span className="text-xs text-slate-400 font-semibold">Net Income</span>
                <p className="text-2xl font-black text-emerald-400 mt-1">
                  ₱{todayRevenue - expenses.reduce((s, e) => s + e.amount, 0)}
                </p>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Modal: New Order Modal */}
      {isNewOrderModalOpen && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#0b1730] border border-slate-800 rounded-2xl w-full max-w-md p-6 shadow-2xl space-y-4">
            <div className="flex justify-between items-center border-b border-slate-800 pb-3">
              <h3 className="font-bold text-slate-100 text-sm">Create New Counter Order</h3>
              <button onClick={() => setIsNewOrderModalOpen(false)} className="text-slate-400 hover:text-white cursor-pointer">
                <XIcon className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleCreateOrder} className="space-y-3 text-xs">
              <div>
                <label className="block text-slate-300 font-medium mb-1">Customer Name / Walk-in</label>
                <input
                  type="text"
                  name="customer"
                  placeholder="e.g. Maria Santos or Walk-in Customer"
                  className="w-full bg-[#060e21] border border-slate-700 rounded-lg px-3 py-2 text-slate-100"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-300 font-medium mb-1">Order Type</label>
                  <select name="type" className="w-full bg-[#060e21] border border-slate-700 rounded-lg px-3 py-2 text-slate-100">
                    <option value="Walk-in">Walk-in</option>
                    <option value="Delivery">Delivery</option>
                  </select>
                </div>
                <div>
                  <label className="block text-slate-300 font-medium mb-1">Amount (₱)</label>
                  <input
                    type="number"
                    name="amount"
                    defaultValue={35}
                    className="w-full bg-[#060e21] border border-slate-700 rounded-lg px-3 py-2 text-slate-100"
                  />
                </div>
              </div>

              <div>
                <label className="block text-slate-300 font-medium mb-1">Items Description</label>
                <input
                  type="text"
                  name="items"
                  defaultValue="1x 5-Gal Slim Container Refill"
                  className="w-full bg-[#060e21] border border-slate-700 rounded-lg px-3 py-2 text-slate-100"
                />
              </div>

              <div>
                <label className="block text-slate-300 font-medium mb-1">Payment Status</label>
                <select name="paymentStatus" className="w-full bg-[#060e21] border border-slate-700 rounded-lg px-3 py-2 text-slate-100">
                  <option value="Paid (Cash)">Paid (Cash)</option>
                  <option value="Paid (GCash)">Paid (GCash)</option>
                  <option value="Unpaid (Pay Later)">Unpaid (Pay Later)</option>
                </select>
              </div>

              <div className="pt-2 flex gap-2">
                <button
                  type="button"
                  onClick={() => setIsNewOrderModalOpen(false)}
                  className="w-1/2 bg-slate-800 hover:bg-slate-700 text-slate-300 py-2.5 rounded-lg font-semibold cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="w-1/2 bg-cyan-500 hover:bg-cyan-400 text-slate-950 py-2.5 rounded-lg font-bold cursor-pointer"
                >
                  Submit Order
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal: Add Expense Modal */}
      {isAddExpenseModalOpen && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#0b1730] border border-slate-800 rounded-2xl w-full max-w-md p-6 shadow-2xl space-y-4">
            <div className="flex justify-between items-center border-b border-slate-800 pb-3">
              <h3 className="font-bold text-slate-100 text-sm">Log New Station Expense</h3>
              <button onClick={() => setIsAddExpenseModalOpen(false)} className="text-slate-400 hover:text-white cursor-pointer">
                <XIcon className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleAddExpense} className="space-y-3 text-xs">
              <div>
                <label className="block text-slate-300 font-medium mb-1">Expense Description</label>
                <input
                  type="text"
                  name="description"
                  placeholder="e.g. Filter Cartridge Replacement"
                  className="w-full bg-[#060e21] border border-slate-700 rounded-lg px-3 py-2 text-slate-100"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-300 font-medium mb-1">Category</label>
                  <select name="category" className="w-full bg-[#060e21] border border-slate-700 rounded-lg px-3 py-2 text-slate-100">
                    <option value="Maintenance">Maintenance</option>
                    <option value="Fuel">Fuel</option>
                    <option value="Supplies">Supplies</option>
                    <option value="Utilities">Utilities</option>
                  </select>
                </div>
                <div>
                  <label className="block text-slate-300 font-medium mb-1">Amount (₱)</label>
                  <input
                    type="number"
                    name="amount"
                    placeholder="100"
                    className="w-full bg-[#060e21] border border-slate-700 rounded-lg px-3 py-2 text-slate-100"
                    required
                  />
                </div>
              </div>

              <div className="pt-2 flex gap-2">
                <button
                  type="button"
                  onClick={() => setIsAddExpenseModalOpen(false)}
                  className="w-1/2 bg-slate-800 hover:bg-slate-700 text-slate-300 py-2.5 rounded-lg font-semibold cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="w-1/2 bg-cyan-500 hover:bg-cyan-400 text-slate-950 py-2.5 rounded-lg font-bold cursor-pointer"
                >
                  Save Expense
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal: Add Customer Modal */}
      {isAddCustomerModalOpen && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#0b1730] border border-slate-800 rounded-2xl w-full max-w-md p-6 shadow-2xl space-y-4">
            <div className="flex justify-between items-center border-b border-slate-800 pb-3">
              <h3 className="font-bold text-slate-100 text-sm">Register New Customer</h3>
              <button onClick={() => setIsAddCustomerModalOpen(false)} className="text-slate-400 hover:text-white cursor-pointer">
                <XIcon className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleAddCustomer} className="space-y-3 text-xs">
              <div>
                <label className="block text-slate-300 font-medium mb-1">Full Name</label>
                <input
                  type="text"
                  name="fullName"
                  placeholder="e.g. Juan Dela Cruz"
                  className="w-full bg-[#060e21] border border-slate-700 rounded-lg px-3 py-2 text-slate-100"
                  required
                />
              </div>

              <div>
                <label className="block text-slate-300 font-medium mb-1">Contact Number</label>
                <input
                  type="text"
                  name="contact"
                  placeholder="e.g. 0917-000-1122"
                  className="w-full bg-[#060e21] border border-slate-700 rounded-lg px-3 py-2 text-slate-100"
                />
              </div>

              <div>
                <label className="block text-slate-300 font-medium mb-1">Address / Zone</label>
                <input
                  type="text"
                  name="address"
                  placeholder="e.g. Zone 4, Poblacion, Maramag"
                  className="w-full bg-[#060e21] border border-slate-700 rounded-lg px-3 py-2 text-slate-100"
                />
              </div>

              <div className="pt-2 flex gap-2">
                <button
                  type="button"
                  onClick={() => setIsAddCustomerModalOpen(false)}
                  className="w-1/2 bg-slate-800 hover:bg-slate-700 text-slate-300 py-2.5 rounded-lg font-semibold cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="w-1/2 bg-cyan-500 hover:bg-cyan-400 text-slate-950 py-2.5 rounded-lg font-bold cursor-pointer"
                >
                  Register
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal: Receipt View Modal */}
      {selectedReceiptOrder && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#0b1730] border border-slate-800 rounded-2xl w-full max-w-xs p-5 shadow-2xl space-y-4 text-xs">
            <div className="text-center border-b border-slate-800 pb-3">
              <h4 className="font-bold text-slate-100 text-sm">GARBUSA WATER REFILLING STATION</h4>
              <p className="text-[10px] text-slate-400">Poblacion, Maramag • WRSMS v3.2</p>
            </div>

            <div className="space-y-2 text-slate-300">
              <div className="flex justify-between">
                <span>Receipt No:</span>
                <span className="font-mono font-bold text-cyan-400">{selectedReceiptOrder.id}</span>
              </div>
              <div className="flex justify-between">
                <span>Customer:</span>
                <span className="font-semibold text-slate-100">{selectedReceiptOrder.customer}</span>
              </div>
              <div className="flex justify-between">
                <span>Type & Time:</span>
                <span>{selectedReceiptOrder.type} ({selectedReceiptOrder.time})</span>
              </div>
              <div className="pt-2 border-t border-slate-800">
                <span className="text-slate-400 block mb-1">Items:</span>
                <p className="font-medium text-slate-200">{selectedReceiptOrder.items}</p>
              </div>
              <div className="flex justify-between pt-2 border-t border-slate-800 text-sm font-bold">
                <span>Total Amount:</span>
                <span className="text-cyan-400">₱{selectedReceiptOrder.amount}</span>
              </div>
            </div>

            <button
              onClick={() => setSelectedReceiptOrder(null)}
              className="w-full bg-slate-800 hover:bg-slate-700 text-slate-200 py-2 rounded-lg font-semibold cursor-pointer"
            >
              Close Receipt
            </button>
          </div>
        </div>
      )}
    </div>
  );
}