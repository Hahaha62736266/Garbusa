import { X, Printer } from 'lucide-react';
import type { Order, Customer, Product } from '../types/waterRefilling';

interface Props {
  open: boolean;
  onClose: () => void;
  order: Order | null;
  customers: Customer[];
  products: Product[];
}

export function ReceiptModal({ open, onClose, order, customers, products }: Props) {
  if (!open || !order) return null;

  const customer = customers.find(c => c.id === order.customerId);
  const product = products.find(p => p.id === order.productId);

  const handlePrint = () => window.print();

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-black/40" onClick={onClose} />
      <div className="relative w-full max-w-sm bg-white text-black rounded-xl border border-slate-200 p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">Receipt</h3>
          <button onClick={onClose} className="p-1 rounded hover:bg-slate-100">
            <X size={18} />
          </button>
        </div>

        <div className="border-b border-dashed border-slate-300 pb-4 mb-4 text-center">
          <h4 className="font-bold text-lg">AquaFlow Tracker</h4>
          <p className="text-sm text-slate-500">Water Refilling Station</p>
          <p className="text-xs text-slate-400 mt-1">Cagayan de Oro, PH</p>
        </div>

        <div className="space-y-2 text-sm">
          <div className="flex justify-between">
            <span className="text-slate-500">Order ID</span>
            <span className="font-mono font-medium">{order.id}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-500">Date</span>
            <span>{order.orderDate}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-500">Customer</span>
            <span className="font-medium">{customer?.fullName || order.customerId}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-500">Product</span>
            <span>{product?.name || order.productId}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-500">Quantity</span>
            <span>×{order.quantity}</span>
          </div>
          <div className="flex justify-between pt-2 border-t border-slate-200 font-bold text-lg">
            <span>Total</span>
            <span>₱{order.totalAmount.toFixed(2)}</span>
          </div>
          <div className="flex justify-between text-xs text-slate-500 pt-1">
            <span>Status</span>
            <span>{order.status} · {order.paymentStatus}</span>
          </div>
        </div>

        <div className="mt-5 pt-4 border-t border-dashed border-slate-300 text-center text-xs text-slate-400">
          Thank you for your business! 💧
        </div>

        <button
          onClick={handlePrint}
          className="w-full mt-4 flex items-center justify-center gap-2 bg-sky-600 hover:bg-sky-500 text-white py-2 rounded-lg text-sm font-medium"
        >
          <Printer size={16} /> Print Receipt
        </button>
      </div>
    </div>
  );
}
