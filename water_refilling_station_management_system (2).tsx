import React, { useState, useEffect, useMemo, useRef } from 'react';

// --- INITIAL MOCK DATA ---
const INITIAL_CUSTOMERS = [
  { id: 'CUST-001', name: 'Maria Santos', phone: '0917-123-4567', address: 'Poblacion Zone 3, Maramag', borrowedSlim: 4, borrowedRound: 2, totalOrders: 38, balance: 0 },
  { id: 'CUST-002', name: 'Barangay Health Center', phone: '0928-888-9911', address: 'Main St, Maramag', borrowedSlim: 12, borrowedRound: 0, totalOrders: 112, balance: 350 },
  { id: 'CUST-003', name: 'Juan Dela Cruz', phone: '0905-555-2233', address: 'Subdivision Phase 2, Maramag', borrowedSlim: 2, borrowedRound: 1, totalOrders: 14, balance: 0 },
  { id: 'CUST-004', name: 'Garbusa Eatery', phone: '0919-777-3344', address: 'Public Market Site, Maramag', borrowedSlim: 8, borrowedRound: 5, totalOrders: 85, balance: 120 },
];

const INITIAL_ORDERS = [
  {
    id: 'ORD-1092',
    customerName: 'Maria Santos',
    phone: '0917-123-4567',
    address: 'Poblacion Zone 3, Maramag',
    orderType: 'Delivery',
    items: [
      { name: '5-Gal Slim Container Refill', qty: 3, price: 35 },
      { name: '5-Gal Round Container Refill', qty: 1, price: 35 }
    ],
    totalAmount: 140,
    paymentMethod: 'GCash',
    paymentStatus: 'Paid',
    status: 'Out for Delivery',
    rider: 'Rider Alex',
    borrowedSlimQty: 0,
    returnedSlimQty: 0,
    timestamp: '10:15 AM'
  },
  {
    id: 'ORD-1093',
    customerName: 'Garbusa Eatery',
    phone: '0919-777-3344',
    address: 'Public Market Site, Maramag',
    orderType: 'Delivery',
    items: [
      { name: '5-Gal Slim Container Refill', qty: 5, price: 35 },
      { name: 'Alkaline Water Bottle 1L', qty: 4, price: 25 }
    ],
    totalAmount: 275,
    paymentMethod: 'Pay Later',
    paymentStatus: 'Unpaid',
    status: 'Refill in Progress',
    rider: 'Rider Ben',
    borrowedSlimQty: 5,
    returnedSlimQty: 3,
    timestamp: '10:42 AM'
  },
  {
    id: 'ORD-1094',
    customerName: 'Walk-in Customer',
    phone: 'N/A',
    address: 'Counter Pickup',
    orderType: 'Walk-in',
    items: [
      { name: '5-Gal Round Container Refill', qty: 2, price: 35 }
    ],
    totalAmount: 70,
    paymentMethod: 'Cash',
    paymentStatus: 'Paid',
    status: 'Completed',
    rider: 'Counter Direct',
    borrowedSlimQty: 0,
    returnedSlimQty: 0,
    timestamp: '11:05 AM'
  }
];

const INITIAL_EXPENSES = [
  { id: 1, category: 'Electricity', amount: 3400, note: 'Power bill for RO Filtration Pumps', date: '2026-10-01' },
  { id: 2, category: 'Gasoline', amount: 850, note: 'Delivery Trike Refuel (Rider Alex)', date: '2026-10-02' },
  { id: 3, category: 'Staff Payroll', amount: 1500, note: 'Daily wages for station helper & riders', date: '2026-10-02' },
  { id: 4, category: 'Filter Replacement', amount: 1200, note: '5-Micron Sediment Pre-Filter replacement', date: '2026-09-28' },
];

export default function App() {
  const [theme, setTheme] = useState('dark');
  const [activeTab, setActiveTab] = useState('pos'); // pos, orders, customers, station, financials

  // Core Data States
  const [customers, setCustomers] = useState(INITIAL_CUSTOMERS);
  const [orders, setOrders] = useState(INITIAL_ORDERS);
  const [expenses, setExpenses] = useState(INITIAL_EXPENSES);

  // Tank & Water Quality State
  const [purifiedTankLiters, setPurifiedTankLiters] = useState(3800); // Out of 5000L
  const [rawWaterMeter, setRawWaterMeter] = useState(14520); // m3 or Gallons
  const [purifiedWaterMeter, setPurifiedWaterMeter] = useState(11840);
  const [tdsLevel, setTdsLevel] = useState(12); // PPM
  const [phLevel, setPhLevel] = useState(7.4);
  const [turbidity, setTurbidity] = useState(0.2); // NTU

  // Container Inventory State
  const [inventory, setInventory] = useState({
    cleanSlim: 84,
    cleanRound: 42,
    inTransitSlim: 26,
    inTransitRound: 10,
    toWashSlim: 15,
    toWashRound: 8,
    damaged: 3
  });

  // Filter Maintenance Lifespan (% Remaining)
  const [filters, setFilters] = useState([
    { id: 1, name: 'Sediment Pre-Filter (5 Micron)', health: 78, nextChange: '25 Days' },
    { id: 2, name: 'Activated Carbon Filter', health: 62, nextChange: '18 Days' },
    { id: 3, name: 'Reverse Osmosis (RO) Membrane', health: 91, nextChange: '110 Days' },
    { id: 4, name: 'Ultraviolet (UV) Sterilizer Tube', health: 45, nextChange: '8 Days' },
  ]);

  // Modals
  const [showNewOrderModal, setShowNewOrderModal] = useState(false);
  const [showReceiptModal, setShowReceiptModal] = useState(null); // holds order object
  const [showReturnModal, setShowReturnModal] = useState(null); // holds customer object
  const [showExpenseModal, setShowExpenseModal] = useState(false);
  const [showMeterModal, setShowMeterModal] = useState(false);

  // Search & Filters
  const [orderSearch, setOrderSearch] = useState('');
  const [customerSearch, setCustomerSearch] = useState('');

  // Toggle Theme
  const toggleTheme = () => setTheme(prev => prev === 'dark' ? 'light' : 'dark');

  // Calculated Stats
  const totalSalesToday = useMemo(() => {
    return orders.reduce((sum, ord) => sum + (ord.paymentStatus === 'Paid' ? ord.totalAmount : 0), 0);
  }, [orders]);

  const totalUnpaid = useMemo(() => {
    return orders.reduce((sum, ord) => sum + (ord.paymentStatus === 'Unpaid' ? ord.totalAmount : 0), 0);
  }, [orders]);

  const activeDeliveriesCount = useMemo(() => {
    return orders.filter(o => o.status === 'Out for Delivery' || o.status === 'Refill in Progress').length;
  }, [orders]);

  const totalBorrowedContainers = useMemo(() => {
    return customers.reduce((acc, c) => ({
      slim: acc.slim + c.borrowedSlim,
      round: acc.round + c.borrowedRound
    }), { slim: 0, round: 0 });
  }, [customers]);

  const isDark = theme === 'dark';
  const bgClass = isDark ? 'bg-slate-950 text-slate-100' : 'bg-slate-50 text-slate-800';
  const cardBg = isDark ? 'bg-slate-900/90 border-slate-800 shadow-xl' : 'bg-white border-slate-200 shadow-md';
  const subText = isDark ? 'text-slate-400' : 'text-slate-500';

  return (
    <div className={`min-h-screen font-sans ${bgClass} transition-colors duration-200 flex flex-col`}>
      {/* --- TOP NAVBAR & STATION HEADER --- */}
      <header className={`border-b ${isDark ? 'border-slate-800 bg-slate-900/80' : 'border-slate-200 bg-white'} sticky top-0 z-40 backdrop-blur-md px-4 lg:px-8 py-3.5 flex flex-wrap items-center justify-between gap-4`}>
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center text-white font-black text-xl shadow-lg shadow-cyan-500/25">
            🚰
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-lg font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 via-blue-400 to-indigo-400">
                GARBUSA WATER REFILLING STATION
              </h1>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-cyan-500/10 border border-cyan-500/30 text-cyan-400">
                WRSMS v3.2
              </span>
            </div>
            <p className={`text-xs ${subText}`}>Poblacion, Maramag • Station Operator: On-Duty</p>
          </div>
        </div>

        {/* Global Key Stats Bar */}
        <div className="hidden md:flex items-center gap-6 text-xs">
          <div className="flex flex-col">
            <span className={subText}>Today's Revenue</span>
            <span className="font-bold text-emerald-400 text-sm">₱{totalSalesToday.toLocaleString()}</span>
          </div>
          <div className="h-7 w-[1px] bg-slate-700/50" />
          <div className="flex flex-col">
            <span className={subText}>Purified Tank</span>
            <span className="font-bold text-cyan-400 text-sm">{purifiedTankLiters} / 5,000 L</span>
          </div>
          <div className="h-7 w-[1px] bg-slate-700/50" />
          <div className="flex flex-col">
            <span className={subText}>Borrowed Containers</span>
            <span className="font-bold text-amber-400 text-sm">{totalBorrowedContainers.slim} Slim • {totalBorrowedContainers.round} Rd</span>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-3">
          <button
            onClick={() => setShowNewOrderModal(true)}
            className="px-4 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-semibold text-xs shadow-lg shadow-cyan-500/20 flex items-center gap-2 transition-all transform hover:scale-[1.02]"
          >
            <span>+</span> New Order / Refill
          </button>
          
          <button
            onClick={toggleTheme}
            className={`p-2.5 rounded-xl border ${cardBg} hover:opacity-80 transition-opacity`}
            title="Toggle Theme"
          >
            {isDark ? '☀️' : '🌙'}
          </button>
        </div>
      </header>

      {/* --- MAIN NAVIGATION TABS --- */}
      <div className={`border-b ${isDark ? 'border-slate-800 bg-slate-900/40' : 'border-slate-200 bg-slate-100'} px-4 lg:px-8`}>
        <nav className="flex space-x-2 overflow-x-auto py-2 scrollbar-none">
          {[
            { id: 'pos', label: 'POS & Counter', icon: '🛒' },
            { id: 'orders', label: 'Active Deliveries & Orders', icon: '🚚', badge: activeDeliveriesCount },
            { id: 'customers', label: 'Customer Container Ledger', icon: '👥' },
            { id: 'station', label: 'Purification & Tank Monitor', icon: '🧪' },
            { id: 'financials', label: 'Sales & Expenses', icon: '📊' },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-semibold whitespace-nowrap transition-all ${
                activeTab === tab.id
                  ? 'bg-cyan-500 text-white shadow-md shadow-cyan-500/20'
                  : `${subText} hover:bg-slate-800/20 hover:text-cyan-400`
              }`}
            >
              <span>{tab.icon}</span>
              <span>{tab.label}</span>
              {tab.badge !== undefined && tab.badge > 0 && (
                <span className="px-1.5 py-0.5 rounded-full bg-amber-500 text-slate-950 font-black text-[10px]">
                  {tab.badge}
                </span>
              )}
            </button>
          ))}
        </nav>
      </div>

      {/* --- DASHBOARD CONTENT PANELS --- */}
      <main className="flex-1 p-4 lg:p-8 max-w-7xl w-full mx-auto space-y-6">
        
        {/* TAB 1: POS & LIVE COUNTER */}
        {activeTab === 'pos' && (
          <PosCounterView 
            isDark={isDark}
            cardBg={cardBg}
            subText={subText}
            orders={orders}
            customers={customers}
            onOpenNewOrder={() => setShowNewOrderModal(true)}
            onViewReceipt={(order) => setShowReceiptModal(order)}
            onQuickStatusChange={(orderId, newStatus) => {
              setOrders(orders.map(o => o.id === orderId ? { ...o, status: newStatus } : o));
            }}
            purifiedTankLiters={purifiedTankLiters}
            tdsLevel={tdsLevel}
            phLevel={phLevel}
          />
        )}

        {/* TAB 2: ACTIVE DELIVERIES & ORDER LIST */}
        {activeTab === 'orders' && (
          <OrdersDeliveryView 
            isDark={isDark}
            cardBg={cardBg}
            subText={subText}
            orders={orders}
            setOrders={setOrders}
            searchQuery={orderSearch}
            setSearchQuery={setOrderSearch}
            onViewReceipt={(order) => setShowReceiptModal(order)}
          />
        )}

        {/* TAB 3: CUSTOMER CONTAINER LEDGER */}
        {activeTab === 'customers' && (
          <CustomerLedgerView 
            isDark={isDark}
            cardBg={cardBg}
            subText={subText}
            customers={customers}
            setCustomers={setCustomers}
            searchQuery={customerSearch}
            setSearchQuery={setCustomerSearch}
            onOpenReturnModal={(cust) => setShowReturnModal(cust)}
          />
        )}

        {/* TAB 4: PURIFICATION & TANK MONITOR */}
        {activeTab === 'station' && (
          <StationMonitorView 
            isDark={isDark}
            cardBg={cardBg}
            subText={subText}
            purifiedTankLiters={purifiedTankLiters}
            setPurifiedTankLiters={setPurifiedTankLiters}
            rawWaterMeter={rawWaterMeter}
            purifiedWaterMeter={purifiedWaterMeter}
            tdsLevel={tdsLevel}
            phLevel={phLevel}
            turbidity={turbidity}
            inventory={inventory}
            setInventory={setInventory}
            filters={filters}
            setFilters={setFilters}
            onOpenMeterModal={() => setShowMeterModal(true)}
          />
        )}

        {/* TAB 5: SALES & FINANCIAL EXPENSES */}
        {activeTab === 'financials' && (
          <FinancialsView 
            isDark={isDark}
            cardBg={cardBg}
            subText={subText}
            orders={orders}
            expenses={expenses}
            onOpenAddExpense={() => setShowExpenseModal(true)}
          />
        )}

      </main>

      {/* --- MODAL DIALOGS --- */}

      {/* 1. NEW ORDER / POS MODAL */}
      {showNewOrderModal && (
        <NewOrderModal 
          isDark={isDark}
          cardBg={cardBg}
          subText={subText}
          customers={customers}
          onClose={() => setShowNewOrderModal(false)}
          onSubmitOrder={(newOrder) => {
            setOrders([newOrder, ...orders]);
            // Deduct tank water (~19 Liters per 5-gallon container)
            const totalContainers = newOrder.items.reduce((s, i) => s + (i.name.includes('5-Gal') ? i.qty : 0), 0);
            setPurifiedTankLiters(prev => Math.max(0, prev - totalContainers * 19));
            // Update customer borrowed container count if applicable
            if (newOrder.customerId && newOrder.orderType === 'Delivery') {
              setCustomers(customers.map(c => {
                if (c.id === newOrder.customerId) {
                  return {
                    ...c,
                    borrowedSlim: c.borrowedSlim + (newOrder.borrowedSlimQty || 0),
                    totalOrders: c.totalOrders + 1,
                    balance: newOrder.paymentStatus === 'Unpaid' ? c.balance + newOrder.totalAmount : c.balance
                  };
                }
                return c;
              }));
            }
            setShowNewOrderModal(false);
            setShowReceiptModal(newOrder);
          }}
        />
      )}

      {/* 2. RECEIPT PREVIEW MODAL */}
      {showReceiptModal && (
        <ReceiptModal 
          isDark={isDark}
          cardBg={cardBg}
          subText={subText}
          order={showReceiptModal}
          onClose={() => setShowReceiptModal(null)}
        />
      )}

      {/* 3. RECORD CONTAINER RETURN MODAL */}
      {showReturnModal && (
        <ContainerReturnModal 
          isDark={isDark}
          cardBg={cardBg}
          subText={subText}
          customer={showReturnModal}
          onClose={() => setShowReturnModal(null)}
          onConfirmReturn={(returnedSlim, returnedRound) => {
            setCustomers(customers.map(c => {
              if (c.id === showReturnModal.id) {
                return {
                  ...c,
                  borrowedSlim: Math.max(0, c.borrowedSlim - returnedSlim),
                  borrowedRound: Math.max(0, c.borrowedRound - returnedRound)
                };
              }
              return c;
            }));
            // Update inventory washed container intake
            setInventory(prev => ({
              ...prev,
              toWashSlim: prev.toWashSlim + returnedSlim,
              toWashRound: prev.toWashRound + returnedRound
            }));
            setShowReturnModal(null);
          }}
        />
      )}

      {/* 4. EXPENSE LOG MODAL */}
      {showExpenseModal && (
        <ExpenseModal 
          isDark={isDark}
          cardBg={cardBg}
          subText={subText}
          onClose={() => setShowExpenseModal(false)}
          onAddExpense={(exp) => {
            setExpenses([{ ...exp, id: Date.now() }, ...expenses]);
            setShowExpenseModal(false);
          }}
        />
      )}

      {/* 5. METER LOGGING MODAL */}
      {showMeterModal && (
        <MeterReadingModal 
          isDark={isDark}
          cardBg={cardBg}
          subText={subText}
          rawWaterMeter={rawWaterMeter}
          purifiedWaterMeter={purifiedWaterMeter}
          onClose={() => setShowMeterModal(false)}
          onUpdateMeters={(newRaw, newPurified) => {
            setRawWaterMeter(newRaw);
            setPurifiedWaterMeter(newPurified);
            setShowMeterModal(false);
          }}
        />
      )}

    </div>
  );
}

// ==========================================
// SUB-COMPONENTS (TABS & MODALS)
// ==========================================

function PosCounterView({ isDark, cardBg, subText, orders, customers, onOpenNewOrder, onViewReceipt, onQuickStatusChange, purifiedTankLiters, tdsLevel, phLevel }) {
  const recentOrders = orders.slice(0, 5);

  return (
    <div className="space-y-6">
      {/* Top Banner Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className={`p-5 rounded-2xl border ${cardBg} flex items-center justify-between`}>
          <div>
            <span className={`text-xs uppercase font-bold tracking-wider ${subText}`}>Station Tank Level</span>
            <div className="text-2xl font-black mt-1 text-cyan-400">{purifiedTankLiters} <span className="text-sm font-normal text-slate-400">Liters</span></div>
            <div className="text-[11px] text-emerald-400 mt-1">Capacity: 5,000 L (76% Full)</div>
          </div>
          <div className="w-12 h-12 rounded-2xl bg-cyan-500/10 flex items-center justify-center text-2xl">💧</div>
        </div>

        <div className={`p-5 rounded-2xl border ${cardBg} flex items-center justify-between`}>
          <div>
            <span className={`text-xs uppercase font-bold tracking-wider ${subText}`}>Water Quality Index</span>
            <div className="text-2xl font-black mt-1 text-emerald-400">{tdsLevel} <span className="text-sm font-normal text-slate-400">PPM (TDS)</span></div>
            <div className="text-[11px] text-slate-400 mt-1">pH Level: <span className="text-emerald-400 font-bold">{phLevel}</span> (Optimal)</div>
          </div>
          <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 flex items-center justify-center text-2xl">🧪</div>
        </div>

        <div className={`p-5 rounded-2xl border ${cardBg} flex items-center justify-between`}>
          <div>
            <span className={`text-xs uppercase font-bold tracking-wider ${subText}`}>Active Refills Today</span>
            <div className="text-2xl font-black mt-1 text-blue-400">{orders.length} <span className="text-sm font-normal text-slate-400">Orders</span></div>
            <div className="text-[11px] text-cyan-400 mt-1">Walk-in: {orders.filter(o=>o.orderType==='Walk-in').length} • Delivery: {orders.filter(o=>o.orderType==='Delivery').length}</div>
          </div>
          <div className="w-12 h-12 rounded-2xl bg-blue-500/10 flex items-center justify-center text-2xl">📦</div>
        </div>

        <div 
          onClick={onOpenNewOrder}
          className="p-5 rounded-2xl border border-cyan-500/40 bg-gradient-to-br from-cyan-600/20 to-blue-600/20 hover:from-cyan-600/30 hover:to-blue-600/30 cursor-pointer flex flex-col justify-center items-center text-center group transition-all"
        >
          <div className="w-10 h-10 rounded-full bg-cyan-500 text-slate-950 font-black text-xl flex items-center justify-center shadow-lg shadow-cyan-500/30 group-hover:scale-110 transition-transform">
            +
          </div>
          <span className="text-xs font-bold mt-2 text-cyan-300">Create New Counter Order</span>
        </div>
      </div>

      {/* POS Quick Product Grid & Live Feed */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Container Refill Price Quick Catalog */}
        <div className={`lg:col-span-1 p-6 rounded-2xl border ${cardBg} space-y-4`}>
          <div className="flex justify-between items-center">
            <h2 className="font-bold text-sm">Container Refill Rates</h2>
            <span className="text-[10px] bg-slate-800 text-slate-400 px-2 py-0.5 rounded-full">Garbusa Standard</span>
          </div>

          <div className="space-y-3">
            {[
              { name: '5-Gallon Slim Refill', price: 35, desc: 'Purified drinking water with handle', icon: '🍶' },
              { name: '5-Gallon Round Refill', price: 35, desc: 'Standard dispenser bottleneck', icon: '🪣' },
              { name: 'Container Dispenser Set', price: 250, desc: 'New container + Initial Refill', icon: '🚰' },
              { name: 'Alkaline Water Bottle 1L', price: 25, desc: 'High pH mineralized drinking bottle', icon: '🍾' },
              { name: 'Container Cap / Seal Replace', price: 5, desc: 'Sanitary replacement cap', icon: '🔘' },
            ].map((prod, idx) => (
              <div key={idx} className="p-3 rounded-xl border border-slate-700/30 bg-slate-800/20 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{prod.icon}</span>
                  <div>
                    <h3 className="text-xs font-bold">{prod.name}</h3>
                    <p className={`text-[10px] ${subText}`}>{prod.desc}</p>
                  </div>
                </div>
                <div className="text-right">
                  <span className="text-sm font-black text-cyan-400">₱{prod.price}</span>
                </div>
              </div>
            ))}
          </div>

          <button 
            onClick={onOpenNewOrder}
            className="w-full py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs shadow-md transition-all"
          >
            Open Full POS Counter Terminal
          </button>
        </div>

        {/* Live Order Stream Table */}
        <div className={`lg:col-span-2 p-6 rounded-2xl border ${cardBg} space-y-4`}>
          <div className="flex justify-between items-center">
            <div>
              <h2 className="font-bold text-sm">Live Terminal Order Stream</h2>
              <p className={`text-xs ${subText}`}>Real-time status tracking for current counter and delivery orders</p>
            </div>
            <span className="flex items-center gap-1.5 text-xs text-emerald-400 font-semibold">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" /> Live Feed
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className={`border-b ${isDark ? 'border-slate-800 text-slate-400' : 'border-slate-200 text-slate-500'}`}>
                <tr>
                  <th className="pb-3 font-semibold">Order ID</th>
                  <th className="pb-3 font-semibold">Customer</th>
                  <th className="pb-3 font-semibold">Items</th>
                  <th className="pb-3 font-semibold">Amount</th>
                  <th className="pb-3 font-semibold">Status</th>
                  <th className="pb-3 font-semibold text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/40">
                {recentOrders.map((ord) => (
                  <tr key={ord.id} className="hover:bg-slate-800/20">
                    <td className="py-3 font-mono font-bold text-cyan-400">{ord.id}</td>
                    <td className="py-3">
                      <div className="font-semibold">{ord.customerName}</div>
                      <div className={`text-[10px] ${subText}`}>{ord.orderType} • {ord.timestamp}</div>
                    </td>
                    <td className="py-3">
                      {ord.items.map(i => `${i.qty}x ${i.name.replace('5-Gallon ', '')}`).join(', ')}
                    </td>
                    <td className="py-3 font-bold">
                      ₱{ord.totalAmount}
                      <span className={`block text-[10px] ${ord.paymentStatus==='Paid' ? 'text-emerald-400' : 'text-amber-400'}`}>
                        {ord.paymentStatus} ({ord.paymentMethod})
                      </span>
                    </td>
                    <td className="py-3">
                      <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold ${
                        ord.status === 'Completed' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30' :
                        ord.status === 'Out for Delivery' ? 'bg-blue-500/10 text-blue-400 border border-blue-500/30' :
                        'bg-amber-500/10 text-amber-400 border border-amber-500/30'
                      }`}>
                        {ord.status}
                      </span>
                    </td>
                    <td className="py-3 text-right space-x-2">
                      <button 
                        onClick={() => onViewReceipt(ord)}
                        className="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-[11px] font-semibold"
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
  );
}

function OrdersDeliveryView({ isDark, cardBg, subText, orders, setOrders, searchQuery, setSearchQuery, onViewReceipt }) {
  const filteredOrders = orders.filter(o => 
    o.customerName.toLowerCase().includes(searchQuery.toLowerCase()) ||
    o.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
    o.address.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const updateOrderStatus = (id, status) => {
    setOrders(orders.map(o => o.id === id ? { ...o, status } : o));
  };

  const updatePaymentStatus = (id, paymentStatus) => {
    setOrders(orders.map(o => o.id === id ? { ...o, paymentStatus } : o));
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap justify-between items-center gap-4">
        <div>
          <h2 className="text-lg font-bold">Order Dispatch & Delivery Dispatcher</h2>
          <p className={`text-xs ${subText}`}>Manage active refills, rider assignments, and delivery fulfillment status</p>
        </div>

        <div className="w-full sm:w-72">
          <input
            type="text"
            placeholder="Search Order ID, Customer, Address..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className={`w-full px-4 py-2 rounded-xl text-xs border ${isDark ? 'bg-slate-900 border-slate-700 text-slate-100' : 'bg-white border-slate-300'} focus:outline-none focus:border-cyan-500`}
          />
        </div>
      </div>

      {/* Orders Kanban / Grid View */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredOrders.map((ord) => (
          <div key={ord.id} className={`p-5 rounded-2xl border ${cardBg} space-y-4 flex flex-col justify-between`}>
            <div>
              <div className="flex justify-between items-start border-b border-slate-800/40 pb-3">
                <div>
                  <span className="font-mono text-xs font-bold text-cyan-400">{ord.id}</span>
                  <h3 className="font-bold text-sm mt-0.5">{ord.customerName}</h3>
                  <p className={`text-xs ${subText}`}>{ord.phone}</p>
                </div>
                <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold ${
                  ord.orderType === 'Delivery' ? 'bg-indigo-500/10 text-indigo-400 border border-indigo-500/30' : 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/30'
                }`}>
                  {ord.orderType}
                </span>
              </div>

              <div className="py-3 space-y-2 text-xs">
                <div className="flex justify-between">
                  <span className={subText}>Address:</span>
                  <span className="font-semibold text-right max-w-[180px] truncate">{ord.address}</span>
                </div>
                <div className="flex justify-between">
                  <span className={subText}>Items Ordered:</span>
                  <span className="font-bold">{ord.items.map(i => `${i.qty}x ${i.name.split(' ')[0]}`).join(', ')}</span>
                </div>
                <div className="flex justify-between">
                  <span className={subText}>Total Amount:</span>
                  <span className="font-bold text-cyan-400">₱{ord.totalAmount}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className={subText}>Payment:</span>
                  <button 
                    onClick={() => updatePaymentStatus(ord.id, ord.paymentStatus === 'Paid' ? 'Unpaid' : 'Paid')}
                    className={`px-2 py-0.5 rounded text-[10px] font-bold ${ord.paymentStatus === 'Paid' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-rose-500/20 text-rose-400'}`}
                  >
                    {ord.paymentStatus} ({ord.paymentMethod})
                  </button>
                </div>
                <div className="flex justify-between">
                  <span className={subText}>Assigned Rider:</span>
                  <span className="font-semibold">{ord.rider || 'Station Helper'}</span>
                </div>
              </div>
            </div>

            {/* Actions & Status Progress */}
            <div className="pt-3 border-t border-slate-800/40 space-y-2">
              <div className="flex items-center justify-between gap-2">
                <span className={`text-[10px] font-bold ${subText}`}>STAGE:</span>
                <select
                  value={ord.status}
                  onChange={(e) => updateOrderStatus(ord.id, e.target.value)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold border ${isDark ? 'bg-slate-800 border-slate-700 text-slate-100' : 'bg-slate-100 border-slate-300'}`}
                >
                  <option value="Pending">Pending</option>
                  <option value="Refill in Progress">Refill in Progress</option>
                  <option value="Out for Delivery">Out for Delivery</option>
                  <option value="Delivered">Delivered</option>
                  <option value="Completed">Completed</option>
                </select>
              </div>

              <button
                onClick={() => onViewReceipt(ord)}
                className="w-full py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold rounded-lg text-xs"
              >
                Print / View Receipt
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function CustomerLedgerView({ isDark, cardBg, subText, customers, setCustomers, searchQuery, setSearchQuery, onOpenReturnModal }) {
  const filteredCustomers = customers.filter(c =>
    c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    c.phone.includes(searchQuery) ||
    c.address.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap justify-between items-center gap-4">
        <div>
          <h2 className="text-lg font-bold">Customer Directory & Container Loan Ledger</h2>
          <p className={`text-xs ${subText}`}>Track borrowed 5-gallon containers, delivery points, and unpaid balances</p>
        </div>

        <div className="w-full sm:w-72">
          <input
            type="text"
            placeholder="Search Customer Name, Phone, Address..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className={`w-full px-4 py-2 rounded-xl text-xs border ${isDark ? 'bg-slate-900 border-slate-700 text-slate-100' : 'bg-white border-slate-300'} focus:outline-none focus:border-cyan-500`}
          />
        </div>
      </div>

      <div className={`p-6 rounded-2xl border ${cardBg} overflow-x-auto`}>
        <table className="w-full text-left text-xs">
          <thead className={`border-b ${isDark ? 'border-slate-800 text-slate-400' : 'border-slate-200 text-slate-500'}`}>
            <tr>
              <th className="pb-3 font-semibold">Customer Name</th>
              <th className="pb-3 font-semibold">Contact & Address</th>
              <th className="pb-3 font-semibold">Borrowed Slims (5L)</th>
              <th className="pb-3 font-semibold">Borrowed Rounds (5L)</th>
              <th className="pb-3 font-semibold">Account Balance</th>
              <th className="pb-3 font-semibold">Total Orders</th>
              <th className="pb-3 font-semibold text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/40">
            {filteredCustomers.map((cust) => (
              <tr key={cust.id} className="hover:bg-slate-800/20">
                <td className="py-3 font-bold text-cyan-400">{cust.name}</td>
                <td className="py-3">
                  <div>{cust.phone}</div>
                  <div className={`text-[10px] ${subText}`}>{cust.address}</div>
                </td>
                <td className="py-3">
                  <span className={`px-2.5 py-1 rounded-full font-bold ${cust.borrowedSlim > 0 ? 'bg-amber-500/20 text-amber-400' : 'bg-slate-800 text-slate-400'}`}>
                    {cust.borrowedSlim} Containers
                  </span>
                </td>
                <td className="py-3">
                  <span className={`px-2.5 py-1 rounded-full font-bold ${cust.borrowedRound > 0 ? 'bg-amber-500/20 text-amber-400' : 'bg-slate-800 text-slate-400'}`}>
                    {cust.borrowedRound} Containers
                  </span>
                </td>
                <td className="py-3 font-bold">
                  {cust.balance > 0 ? (
                    <span className="text-rose-400">₱{cust.balance} Unpaid</span>
                  ) : (
                    <span className="text-emerald-400">₱0 (Cleared)</span>
                  )}
                </td>
                <td className="py-3 font-semibold">{cust.totalOrders} Completed</td>
                <td className="py-3 text-right">
                  <button
                    onClick={() => onOpenReturnModal(cust)}
                    className="px-3 py-1.5 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-bold rounded-lg text-xs shadow-md"
                  >
                    Record Container Return
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function StationMonitorView({ isDark, cardBg, subText, purifiedTankLiters, setPurifiedTankLiters, rawWaterMeter, purifiedWaterMeter, tdsLevel, phLevel, turbidity, inventory, setInventory, filters, setFilters, onOpenMeterModal }) {
  return (
    <div className="space-y-6">
      {/* Station Tank & Purification Progress */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Main Tank Indicator */}
        <div className={`p-6 rounded-2xl border ${cardBg} space-y-4`}>
          <h2 className="font-bold text-sm">Main Purified Water Storage Tank</h2>
          
          <div className="relative h-48 w-full bg-slate-800/40 rounded-xl overflow-hidden border border-slate-700/50 flex flex-col justify-end">
            <div 
              style={{ height: `${(purifiedTankLiters / 5000) * 100}%` }} 
              className="bg-gradient-to-t from-blue-600 via-cyan-500 to-sky-400 w-full transition-all duration-500 relative flex items-center justify-center"
            >
              <span className="font-black text-white text-xl drop-shadow-md">
                {Math.round((purifiedTankLiters / 5000) * 100)}%
              </span>
            </div>
          </div>

          <div className="flex justify-between items-center text-xs">
            <span className={subText}>Current Vol: <b className="text-cyan-400">{purifiedTankLiters} L</b></span>
            <span className={subText}>Max Tank Cap: <b>5,000 L</b></span>
          </div>

          <button
            onClick={() => setPurifiedTankLiters(5000)}
            className="w-full py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-cyan-400 font-bold text-xs"
          >
            Refill Main Water Reservoir (Simulate Batch)
          </button>
        </div>

        {/* Quality Meters */}
        <div className={`p-6 rounded-2xl border ${cardBg} space-y-4`}>
          <h2 className="font-bold text-sm">Water Quality Telemetry (Sensors)</h2>

          <div className="space-y-3">
            <div className="p-3 rounded-xl bg-slate-800/20 border border-slate-700/30 flex justify-between items-center">
              <div>
                <span className={`text-[10px] uppercase font-bold ${subText}`}>Total Dissolved Solids (TDS)</span>
                <h3 className="text-xl font-black text-emerald-400">{tdsLevel} PPM</h3>
              </div>
              <span className="text-xs px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-bold">Grade A Purified</span>
            </div>

            <div className="p-3 rounded-xl bg-slate-800/20 border border-slate-700/30 flex justify-between items-center">
              <div>
                <span className={`text-[10px] uppercase font-bold ${subText}`}>pH Level</span>
                <h3 className="text-xl font-black text-cyan-400">{phLevel} pH</h3>
              </div>
              <span className="text-xs px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-400 font-bold">Neutral / Alkaline</span>
            </div>

            <div className="p-3 rounded-xl bg-slate-800/20 border border-slate-700/30 flex justify-between items-center">
              <div>
                <span className={`text-[10px] uppercase font-bold ${subText}`}>Turbidity</span>
                <h3 className="text-xl font-black text-blue-400">{turbidity} NTU</h3>
              </div>
              <span className="text-xs px-2 py-0.5 rounded bg-blue-500/20 text-blue-400 font-bold">Crystal Clear</span>
            </div>
          </div>
        </div>

        {/* Water Meter Readings */}
        <div className={`p-6 rounded-2xl border ${cardBg} space-y-4 flex flex-col justify-between`}>
          <div>
            <h2 className="font-bold text-sm">Station Water Flow Meter Logs</h2>
            <p className={`text-xs ${subText} mb-4`}>Track raw water intake vs actual purified output</p>

            <div className="space-y-3 text-xs">
              <div className="flex justify-between p-3 rounded-xl bg-slate-800/20">
                <span className={subText}>Raw Water Intake Meter:</span>
                <span className="font-mono font-bold text-slate-200">{rawWaterMeter.toLocaleString()} Gallons</span>
              </div>
              <div className="flex justify-between p-3 rounded-xl bg-slate-800/20">
                <span className={subText}>Purified Water Meter:</span>
                <span className="font-mono font-bold text-cyan-400">{purifiedWaterMeter.toLocaleString()} Gallons</span>
              </div>
              <div className="flex justify-between p-3 rounded-xl bg-slate-800/20">
                <span className={subText}>Filtration Efficiency Ratio:</span>
                <span className="font-mono font-bold text-emerald-400">81.5%</span>
              </div>
            </div>
          </div>

          <button
            onClick={onOpenMeterModal}
            className="w-full py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-bold text-xs shadow-md"
          >
            Update Water Meter Readings
          </button>
        </div>

      </div>

      {/* Filter Health Tracker */}
      <div className={`p-6 rounded-2xl border ${cardBg} space-y-4`}>
        <h2 className="font-bold text-sm">Filtration System & UV Sterilizer Maintenance</h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {filters.map((f) => (
            <div key={f.id} className="p-4 rounded-xl border border-slate-700/30 bg-slate-800/20 space-y-3">
              <div className="flex justify-between items-start">
                <h3 className="text-xs font-bold">{f.name}</h3>
                <span className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                  f.health > 50 ? 'bg-emerald-500/20 text-emerald-400' : 'bg-amber-500/20 text-amber-400'
                }`}>
                  {f.health}% Life
                </span>
              </div>

              <div className="w-full h-2 bg-slate-700 rounded-full overflow-hidden">
                <div 
                  style={{ width: `${f.health}%` }} 
                  className={`h-full ${f.health > 50 ? 'bg-emerald-400' : 'bg-amber-400'}`} 
                />
              </div>

              <div className="flex justify-between items-center text-[10px]">
                <span className={subText}>Est. Replacement:</span>
                <span className="font-semibold">{f.nextChange}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function FinancialsView({ isDark, cardBg, subText, orders, expenses, onOpenAddExpense }) {
  const totalRevenue = orders.reduce((sum, o) => sum + (o.paymentStatus === 'Paid' ? o.totalAmount : 0), 0);
  const totalExpenses = expenses.reduce((sum, e) => sum + e.amount, 0);
  const netProfit = totalRevenue - totalExpenses;

  return (
    <div className="space-y-6">
      {/* Financial Summary Stat Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className={`p-5 rounded-2xl border ${cardBg}`}>
          <span className={`text-xs uppercase font-bold tracking-wider ${subText}`}>Total Gross Sales</span>
          <div className="text-2xl font-black mt-1 text-emerald-400">₱{totalRevenue.toLocaleString()}</div>
          <p className={`text-[11px] ${subText} mt-1`}>Calculated from completed paid orders</p>
        </div>

        <div className={`p-5 rounded-2xl border ${cardBg}`}>
          <span className={`text-xs uppercase font-bold tracking-wider ${subText}`}>Total Station Expenses</span>
          <div className="text-2xl font-black mt-1 text-rose-400">₱{totalExpenses.toLocaleString()}</div>
          <p className={`text-[11px] ${subText} mt-1`}>Electricity, Gasoline, Wages & Filters</p>
        </div>

        <div className={`p-5 rounded-2xl border ${cardBg}`}>
          <span className={`text-xs uppercase font-bold tracking-wider ${subText}`}>Estimated Net Profit</span>
          <div className={`text-2xl font-black mt-1 ${netProfit >= 0 ? 'text-cyan-400' : 'text-rose-400'}`}>
            ₱{netProfit.toLocaleString()}
          </div>
          <p className={`text-[11px] ${subText} mt-1`}>Gross Sales minus Total Operating Expenses</p>
        </div>
      </div>

      {/* Expense Log & Action */}
      <div className={`p-6 rounded-2xl border ${cardBg} space-y-4`}>
        <div className="flex justify-between items-center">
          <div>
            <h2 className="font-bold text-sm">Operating Expense Ledger</h2>
            <p className={`text-xs ${subText}`}>Record station utilities, driver fuel allowance, maintenance and staff pay</p>
          </div>
          <button
            onClick={onOpenAddExpense}
            className="px-4 py-2 rounded-xl bg-rose-500 hover:bg-rose-400 text-white font-bold text-xs shadow-md"
          >
            + Add New Expense
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className={`border-b ${isDark ? 'border-slate-800 text-slate-400' : 'border-slate-200 text-slate-500'}`}>
              <tr>
                <th className="pb-3 font-semibold">Category</th>
                <th className="pb-3 font-semibold">Note / Description</th>
                <th className="pb-3 font-semibold">Date</th>
                <th className="pb-3 font-semibold text-right">Amount</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/40">
              {expenses.map((e) => (
                <tr key={e.id} className="hover:bg-slate-800/20">
                  <td className="py-3 font-bold text-amber-400">{e.category}</td>
                  <td className="py-3 text-slate-300">{e.note}</td>
                  <td className={`py-3 ${subText}`}>{e.date}</td>
                  <td className="py-3 text-right font-mono font-bold text-rose-400">₱{e.amount.toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

// ==========================================
// MODAL DIALOG COMPONENTS
// ==========================================

function NewOrderModal({ isDark, cardBg, subText, customers, onClose, onSubmitOrder }) {
  const [selectedCustId, setSelectedCustId] = useState('');
  const [custName, setCustName] = useState('Walk-in Customer');
  const [custPhone, setCustPhone] = useState('');
  const [custAddress, setCustAddress] = useState('Counter Direct');
  const [orderType, setOrderType] = useState('Walk-in'); // Walk-in, Delivery
  const [paymentMethod, setPaymentMethod] = useState('Cash'); // Cash, GCash, Pay Later
  const [paymentStatus, setPaymentStatus] = useState('Paid');

  // Quantities
  const [slimQty, setSlimQty] = useState(1);
  const [roundQty, setRoundQty] = useState(0);
  const [bottleQty, setBottleQty] = useState(0);

  // When customer dropdown changes
  const handleCustomerSelect = (id) => {
    setSelectedCustId(id);
    if (id) {
      const found = customers.find(c => c.id === id);
      if (found) {
        setCustName(found.name);
        setCustPhone(found.phone);
        setCustAddress(found.address);
        setOrderType('Delivery');
      }
    }
  };

  const calculateTotal = () => {
    return (slimQty * 35) + (roundQty * 35) + (bottleQty * 25);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const items = [];
    if (slimQty > 0) items.push({ name: '5-Gal Slim Container Refill', qty: slimQty, price: 35 });
    if (roundQty > 0) items.push({ name: '5-Gal Round Container Refill', qty: roundQty, price: 35 });
    if (bottleQty > 0) items.push({ name: 'Alkaline Water Bottle 1L', qty: bottleQty, price: 25 });

    if (items.length === 0) return alert('Please select at least 1 item.');

    const newOrder = {
      id: `ORD-${Math.floor(1000 + Math.random() * 9000)}`,
      customerId: selectedCustId || null,
      customerName: custName,
      phone: custPhone,
      address: custAddress,
      orderType,
      items,
      totalAmount: calculateTotal(),
      paymentMethod,
      paymentStatus,
      status: orderType === 'Walk-in' ? 'Completed' : 'Refill in Progress',
      rider: orderType === 'Delivery' ? 'Rider Alex' : 'Counter Direct',
      borrowedSlimQty: orderType === 'Delivery' ? slimQty : 0,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    onSubmitOrder(newOrder);
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/70 backdrop-blur-sm flex items-center justify-center p-4">
      <div className={`w-full max-w-lg rounded-2xl border ${cardBg} p-6 space-y-4 shadow-2xl animate-in fade-in zoom-in duration-150`}>
        <div className="flex justify-between items-center border-b border-slate-800 pb-3">
          <h2 className="text-base font-bold">New Refill & POS Order Entry</h2>
          <button onClick={onClose} className="text-slate-400 hover:text-white font-bold">✕</button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4 text-xs">
          <div>
            <label className={`block font-semibold mb-1 ${subText}`}>Select Regular Customer (Optional)</label>
            <select
              value={selectedCustId}
              onChange={(e) => handleCustomerSelect(e.target.value)}
              className={`w-full p-2.5 rounded-xl border ${isDark ? 'bg-slate-800 border-slate-700 text-slate-100' : 'bg-slate-100 border-slate-300'}`}
            >
              <option value="">-- Walk-in / New Customer --</option>
              {customers.map(c => (
                <option key={c.id} value={c.id}>{c.name} ({c.phone})</option>
              ))}
            </select>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className={`block font-semibold mb-1 ${subText}`}>Customer Name</label>
              <input
                type="text"
                required
                value={custName}
                onChange={(e) => setCustName(e.target.value)}
                className={`w-full p-2.5 rounded-xl border ${isDark ? 'bg-slate-800 border-slate-700 text-slate-100' : 'bg-slate-100 border-slate-300'}`}
              />
            </div>
            <div>
              <label className={`block font-semibold mb-1 ${subText}`}>Phone Number</label>
              <input
                type="text"
                value={custPhone}
                onChange={(e) => setCustPhone(e.target.value)}
                className={`w-full p-2.5 rounded-xl border ${isDark ? 'bg-slate-800 border-slate-700 text-slate-100' : 'bg-slate-100 border-slate-300'}`}
              />
            </div>
          </div>

          <div>
            <label className={`block font-semibold mb-1 ${subText}`}>Delivery Address / Notes</label>
            <input
              type="text"
              value={custAddress}
              onChange={(e) => setCustAddress(e.target.value)}
              className={`w-full p-2.5 rounded-xl border ${isDark ? 'bg-slate-800 border-slate-700 text-slate-100' : 'bg-slate-100 border-slate-300'}`}
            />
          </div>

          {/* Item Selector */}
          <div className="p-3 rounded-xl bg-slate-800/30 border border-slate-700/40 space-y-3">
            <span className="font-bold block text-cyan-400">Order Quantities</span>

            <div className="flex justify-between items-center">
              <span>5-Gallon Slim Refill (₱35)</span>
              <div className="flex items-center gap-2">
                <button type="button" onClick={() => setSlimQty(Math.max(0, slimQty - 1))} className="px-2.5 py-1 bg-slate-700 rounded font-bold">-</button>
                <span className="w-6 text-center font-bold">{slimQty}</span>
                <button type="button" onClick={() => setSlimQty(slimQty + 1)} className="px-2.5 py-1 bg-slate-700 rounded font-bold">+</button>
              </div>
            </div>

            <div className="flex justify-between items-center">
              <span>5-Gallon Round Refill (₱35)</span>
              <div className="flex items-center gap-2">
                <button type="button" onClick={() => setRoundQty(Math.max(0, roundQty - 1))} className="px-2.5 py-1 bg-slate-700 rounded font-bold">-</button>
                <span className="w-6 text-center font-bold">{roundQty}</span>
                <button type="button" onClick={() => setRoundQty(roundQty + 1)} className="px-2.5 py-1 bg-slate-700 rounded font-bold">+</button>
              </div>
            </div>

            <div className="flex justify-between items-center">
              <span>Alkaline Water 1L (₱25)</span>
              <div className="flex items-center gap-2">
                <button type="button" onClick={() => setBottleQty(Math.max(0, bottleQty - 1))} className="px-2.5 py-1 bg-slate-700 rounded font-bold">-</button>
                <span className="w-6 text-center font-bold">{bottleQty}</span>
                <button type="button" onClick={() => setBottleQty(bottleQty + 1)} className="px-2.5 py-1 bg-slate-700 rounded font-bold">+</button>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className={`block font-semibold mb-1 ${subText}`}>Payment Mode</label>
              <select
                value={paymentMethod}
                onChange={(e) => setPaymentMethod(e.target.value)}
                className={`w-full p-2.5 rounded-xl border ${isDark ? 'bg-slate-800 border-slate-700 text-slate-100' : 'bg-slate-100 border-slate-300'}`}
              >
                <option value="Cash">Cash</option>
                <option value="GCash">GCash / e-Wallet</option>
                <option value="Pay Later">Pay Later (Credit)</option>
              </select>
            </div>

            <div>
              <label className={`block font-semibold mb-1 ${subText}`}>Payment Status</label>
              <select
                value={paymentStatus}
                onChange={(e) => setPaymentStatus(e.target.value)}
                className={`w-full p-2.5 rounded-xl border ${isDark ? 'bg-slate-800 border-slate-700 text-slate-100' : 'bg-slate-100 border-slate-300'}`}
              >
                <option value="Paid">Paid</option>
                <option value="Unpaid">Unpaid</option>
              </select>
            </div>
          </div>

          <div className="pt-2 flex justify-between items-center border-t border-slate-800">
            <div>
              <span className={subText}>Total Bill:</span>
              <div className="text-xl font-black text-cyan-400">₱{calculateTotal()}</div>
            </div>

            <button
              type="submit"
              className="px-6 py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs shadow-lg shadow-cyan-500/20"
            >
              Submit Order
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

function ReceiptModal({ isDark, cardBg, subText, order, onClose }) {
  return (
    <div className="fixed inset-0 z-50 bg-slate-950/70 backdrop-blur-sm flex items-center justify-center p-4">
      <div className={`w-full max-w-sm rounded-2xl border ${cardBg} p-6 space-y-4 shadow-2xl font-mono text-xs`}>
        <div className="text-center space-y-1 border-b border-dashed border-slate-700 pb-4">
          <h2 className="font-bold text-base text-cyan-400">GARBUSA WATER REFILLING</h2>
          <p className={subText}>Poblacion, Maramag, Bukidnon</p>
          <p className={subText}>Tel: 0917-000-WATER</p>
        </div>

        <div className="space-y-1 py-2 border-b border-dashed border-slate-700">
          <div className="flex justify-between"><span>RECEIPT:</span><span className="font-bold">{order.id}</span></div>
          <div className="flex justify-between"><span>DATE/TIME:</span><span>{order.timestamp}</span></div>
          <div className="flex justify-between"><span>CUSTOMER:</span><span className="font-bold">{order.customerName}</span></div>
          <div className="flex justify-between"><span>PAYMENT:</span><span>{order.paymentMethod} ({order.paymentStatus})</span></div>
        </div>

        <div className="space-y-2 py-2 border-b border-dashed border-slate-700">
          {order.items.map((item, idx) => (
            <div key={idx} className="flex justify-between">
              <span>{item.qty}x {item.name}</span>
              <span>₱{item.qty * item.price}</span>
            </div>
          ))}
        </div>

        <div className="flex justify-between font-bold text-sm py-1">
          <span>TOTAL AMOUNT:</span>
          <span className="text-cyan-400">₱{order.totalAmount}</span>
        </div>

        <div className="text-center pt-2 space-y-3">
          <p className="text-[10px] text-slate-400">Thank you for trusting Garbusa Purified Water! Clean & Safe Drinking Water Always.</p>
          <button
            onClick={onClose}
            className="w-full py-2 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold"
          >
            Close & Print Receipt
          </button>
        </div>
      </div>
    </div>
  );
}

function ContainerReturnModal({ isDark, cardBg, subText, customer, onClose, onConfirmReturn }) {
  const [returnSlim, setReturnSlim] = useState(0);
  const [returnRound, setReturnRound] = useState(0);

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/70 backdrop-blur-sm flex items-center justify-center p-4">
      <div className={`w-full max-w-md rounded-2xl border ${cardBg} p-6 space-y-4 shadow-2xl`}>
        <div className="flex justify-between items-center border-b border-slate-800 pb-3">
          <h2 className="text-sm font-bold">Record Container Return</h2>
          <button onClick={onClose} className="text-slate-400">✕</button>
        </div>

        <div className="space-y-3 text-xs">
          <div className="p-3 rounded-xl bg-slate-800/30">
            <span className="font-bold">{customer.name}</span>
            <p className={subText}>Active Borrowed: {customer.borrowedSlim} Slims, {customer.borrowedRound} Rounds</p>
          </div>

          <div>
            <label className={`block font-semibold mb-1 ${subText}`}>Returned Slim Containers</label>
            <input
              type="number"
              min="0"
              max={customer.borrowedSlim}
              value={returnSlim}
              onChange={(e) => setReturnSlim(Number(e.target.value))}
              className={`w-full p-2.5 rounded-xl border ${isDark ? 'bg-slate-800 border-slate-700' : 'bg-slate-100 border-slate-300'}`}
            />
          </div>

          <div>
            <label className={`block font-semibold mb-1 ${subText}`}>Returned Round Containers</label>
            <input
              type="number"
              min="0"
              max={customer.borrowedRound}
              value={returnRound}
              onChange={(e) => setReturnRound(Number(e.target.value))}
              className={`w-full p-2.5 rounded-xl border ${isDark ? 'bg-slate-800 border-slate-700' : 'bg-slate-100 border-slate-300'}`}
            />
          </div>

          <button
            onClick={() => onConfirmReturn(returnSlim, returnRound)}
            className="w-full py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs"
          >
            Confirm & Balance Container Ledger
          </button>
        </div>
      </div>
    </div>
  );
}

function ExpenseModal({ isDark, cardBg, subText, onClose, onAddExpense }) {
  const [category, setCategory] = useState('Electricity');
  const [amount, setAmount] = useState('');
  const [note, setNote] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!amount) return;
    onAddExpense({
      category,
      amount: Number(amount),
      note,
      date: new Date().toISOString().split('T')[0]
    });
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/70 backdrop-blur-sm flex items-center justify-center p-4">
      <div className={`w-full max-w-md rounded-2xl border ${cardBg} p-6 space-y-4 shadow-2xl`}>
        <div className="flex justify-between items-center border-b border-slate-800 pb-3">
          <h2 className="text-sm font-bold">Log New Station Operating Expense</h2>
          <button onClick={onClose} className="text-slate-400">✕</button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-3 text-xs">
          <div>
            <label className={`block font-semibold mb-1 ${subText}`}>Expense Category</label>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className={`w-full p-2.5 rounded-xl border ${isDark ? 'bg-slate-800 border-slate-700' : 'bg-slate-100 border-slate-300'}`}
            >
              <option value="Electricity">Electricity / Power Bill</option>
              <option value="Gasoline">Gasoline / Trike Delivery Fuel</option>
              <option value="Staff Payroll">Staff / Driver Payroll</option>
              <option value="Filter Replacement">Filter Cartridge Replacement</option>
              <option value="Water Utility Bill">Raw Water Supply Bill</option>
            </select>
          </div>

          <div>
            <label className={`block font-semibold mb-1 ${subText}`}>Amount (₱)</label>
            <input
              type="number"
              required
              placeholder="0.00"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              className={`w-full p-2.5 rounded-xl border ${isDark ? 'bg-slate-800 border-slate-700' : 'bg-slate-100 border-slate-300'}`}
            />
          </div>

          <div>
            <label className={`block font-semibold mb-1 ${subText}`}>Description / Notes</label>
            <input
              type="text"
              placeholder="e.g. RO Pump power bill for October"
              value={note}
              onChange={(e) => setNote(e.target.value)}
              className={`w-full p-2.5 rounded-xl border ${isDark ? 'bg-slate-800 border-slate-700' : 'bg-slate-100 border-slate-300'}`}
            />
          </div>

          <button
            type="submit"
            className="w-full py-2.5 rounded-xl bg-rose-500 hover:bg-rose-400 text-white font-bold text-xs"
          >
            Record Expense
          </button>
        </form>
      </div>
    </div>
  );
}

function MeterReadingModal({ isDark, cardBg, subText, rawWaterMeter, purifiedWaterMeter, onClose, onUpdateMeters }) {
  const [rawMeter, setRawMeter] = useState(rawWaterMeter);
  const [purifiedMeter, setPurifiedMeter] = useState(purifiedWaterMeter);

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/70 backdrop-blur-sm flex items-center justify-center p-4">
      <div className={`w-full max-w-md rounded-2xl border ${cardBg} p-6 space-y-4 shadow-2xl`}>
        <div className="flex justify-between items-center border-b border-slate-800 pb-3">
          <h2 className="text-sm font-bold">Log Water Flow Meter Readings</h2>
          <button onClick={onClose} className="text-slate-400">✕</button>
        </div>

        <div className="space-y-3 text-xs">
          <div>
            <label className={`block font-semibold mb-1 ${subText}`}>Raw Intake Meter (Gallons)</label>
            <input
              type="number"
              value={rawMeter}
              onChange={(e) => setRawMeter(Number(e.target.value))}
              className={`w-full p-2.5 rounded-xl border ${isDark ? 'bg-slate-800 border-slate-700' : 'bg-slate-100 border-slate-300'}`}
            />
          </div>

          <div>
            <label className={`block font-semibold mb-1 ${subText}`}>Purified Water Meter (Gallons)</label>
            <input
              type="number"
              value={purifiedMeter}
              onChange={(e) => setPurifiedMeter(Number(e.target.value))}
              className={`w-full p-2.5 rounded-xl border ${isDark ? 'bg-slate-800 border-slate-700' : 'bg-slate-100 border-slate-300'}`}
            />
          </div>

          <button
            onClick={() => onUpdateMeters(rawMeter, purifiedMeter)}
            className="w-full py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs"
          >
            Save Meter Logs
          </button>
        </div>
      </div>
    </div>
  );
}