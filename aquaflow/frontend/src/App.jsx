import React, { useState, useEffect, useMemo } from 'react';
import { api } from './api';

// --- FALLBACK MOCK DATA (used if backend unreachable) ---
const INITIAL_CUSTOMERS = [
  { id: 'CUST-001', name: 'Maria Santos', phone: '0917-123-4567', address: 'Poblacion Zone 3, Maramag', borrowedSlim: 4, borrowedRound: 2, totalOrders: 38, balance: 0 },
  { id: 'CUST-002', name: 'Barangay Health Center', phone: '0928-888-9911', address: 'Main St, Maramag', borrowedSlim: 12, borrowedRound: 0, totalOrders: 112, balance: 350 },
  { id: 'CUST-003', name: 'Juan Dela Cruz', phone: '0905-555-2233', address: 'Subdivision Phase 2, Maramag', borrowedSlim: 2, borrowedRound: 1, totalOrders: 14, balance: 0 },
  { id: 'CUST-004', name: 'Garbusa Eatery', phone: '0919-777-3344', address: 'Public Market Site, Maramag', borrowedSlim: 8, borrowedRound: 5, totalOrders: 85, balance: 120 },
];
const INITIAL_ORDERS = [
  { id: 'ORD-1092', customerName: 'Maria Santos', phone: '0917-123-4567', address: 'Poblacion Zone 3, Maramag', orderType: 'Delivery', items: [
    { name: '5-Gal Slim Container Refill', qty: 3, price: 35 },
    { name: '5-Gal Round Container Refill', qty: 1, price: 35 }
  ], totalAmount: 140, paymentMethod: 'GCash', paymentStatus: 'Paid', status: 'Out for Delivery', rider: 'Rider Alex', borrowedSlimQty: 0, returnedSlimQty: 0, timestamp: '10:15 AM' },
  { id: 'ORD-1093', customerName: 'Garbusa Eatery', phone: '0919-777-3344', address: 'Public Market Site, Maramag', orderType: 'Delivery', items: [
    { name: '5-Gal Slim Container Refill', qty: 5, price: 35 },
    { name: 'Alkaline Water Bottle 1L', qty: 4, price: 25 }
  ], totalAmount: 275, paymentMethod: 'Pay Later', paymentStatus: 'Unpaid', status: 'Refill in Progress', rider: 'Rider Ben', borrowedSlimQty: 5, returnedSlimQty: 3, timestamp: '10:42 AM' },
  { id: 'ORD-1094', customerName: 'Walk-in Customer', phone: 'N/A', address: 'Counter Pickup', orderType: 'Walk-in', items: [
    { name: '5-Gal Round Container Refill', qty: 2, price: 35 }
  ], totalAmount: 70, paymentMethod: 'Cash', paymentStatus: 'Paid', status: 'Completed', rider: 'Counter Direct', borrowedSlimQty: 0, returnedSlimQty: 0, timestamp: '11:05 AM' }
];
const INITIAL_EXPENSES = [
  { id: 1, category: 'Electricity', amount: 3400, note: 'Power bill for RO Filtration Pumps', date: '2026-10-01' },
  { id: 2, category: 'Gasoline', amount: 850, note: 'Delivery Trike Refuel (Rider Alex)', date: '2026-10-02' },
  { id: 3, category: 'Staff Payroll', amount: 1500, note: 'Daily wages for station helper & riders', date: '2026-10-02' },
  { id: 4, category: 'Filter Replacement', amount: 1200, note: '5-Micron Sediment Pre-Filter replacement', date: '2026-09-28' },
];

export default function App() {
  const [theme, setTheme] = useState('dark');
  const [activeTab, setActiveTab] = useState('pos');

  // Core Data States — Load from API with fallback
  const [customers, setCustomers] = useState([]);
  const [orders, setOrders] = useState([]);
  const [expenses, setExpenses] = useState([]);
  const [loading, setLoading] = useState(true);

  // Station State
  const [purifiedTankLiters, setPurifiedTankLiters] = useState(3800);
  const [rawWaterMeter, setRawWaterMeter] = useState(14520);
  const [purifiedWaterMeter, setPurifiedWaterMeter] = useState(11840);
  const [tdsLevel, setTdsLevel] = useState(12);
  const [phLevel, setPhLevel] = useState(7.4);
  const [turbidity, setTurbidity] = useState(0.2);

  // Inventory & Filters
  const [inventory, setInventory] = useState({
    cleanSlim: 84, cleanRound: 42, inTransitSlim: 26, inTransitRound: 10, toWashSlim: 15, toWashRound: 8, damaged: 3
  });
  const [filters] = useState([
    { id: 1, name: 'Sediment Pre-Filter (5 Micron)', health: 78, nextChange: '25 Days' },
    { id: 2, name: 'Activated Carbon Filter', health: 62, nextChange: '18 Days' },
    { id: 3, name: 'Reverse Osmosis (RO) Membrane', health: 91, nextChange: '110 Days' },
    { id: 4, name: 'Ultraviolet (UV) Sterilizer Tube', health: 45, nextChange: '8 Days' },
  ]);

  // Modals & Search
  const [showNewOrderModal, setShowNewOrderModal] = useState(false);
  const [showReceiptModal, setShowReceiptModal] = useState(null);
  const [showReturnModal, setShowReturnModal] = useState(null);
  const [showExpenseModal, setShowExpenseModal] = useState(false);
  const [showMeterModal, setShowMeterModal] = useState(false);
  const [orderSearch, setOrderSearch] = useState('');
  const [customerSearch, setCustomerSearch] = useState('');

  // --- API DATA LOADER ---
  useEffect(() => {
    async function loadAllData() {
      setLoading(true);
      try {
        const [custData, orderData, expData, stationData] = await Promise.allSettled([
          api.getCustomers(),
          api.getOrders(),
          api.getExpenses(),
          api.getStationStatus()
        ]);

        setCustomers(custData.status === 'fulfilled' ? custData.value : INITIAL_CUSTOMERS);
        setOrders(orderData.status === 'fulfilled' ? orderData.value : INITIAL_ORDERS);
        setExpenses(expData.status === 'fulfilled' ? expData.value : INITIAL_EXPENSES);
        
        if (stationData.status === 'fulfilled') {
          const s = stationData.value;
          setPurifiedTankLiters(s.purified_tank_liters ?? 3800);
          setTdsLevel(s.tds ?? 12);
          setPhLevel(s.ph ?? 7.4);
          setTurbidity(s.turbidity ?? 0.2);
          setRawWaterMeter(s.raw_water_meter ?? 14520);
          setPurifiedWaterMeter(s.purified_water_meter ?? 11840);
        }
      } catch {
        setCustomers(INITIAL_CUSTOMERS);
        setOrders(INITIAL_ORDERS);
        setExpenses(INITIAL_EXPENSES);
      } finally {
        setLoading(false);
      }
    }
    loadAllData();
  }, []);

  const toggleTheme = () => setTheme(prev => prev === 'dark' ? 'light' : 'dark');

  // Calculated Stats
  const totalSalesToday = useMemo(() => orders.reduce((sum, ord) => sum + (ord.paymentStatus === 'Paid' ? ord.totalAmount : 0), 0), [orders]);
  const totalUnpaid = useMemo(() => orders.reduce((sum, ord) => sum + (ord.paymentStatus === 'Unpaid' ? ord.totalAmount : 0), 0), [orders]);
  const activeDeliveriesCount = useMemo(() => orders.filter(o => o.status === 'Out for Delivery' || o.status === 'Refill in Progress').length, [orders]);
  const totalBorrowedContainers = useMemo(() => ({
    slim: customers.reduce((a, c) => a + (c.borrowedSlim || 0), 0),
    round: customers.reduce((a, c) => a + (c.borrowedRound || 0), 0)
  }), [customers]);

  const isDark = theme === 'dark';
  const bgClass = isDark ? 'bg-slate-950 text-slate-100' : 'bg-slate-50 text-slate-800';
  const cardBg = isDark ? 'bg-slate-900/90 border-slate-800 shadow-xl' : 'bg-white border-slate-200 shadow-md';
  const subText = isDark ? 'text-slate-400' : 'text-slate-500';

  // --- ORDER ACTIONS ---
  const handleNewOrder = async (newOrder) => {
    let saved = newOrder;
    try { saved = await api.createOrder(newOrder); } catch {}
    setOrders([saved, ...orders]);
    
    // Deduct tank water
    const totalContainers = newOrder.items.reduce((s, i) => s + (i.name.includes('5-Gal') ? i.qty : 0), 0);
    setPurifiedTankLiters(prev => Math.max(0, prev - totalContainers * 19));

    // Update customer ledger
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
    setShowReceiptModal(saved);
  };

  const handleStatusChange = async (orderId, newStatus) => {
    try { await api.updateOrderStatus(orderId, newStatus); } catch {}
    setOrders(orders.map(o => o.id === orderId ? { ...o, status: newStatus } : o));
  };

  const handlePaymentChange = async (orderId, newPaymentStatus) => {
    try { await api.updatePaymentStatus(orderId, newPaymentStatus); } catch {}
    setOrders(orders.map(o => o.id === orderId ? { ...o, paymentStatus: newPaymentStatus } : o));
  };

  const handleReturnConfirm = async (customerId, returnedSlim, returnedRound) => {
    try { await api.recordReturn(customerId, returnedSlim, returnedRound); } catch {}
    setCustomers(customers.map(c => c.id === customerId ? {
      ...c,
      borrowedSlim: Math.max(0, c.borrowedSlim - returnedSlim),
      borrowedRound: Math.max(0, c.borrowedRound - returnedRound)
    } : c));
    setInventory(prev => ({
      ...prev,
      toWashSlim: prev.toWashSlim + returnedSlim,
      toWashRound: prev.toWashRound + returnedRound
    }));
    setShowReturnModal(null);
  };

  const handleAddExpense = async (exp) => {
    const newExp = { ...exp, id: Date.now() };
    try { await api.addExpense(exp); } catch { setExpenses([newExp, ...expenses]); }
    setExpenses([newExp, ...expenses]);
    setShowExpenseModal(false);
  };

  const handleMeterUpdate = async (newRaw, newPurified) => {
    try { await api.updateMeters(newRaw, newPurified); } catch {}
    setRawWaterMeter(newRaw);
    setPurifiedWaterMeter(newPurified);
    setShowMeterModal(false);
  };

  // --- RENDER ---
  if (loading) return <div className="min-h-screen flex items-center justify-center bg-slate-950 text-white">Loading AquaFlow Dashboard...</div>;

  return (
    <div className={`min-h-screen font-sans ${bgClass} transition-colors duration-200 flex flex-col`}>
      {/* TOP NAVBAR */}
      <header className={`border-b ${isDark ? 'border-slate-800 bg-slate-900/80' : 'border-slate-200 bg-white'} sticky top-0 z-40 backdrop-blur-md px-4 lg:px-8 py-3.5 flex flex-wrap items-center justify-between gap-4`}>
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center text-white font-black text-xl shadow-lg shadow-cyan-500/25">🚰</div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-lg font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 via-blue-400 to-indigo-400">AQUAFLOW WATER REFILLING STATION</h1>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-cyan-500/10 border border-cyan-500/30 text-cyan-400">v3.2</span>
            </div>
            <p className={`text-xs ${subText}`}>Poblacion, Maramag • Station Operator: On-Duty</p>
          </div>
        </div>
        <div className="hidden md:flex items-center gap-6 text-xs">
          <div className="flex flex-col"><span className={subText}>Today's Revenue</span><span className="font-bold text-emerald-400 text-sm">₱{totalSalesToday.toLocaleString()}</span></div>
          <div className="h-7 w-[1px] bg-slate-700/50" />
          <div className="flex flex-col"><span className={subText}>Purified Tank</span><span className="font-bold text-cyan-400 text-sm">{purifiedTankLiters} / 5,000 L</span></div>
          <div className="h-7 w-[1px] bg-slate-700/50" />
          <div className="flex flex-col"><span className={subText}>Borrowed Containers</span><span className="font-bold text-amber-400 text-sm">{totalBorrowedContainers.slim} Slim • {totalBorrowedContainers.round} Rd</span></div>
        </div>
        <div className="flex items-center gap-3">
          <button onClick={() => setShowNewOrderModal(true)} className="px-4 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-semibold text-xs shadow-lg shadow-cyan-500/20 flex items-center gap-2 transition-all">
            <span>+</span> New Order / Refill
          </button>
          <button onClick={toggleTheme} className={`p-2.5 rounded-xl border ${cardBg}`}>{isDark ? '☀️' : '🌙'}</button>
        </div>
      </header>

      {/* TABS NAV */}
      <div className={`border-b ${isDark ? 'border-slate-800 bg-slate-900/40' : 'border-slate-200 bg-slate-100'} px-4 lg:px-8`}>
        <nav className="flex space-x-2 overflow-x-auto py-2">
          {[
            { id: 'pos', label: 'POS & Counter', icon: '🛒' },
            { id: 'orders', label: 'Active Deliveries', icon: '🚚', badge: activeDeliveriesCount },
            { id: 'customers', label: 'Customer Ledger', icon: '👥' },
            { id: 'station', label: 'Station Monitor', icon: '🧪' },
            { id: 'financials', label: 'Sales & Expenses', icon: '📊' },
          ].map(tab => (
            <button key={tab.id} onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-semibold whitespace-nowrap transition-all ${
                activeTab === tab.id ? 'bg-cyan-500 text-white shadow-md shadow-cyan-500/20' : `${subText} hover:bg-slate-800/20`
              }`}>
              <span>{tab.icon}</span><span>{tab.label}</span>
              {tab.badge > 0 && <span className="px-1.5 py-0.5 rounded-full bg-amber-500 text-slate-950 font-black text-[10px]">{tab.badge}</span>}
            </button>
          ))}
        </nav>
      </div>

      {/* MAIN CONTENT — Tabs components continue below */}
      <main className="flex-1 p-4 lg:p-8 max-w-7xl w-full mx-auto space-y-6">
        {activeTab === 'pos' && (
          <PosCounterView {...{ isDark, cardBg, subText, orders, purifiedTankLiters, tdsLevel, phLevel, onOpenNewOrder: () => setShowNewOrderModal(true), onViewReceipt: o => setShowReceiptModal(o), onQuickStatusChange: handleStatusChange }} />
        )}
        {activeTab === 'orders' && (
          <OrdersDeliveryView {...{ isDark, cardBg, subText, orders, onStatusChange: handleStatusChange, onPaymentChange: handlePaymentChange, searchQuery: orderSearch, setSearchQuery: setOrderSearch, onViewReceipt: o => setShowReceiptModal(o) }} />
        )}
        {activeTab === 'customers' && (
          <CustomerLedgerView {...{ isDark, cardBg, subText, customers, searchQuery: customerSearch, setSearchQuery: setCustomerSearch, onOpenReturn: c => setShowReturnModal(c) }} />
        )}
        {activeTab === 'station' && (
          <StationMonitorView {...{ isDark, cardBg, subText, purifiedTankLiters, setPurifiedTankLiters, rawWaterMeter, purifiedWaterMeter, tdsLevel, phLevel, turbidity, filters, onOpenMeter: () => setShowMeterModal(true) }} />
        )}
        {activeTab === 'financials' && (
          <FinancialsView {...{ isDark, cardBg, subText, orders, expenses, totalSalesToday, totalUnpaid, onAddExpense: () => setShowExpenseModal(true) }} />
        )}
      </main>

      {/* MODALS — simplified versions included below */}
      {showNewOrderModal && <NewOrderModal {...{ isDark, cardBg, subText, customers, onClose: () => setShowNewOrderModal(false), onSubmit: handleNewOrder }} />}
      {showReceiptModal && <ReceiptModal {...{ isDark, cardBg, subText, order: showReceiptModal, onClose: () => setShowReceiptModal(null) }} />}
      {showReturnModal && <ContainerReturnModal {...{ isDark, cardBg, subText, customer: showReturnModal, onClose: () => setShowReturnModal(null), onConfirm: (s, r) => handleReturnConfirm(showReturnModal.id, s, r) }} />}
      {showExpenseModal && <ExpenseModal {...{ isDark, cardBg, subText, onClose: () => setShowExpenseModal(false), onSubmit: handleAddExpense }} />}
      {showMeterModal && <MeterReadingModal {...{ isDark, cardBg, subText, rawWaterMeter, purifiedWaterMeter, onClose: () => setShowMeterModal(false), onSubmit: handleMeterUpdate }} />}
    </div>
  );
}

// ==================== SUB-COMPONENTS (Simplified — full UI preserved) ====================
function PosCounterView({ isDark, cardBg, subText, orders, purifiedTankLiters, tdsLevel, phLevel, onOpenNewOrder, onViewReceipt, onQuickStatusChange }) {
  const recentOrders = orders.slice(0, 5);
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className={`p-5 rounded-2xl border ${cardBg}`}>
          <span className={`text-xs uppercase font-bold ${subText}`}>Tank Level</span>
          <div className="text-2xl font-black text-cyan-400 mt-1">{purifiedTankLiters} <span className="text-sm text-slate-400">L</span></div>
        </div>
        <div className={`p-5 rounded-2xl border ${cardBg}`}>
          <span className={`text-xs uppercase font-bold ${subText}`}>Water Quality</span>
          <div className="text-2xl font-black text-emerald-400 mt-1">{tdsLevel} <span className="text-sm text-slate-400">PPM</span></div>
          <div className="text-xs mt-1">pH: <b className="text-emerald-400">{phLevel}</b></div>
        </div>
        <div className={`p-5 rounded-2xl border ${cardBg}`}>
          <span className={`text-xs uppercase font-bold ${subText}`}>Orders Today</span>
          <div className="text-2xl font-black text-blue-400 mt-1">{orders.length}</div>
        </div>
        <div onClick={onOpenNewOrder} className="p-5 rounded-2xl border border-cyan-500/40 bg-cyan-600/20 cursor-pointer text-center">
          <div className="w-10 h-10 rounded-full bg-cyan-500 text-slate-950 font-black text-xl flex items-center justify-center mx-auto">+</div>
          <span className="text-xs font-bold mt-2 block text-cyan-300">New Order</span>
        </div>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className={`p-6 rounded-2xl border ${cardBg}`}>
          <h3 className="font-bold text-sm mb-3">Price List</h3>
          {[
            { name: '5-Gal Slim Refill', price: 35 },
            { name: '5-Gal Round Refill', price: 35 },
            { name: 'Alkaline 1L Bottle', price: 25 },
          ].map(p => (
            <div key={p.name} className="flex justify-between py-2 border-b border-slate-700/30">
              <span className="text-xs">{p.name}</span>
              <span className="font-bold text-cyan-400">₱{p.price}</span>
            </div>
          ))}
          <button onClick={onOpenNewOrder} className="w-full mt-4 py-2.5 rounded-xl bg-cyan-500 text-white font-bold text-xs">Open POS</button>
        </div>
        <div className={`lg:col-span-2 p-6 rounded-2xl border ${cardBg}`}>
          <h3 className="font-bold text-sm mb-4">Live Orders</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-xs">
              <thead><tr className={`border-b ${isDark ? 'border-slate-800' : 'border-slate-200'}`}>
                <th className="pb-2 text-left">ID</th><th className="pb-2 text-left">Customer</th><th className="pb-2 text-left">Amount</th><th className="pb-2 text-left">Status</th><th className="pb-2 text-left">Action</th>
              </tr></thead>
              <tbody>
                {recentOrders.map(o => (
                  <tr key={o.id} className="border-b border-slate-800/20">
                    <td className="py-2 font-mono text-cyan-400">{o.id}</td>
                    <td className="py-2">{o.customerName}</td>
                    <td className="py-2 font-bold">₱{o.totalAmount}</td>
                    <td className="py-2">
                      <select value={o.status} onChange={(e) => onQuickStatusChange(o.id, e.target.value)}
                        className="text-xs px-2 py-1 rounded bg-slate-800 text-white">
                        <option value="Pending">Pending</option>
                        <option value="Refill in Progress">Refill</option>
                        <option value="Out for Delivery">Out for Delivery</option>
                        <option value="Completed">Done</option>
                      </select>
                    </td>
                    <td className="py-2">
                      <button onClick={() => onViewReceipt(o)} className="px-2 py-1 rounded bg-slate-700 text-white text-xs">Receipt</button>
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

function OrdersDeliveryView({ isDark, cardBg, subText, orders, onStatusChange, onPaymentChange, searchQuery, setSearchQuery, onViewReceipt }) {
  const filtered = orders.filter(o => 
    o.customerName.toLowerCase().includes(searchQuery.toLowerCase()) ||
    o.id.toLowerCase().includes(searchQuery.toLowerCase())
  );
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center flex-wrap gap-4">
        <h2 className="text-lg font-bold">Active Orders & Deliveries</h2>
        <input type="text" placeholder="Search..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)}
          className={`px-4 py-2 rounded-xl text-xs border ${isDark ? 'bg-slate-900 border-slate-700' : 'bg-white border-slate-300'}`} />
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filtered.map(o => (
          <div key={o.id} className={`p-5 rounded-2xl border ${cardBg}`}>
            <div className="flex justify-between items-start mb-3">
              <span className="font-mono text-cyan-400 font-bold">{o.id}</span>
              <span className={`px-2 py-0.5 rounded-full text-xs ${o.orderType==='Delivery' ? 'bg-indigo-500/20 text-indigo-400' : 'bg-cyan-500/20 text-cyan-400'}`}>{o.orderType}</span>
            </div>
            <h3 className="font-bold text-sm">{o.customerName}</h3>
            <p className={`text-xs ${subText} mb-2`}>{o.address}</p>
            <div className="space-y-1 text-xs mb-3">
              <div className="flex justify-between"><span className={subText}>Items:</span><span>{o.items.map(i => `${i.qty}x ${i.name.split(' ')[0]}`).join(', ')}</span></div>
              <div className="flex justify-between"><span className={subText}>Total:</span><span className="font-bold text-cyan-400">₱{o.totalAmount}</span></div>
              <div className="flex justify-between items-center">
                <span className={subText}>Payment:</span>
                <button onClick={() => onPaymentChange(o.id, o.paymentStatus==='Paid'?'Unpaid':'Paid')}
                  className={`px-2 py-0.5 rounded text-xs font-bold ${o.paymentStatus==='Paid'?'bg-emerald-500/20 text-emerald-400':'bg-rose-500/20 text-rose-400'}`}>
                  {o.paymentStatus}
                </button>
              </div>
            </div>
            <select value={o.status} onChange={(e) => onStatusChange(o.id, e.target.value)}
              className="w-full px-2 py-1.5 rounded-lg text-xs bg-slate-800 text-white mb-2">
              <option value="Pending">Pending</option>
              <option value="Refill in Progress">Refill in Progress</option>
              <option value="Out for Delivery">Out for Delivery</option>
              <option value="Delivered">Delivered</option>
              <option value="Completed">Completed</option>
            </select>
            <button onClick={() => onViewReceipt(o)} className="w-full py-1.5 bg-slate-700 rounded-lg text-xs">View Receipt</button>
          </div>
        ))}
      </div>
    </div>
  );
}

function CustomerLedgerView({ isDark, cardBg, subText, customers, searchQuery, setSearchQuery, onOpenReturn }) {
  const filtered = customers.filter(c => 
    c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    c.phone.includes(searchQuery)
  );
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center flex-wrap gap-4">
        <h2 className="text-lg font-bold">Customer Ledger</h2>
        <input type="text" placeholder="Search customer..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)}
          className={`px-4 py-2 rounded-xl text-xs border ${isDark ? 'bg-slate-900 border-slate-700' : 'bg-white border-slate-300'}`} />
      </div>
      <div className={`p-6 rounded-2xl border ${cardBg} overflow-x-auto`}>
        <table className="w-full text-xs">
          <thead><tr className={`border-b ${isDark ? 'border-slate-800' : 'border-slate-200'}`}>
            <th className="pb-2 text-left">Name</th>
            <th className="pb-2 text-left">Contact</th>
            <th className="pb-2 text-left">Borrowed Slim</th>
            <th className="pb-2 text-left">Borrowed Round</th>
            <th className="pb-2 text-left">Balance</th>
            <th className="pb-2 text-left">Action</th>
          </tr></thead>
          <tbody>
            {filtered.map(c => (
              <tr key={c.id} className="border-b border-slate-800/20">
                <td className="py-2 font-bold text-cyan-400">{c.name}</td>
                <td className="py-2">{c.phone}</td>
                <td className="py-2">{c.borrowedSlim}</td>
                <td className="py-2">{c.borrowedRound}</td>
                <td className="py-2 font-bold">{c.balance > 0 ? <span className="text-rose-400">₱{c.balance}</span> : <span className="text-emerald-400">Cleared</span>}</td>
                <td className="py-2">
                  <button onClick={() => onOpenReturn(c)} className="px-3 py-1.5 bg-cyan-500 rounded-lg text-white text-xs font-bold">Record Return</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function StationMonitorView({ isDark, cardBg, subText, purifiedTankLiters, setPurifiedTankLiters, rawWaterMeter, purifiedWaterMeter, tdsLevel, phLevel, turbidity, filters, onOpenMeter }) {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className={`p-6 rounded-2xl border ${cardBg}`}>
          <h3 className="font-bold text-sm mb-4">Purified Water Tank</h3>
          <div className="h-48 bg-slate-800/40 rounded-xl relative flex flex-col justify-end mb-4">
            <div style={{ height: `${(purifiedTankLiters/5000)*100}%` }}
              className="bg-gradient-to-t from-blue-600 via-cyan-500 to-sky-400 w-full flex items-center justify-center">
              <span className="font-black text-white text-xl">{Math.round((purifiedTankLiters/5000)*100)}%</span>
            </div>
          </div>
          <p className="text-xs text-center">Current: <b className="text-cyan-400">{purifiedTankLiters}L</b> / 5,000L</p>
          <button onClick={() => setPurifiedTankLiters(5000)} className="w-full mt-3 py-2 rounded-xl bg-slate-800 text-cyan-400 text-xs">Refill Tank</button>
        </div>
        <div className={`p-6 rounded-2xl border ${cardBg}`}>
          <h3 className="font-bold text-sm mb-4">Water Quality</h3>
          {[
            { label: 'TDS', value: `${tdsLevel} PPM`, color: 'text-emerald-400' },
            { label: 'pH Level', value: phLevel, color: 'text-cyan-400' },
            { label: 'Turbidity', value: `${turbidity} NTU`, color: 'text-blue-400' },
          ].map(m => (
            <div key={m.label} className="flex justify-between py-2 border-b border-slate-700/30">
              <span className={`text-xs ${subText}`}>{m.label}</span>
              <span className={`font-bold ${m.color}`}>{m.value}</span>
            </div>
          ))}
        </div>
        <div className={`p-6 rounded-2xl border ${cardBg}`}>
          <h3 className="font-bold text-sm mb-4">Meter Readings</h3>
          <div className="space-y-3 text-xs">
            <div className="flex justify-between p-2 bg-slate-800/30 rounded"><span className={subText}>Raw Water:</span><span className="font-mono">{rawWaterMeter}</span></div>
            <div className="flex justify-between p-2 bg-slate-800/30 rounded"><span className={subText}>Purified:</span><span className="font-mono text-cyan-400">{purifiedWaterMeter}</span></div>
          </div>
          <button onClick={onOpenMeter} className="w-full mt-4 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 text-white text-xs font-bold">Update Readings</button>
        </div>
      </div>
      <div className={`p-6 rounded-2xl border ${cardBg}`}>
        <h3 className="font-bold text-sm mb-4">Filter Health</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filters.map(f => (
            <div key={f.id} className="p-3 bg-slate-800/30 rounded-xl">
              <div className="flex justify-between text-xs mb-2">
                <span className="font-bold">{f.name}</span>
                <span className={`font-bold ${f.health > 60 ? 'text-emerald-400' : f.health > 40 ? 'text-amber-400' : 'text-rose-400'}`}>{f.health}%</span>
              </div>
              <div className="w-full h-2 bg-slate-700 rounded-full overflow-hidden">
                <div style={{ width: `${f.health}%` }}
                  className={`h-full ${f.health > 60 ? 'bg-emerald-500' : f.health > 40 ? 'bg-amber-500' : 'bg-rose-500'}`} />
              </div>
              <p className={`text-xs mt-2 ${subText}`}>Next change: {f.nextChange}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function FinancialsView({ isDark, cardBg, subText, orders, expenses, totalSalesToday, totalUnpaid, onAddExpense }) {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className={`p-5 rounded-2xl border ${cardBg}`}>
          <span className={`text-xs uppercase font-bold ${subText}`}>Total Sales Today</span>
          <div className="text-2xl font-black text-emerald-400 mt-1">₱{totalSalesToday.toLocaleString()}</div>
        </div>
        <div className={`p-5 rounded-2xl border ${cardBg}`}>
          <span className={`text-xs uppercase font-bold ${subText}`}>Unpaid Balance</span>
          <div className="text-2xl font-black text-amber-400 mt-1">₱{totalUnpaid.toLocaleString()}</div>
        </div>
        <div className={`p-5 rounded-2xl border ${cardBg}`}>
          <span className={`text-xs uppercase font-bold ${subText}`}>Net Position</span>
          <div className="text-2xl font-black text-cyan-400 mt-1">₱{(totalSalesToday - totalUnpaid).toLocaleString()}</div>
        </div>
      </div>
      <div className="flex justify-between items-center">
        <h2 className="text-lg font-bold">Expense Log</h2>
        <button onClick={onAddExpense} className="px-4 py-2 rounded-xl bg-cyan-500 text-white text-xs font-bold">+ Add Expense</button>
      </div>
      <div className={`p-6 rounded-2xl border ${cardBg}`}>
        <table className="w-full text-xs">
          <thead><tr className={`border-b ${isDark ? 'border-slate-800' : 'border-slate-200'}`}>
            <th className="pb-2 text-left">Date</th>
            <th className="pb-2 text-left">Category</th>
            <th className="pb-2 text-left">Amount</th>
            <th className="pb-2 text-left">Note</th>
          </tr></thead>
          <tbody>
            {expenses.map(e => (
              <tr key={e.id} className="border-b border-slate-800/20">
                <td className="py-2">{e.date}</td>
                <td className="py-2 font-bold">{e.category}</td>
                <td className="py-2 font-bold text-rose-400">₱{e.amount}</td>
                <td className="py-2">{e.note}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// ==================== MODAL COMPONENTS ====================
function NewOrderModal({ isDark, cardBg, subText, customers, onClose, onSubmit }) {
  const [form, setForm] = useState({
    customerId: '', customerName: '', phone: '', address: '', orderType: 'Walk-in',
    items: [{ name: '5-Gal Slim Container Refill', qty: 1, price: 35 }],
    totalAmount: 35, paymentMethod: 'Cash', paymentStatus: 'Paid', status: 'Pending',
    rider: 'Counter Direct', borrowedSlimQty: 0, borrowedRoundQty: 0
  });

  const updateItem = (idx, field, val) => {
    const items = [...form.items];
    items[idx][field] = val;
    const total = items.reduce((s, i) => s + i.qty * i.price, 0);
    setForm({ ...form, items, totalAmount: total });
  };

  const addItem = () => setForm({ ...form, items: [...form.items, { name: '', qty: 1, price: 0 }] });

  const handleSelectCustomer = (cust) => {
    setForm({
      ...form,
      customerId: cust.id,
      customerName: cust.name,
      phone: cust.phone,
      address: cust.address
    });
  };

  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
      <div className={`w-full max-w-lg max-h-[90vh] overflow-y-auto rounded-2xl p-6 border ${cardBg}`}>
        <h2 className="text-lg font-bold mb-4">Create New Order</h2>
        <div className="space-y-3 text-xs">
          <select value={form.customerId} onChange={(e) => {
            const c = customers.find(x => x.id === e.target.value);
            c ? handleSelectCustomer(c) : setForm({ ...form, customerId: '', customerName: e.target.value });
          }} className="w-full px-3 py-2 rounded-lg bg-slate-800 text-white">
            <option value="">-- Select or type customer name --</option>
            {customers.map(c => <option key={c.id} value={c.id}>{c.name} — {c.phone}</option>)}
          </select>
          <input placeholder="Customer Name" value={form.customerName} onChange={(e) => setForm({...form, customerName: e.target.value})}
            className="w-full px-3 py-2 rounded-lg bg-slate-800 text-white" />
          <input placeholder="Phone" value={form.phone} onChange={(e) => setForm({...form, phone: e.target.value})}
            className="w-full px-3 py-2 rounded-lg bg-slate-800 text-white" />
          <input placeholder="Address" value={form.address} onChange={(e) => setForm({...form, address: e.target.value})}
            className="w-full px-3 py-2 rounded-lg bg-slate-800 text-white" />
          <div className="flex gap-2">
            {['Walk-in', 'Delivery'].map(t => (
              <label key={t} className="flex-1 text-center py-2 rounded-lg border cursor-pointer">
                <input type="radio" name="orderType" value={t} checked={form.orderType === t}
                  onChange={(e) => setForm({...form, orderType: e.target.value})} className="hidden" />
                <span className={form.orderType === t ? 'text-cyan-400 font-bold' : ''}>{t}</span>
              </label>
            ))}
          </div>
          <div className="border-t pt-3">
            <label className="font-bold">Items</label>
            {form.items.map((item, idx) => (
              <div key={idx} className="flex gap-2 mt-2">
                <select value={item.name} onChange={(e) => updateItem(idx, 'name', e.target.value)}
                  className="flex-1 px-2 py-2 rounded-lg bg-slate-800 text-white text-xs">
                  <option value="">Select Item</option>
                  <option value="5-Gal Slim Container Refill">5-Gal Slim Refill — ₱35</option>
                  <option value="5-Gal Round Container Refill">5-Gal Round Refill — ₱35</option>
                  <option value="Alkaline Water Bottle 1L">Alkaline 1L — ₱25</option>
                </select>
                <input type="number" value={item.qty} min="1" onChange={(e) => updateItem(idx, 'qty', parseInt(e.target.value)||0)}
                  className="w-16 px-2 py-2 rounded-lg bg-slate-800 text-white text-center" />
              </div>
            ))}
            <button onClick={addItem} className="mt-2 text-cyan-400 text-xs">+ Add Another Item</button>
          </div>
          <div className="flex justify-between text-sm font-bold pt-2 border-t">
            <span>Total:</span>
            <span className="text-cyan-400">₱{form.totalAmount}</span>
          </div>
          <div className="flex gap-2">
            {['Cash', 'GCash', 'Pay Later'].map(m => (
              <button key={m} onClick={() => setForm({...form, paymentMethod: m, paymentStatus: m==='Pay Later'?'Unpaid':'Paid'})}
                className={`flex-1 py-2 rounded-lg ${form.paymentMethod === m ? 'bg-cyan-500 text-white' : 'bg-slate-800'}`}>
                {m}
              </button>
            ))}
          </div>
          {form.orderType === 'Delivery' && (
            <div className="space-y-2">
              <input placeholder="Rider Name" value={form.rider} onChange={(e) => setForm({...form, rider: e.target.value})}
                className="w-full px-3 py-2 rounded-lg bg-slate-800 text-white" />
              <div className="flex gap-2">
                <label className="flex-1">Borrowed Slim: <input type="number" value={form.borrowedSlimQty} min="0"
                  onChange={(e) => setForm({...form, borrowedSlimQty: parseInt(e.target.value)||0})}
                  className="w-full px-2 py-1 rounded bg-slate-800 text-white" /></label>
              </div>
            </div>
                  </div>
          )}
          <div className="flex gap-3 mt-4 pt-3 border-t">
            <button onClick={onClose} className="flex-1 py-2.5 rounded-lg bg-slate-700 text-white font-bold">Cancel</button>
            <button onClick={() => onSubmit({
              ...form,
              id: `ORD-${Date.now().toString().slice(-4)}`,
              timestamp: new Date().toLocaleTimeString('en-PH', { hour: 'numeric', minute: '2-digit', hour12: true })
            })} className="flex-1 py-2.5 rounded-lg bg-cyan-500 text-white font-bold">
              Create Order
            </button>
          </div>
        </div>
      </div>
    );
  }

  function ReceiptModal({ isDark, cardBg, subText, order, onClose }) {
    return (
      <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
        <div className={`w-full max-w-md rounded-2xl p-6 border ${cardBg}`}>
          <div className="text-center mb-4">
            <h2 className="text-lg font-black">AQUAFLOW WATER REFILLING</h2>
            <p className={`text-xs ${subText}`}>Poblacion, Maramag • 0917-XXX-XXXX</p>
            <p className="font-mono text-sm mt-2">{order.id}</p>
            <p className={`text-xs ${subText}`}>{new Date().toLocaleString('en-PH')}</p>
          </div>
          <div className="border-y border-dashed py-3 my-3 text-xs space-y-1">
            <p><b>Customer:</b> {order.customerName}</p>
            <p><b>Items:</b></p>
            {order.items.map((item, i) => (
              <p key={i} className="flex justify-between">
                <span>{item.qty}× {item.name}</span>
                <span>₱{item.price * item.qty}</span>
              </p>
            ))}
            <p className="flex justify-between font-bold text-base pt-2">
              <span>TOTAL</span>
              <span>₱{order.totalAmount}</span>
            </p>
            <p><b>Payment:</b> {order.paymentMethod} — {order.paymentStatus}</p>
          </div>
          <p className="text-center text-xs text-slate-400">Thank you! Drink Clean 💧</p>
          <button onClick={onClose} className="w-full mt-4 py-2.5 rounded-lg bg-cyan-500 text-white font-bold">Close</button>
        </div>
      </div>
    );
  }

  function ContainerReturnModal({ isDark, cardBg, subText, customer, onClose, onConfirm }) {
    const [slim, setSlim] = useState(0);
    const [round, setRound] = useState(0);
    return (
      <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
        <div className={`w-full max-w-sm rounded-2xl p-6 border ${cardBg}`}>
          <h2 className="text-lg font-bold mb-4">Record Container Return</h2>
          <p className="text-sm mb-4">{customer.name}</p>
          <div className="space-y-3 text-xs">
            <div>
              <label>Slim Containers Returning</label>
              <input type="number" value={slim} min="0" onChange={(e) => setSlim(parseInt(e.target.value)||0)}
                className="w-full px-3 py-2 rounded-lg bg-slate-800 text-white" />
            </div>
            <div>
              <label>Round Containers Returning</label>
              <input type="number" value={round} min="0" onChange={(e) => setRound(parseInt(e.target.value)||0)}
                className="w-full px-3 py-2 rounded-lg bg-slate-800 text-white" />
            </div>
            <p className={subText}>Current borrowed: {customer.borrowedSlim} Slim • {customer.borrowedRound} Round</p>
          </div>
          <div className="flex gap-3 mt-4">
            <button onClick={onClose} className="flex-1 py-2.5 rounded-lg bg-slate-700 text-white font-bold">Cancel</button>
            <button onClick={() => onConfirm(slim, round)} className="flex-1 py-2.5 rounded-lg bg-cyan-500 text-white font-bold">Confirm Return</button>
          </div>
        </div>
      </div>
    );
  }

  function ExpenseModal({ isDark, cardBg, subText, onClose, onSubmit }) {
    const [form, setForm] = useState({ category: '', amount: '', note: '', date: new Date().toISOString().split('T')[0] });
    return (
      <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
        <div className={`w-full max-w-sm rounded-2xl p-6 border ${cardBg}`}>
          <h2 className="text-lg font-bold mb-4">Add Expense</h2>
          <div className="space-y-3 text-xs">
            <select value={form.category} onChange={(e) => setForm({...form, category: e.target.value})}
              className="w-full px-3 py-2 rounded-lg bg-slate-800 text-white">
              <option value="">Select Category</option>
              <option value="Electricity">Electricity</option>
              <option value="Water">Water</option>
              <option value="Gasoline">Gasoline</option>
              <option value="Filter Replacement">Filter Replacement</option>
              <option value="Staff Payroll">Staff Payroll</option>
              <option value="Supplies">Supplies</option>
              <option value="Other">Other</option>
            </select>
            <input type="number" placeholder="Amount" value={form.amount} onChange={(e) => setForm({...form, amount: parseFloat(e.target.value)||0})}
              className="w-full px-3 py-2 rounded-lg bg-slate-800 text-white" />
            <input placeholder="Note / Description" value={form.note} onChange={(e) => setForm({...form, note: e.target.value})}
              className="w-full px-3 py-2 rounded-lg bg-slate-800 text-white" />
            <input type="date" value={form.date} onChange={(e) => setForm({...form, date: e.target.value})}
              className="w-full px-3 py-2 rounded-lg bg-slate-800 text-white" />
          </div>
          <div className="flex gap-3 mt-4">
            <button onClick={onClose} className="flex-1 py-2.5 rounded-lg bg-slate-700 text-white font-bold">Cancel</button>
            <button onClick={() => onSubmit(form)} className="flex-1 py-2.5 rounded-lg bg-cyan-500 text-white font-bold">Save</button>
          </div>
        </div>
      </div>
    );
  }

  function MeterReadingModal({ isDark, cardBg, subText, rawWaterMeter, purifiedWaterMeter, onClose, onSubmit }) {
    const [raw, setRaw] = useState(rawWaterMeter);
    const [purified, setPurified] = useState(purifiedWaterMeter);
    return (
      <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
        <div className={`w-full max-w-sm rounded-2xl p-6 border ${cardBg}`}>
          <h2 className="text-lg font-bold mb-4">Update Meter Readings</h2>
          <div className="space-y-4 text-xs">
            <div>
              <label>Raw Water Meter (m³)</label>
              <input type="number" value={raw} onChange={(e) => setRaw(parseFloat(e.target.value)||0)}
                className="w-full px-3 py-2 rounded-lg bg-slate-800 text-white font-mono" />
            </div>
            <div>
              <label>Purified Water Meter (m³)</label>
              <input type="number" value={purified} onChange={(e) => setPurified(parseFloat(e.target.value)||0)}
                className="w-full px-3 py-2 rounded-lg bg-slate-800 text-white font-mono" />
            </div>
            <p className={subText}>Daily consumption will be calculated automatically</p>
          </div>
          <div className="flex gap-3 mt-4">
            <button onClick={onClose} className="flex-1 py-2.5 rounded-lg bg-slate-700 text-white font-bold">Cancel</button>
            <button onClick={() => onSubmit(raw, purified)} className="flex-1 py-2.5 rounded-lg bg-cyan-500 text-white font-bold">Update</button>
          </div>
        </div>
      </div>
    );
  }
  );
}
