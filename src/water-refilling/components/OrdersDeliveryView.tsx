import { Truck, CheckCircle, FileText, Clock, XCircle } from 'lucide-react';
import type { Order, Customer, Product } from '../types/waterRefilling';

interface Props {
  orders: Order[];
  customers: Customer[];
  products: Product[];
  onMarkDelivered: (orderId: string) => void;
  onPrintReceipt: (order: Order) => void;
  theme: 'light' | 'dark';
}

export function OrdersDeliveryView({ orders, customers, products, onMarkDelivered, onPrintReceipt, theme }: Props) {
  const getCustomer = (id: string) => customers.find(c => c.id === id);
  const getProduct = (id: string) => products.find(p => p.id === id);

  const statusConfig = {
    Pending: { icon: <Clock size={14} />, color: 'text-amber-500 bg-amber-500/10' },
    Delivered: { icon: <CheckCircle size={14} />, color: 'text-emerald-500 bg-emerald-500/10' },
    Cancelled: { icon: <XCircle size={14} />, color: 'text-red-500 bg-red-500/10' },
  };

  const cardClass = theme === 'dark' ? 'bg-gray-900 border-gray-800' : 'bg-white border-slate-200';

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <Truck className="text-sky-500" size={24} />
        <h2 className="text-xl font-semibold">Orders & Delivery Queue</h2>
      </div>

      {orders.length === 0 ? (
        <p className="text-slate-500 italic">No orders yet.</p>
      ) : (
        <div className="space-y-3">
          {orders.map(order => {
            const cust = getCustomer(order.customerId);
            const prod = getProduct(order.productId);
            const status = statusConfig[order.status];

            return (
              <div key={order.id} className={`p-4 rounded-xl border ${cardClass}`}>
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                  <div>
                    <div className="font-semibold">{order.id}</div>
                    <div className="text-sm space-y-0.5 mt-1">
                      <p><span className="font-medium">Customer:</span> {cust?.fullName || order.customerId}</p>
                      <p><span className="font-medium">Product:</span> {prod?.name || order.productId} × {order.quantity}</p>
                      <p><span className="font-medium">Date:</span> {order.orderDate}</p>
                      <p><span className="font-medium">Payment:</span> {order.paymentStatus}</p>
                    </div>
                  </div>

                  <div className="flex flex-col items-end gap-2">
                    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${status.color}`}>
                      {status.icon} {order.status}
                    </span>
                    <p className="font-bold text-lg">₱{order.totalAmount.toFixed(2)}</p>

                    <div className="flex gap-2 mt-1">
                      {order.status === 'Pending' && (
                        <button
                          onClick={() => onMarkDelivered(order.id)}
                          className="px-3 py-1.5 text-sm bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg transition-colors flex items-center gap-1.5"
                        >
                          <CheckCircle size={14} /> Mark Delivered
                        </button>
                      )}
                      <button
                        onClick={() => onPrintReceipt(order)}
                        className={`px-3 py-1.5 text-sm rounded-lg transition-colors flex items-center gap-1.5 ${
                          theme === 'dark' ? 'bg-gray-800 hover:bg-gray-700' : 'bg-slate-100 hover:bg-slate-200'
                        }`}
                      >
                        <FileText size={14} /> Receipt
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
