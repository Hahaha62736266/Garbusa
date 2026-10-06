// src/water-refilling/data/mockWaterData.ts
import type { Customer, Product, Order, Collection, Expense, MeterReading, DailySummary } from '../types/waterRefilling';

export const initialCustomers: Customer[] = [
  { id: 'C001', fullName: 'Maria Santos', contactNumber: '0917-123-4567', address: 'Brgy. 25, Cagayan de Oro', containerOwned: 2, containerBalance: 2, registrationDate: '2026-01-10' },
  { id: 'C002', fullName: 'Juan Dela Cruz', contactNumber: '0918-987-6543', address: 'Brgy. Lapasan, Cagayan de Oro', containerOwned: 3, containerBalance: 3, registrationDate: '2026-02-15' },
  { id: 'C003', fullName: 'Ana Reyes', contactNumber: '0915-111-2222', address: 'Brgy. Nazareth, Cagayan de Oro', containerOwned: 1, containerBalance: 1, registrationDate: '2026-03-20' },
];

export const initialProducts: Product[] = [
  { id: 'P001', name: '5-Gal Purified', pricePerUnit: 35.00, description: 'Refill only', stockAvailable: 120 },
  { id: 'P002', name: '5-Gal Distilled', pricePerUnit: 45.00, description: 'Best for drinking', stockAvailable: 85 },
  { id: 'P003', name: 'New 5-Gal Jug', pricePerUnit: 180.00, description: 'Empty plastic jug', stockAvailable: 40 },
];

export const initialOrders: Order[] = [
  { id: 'O001', customerId: 'C001', productId: 'P002', quantity: 2, totalAmount: 90.00, orderDate: '2026-10-06', status: 'Delivered', paymentStatus: 'Paid' },
  { id: 'O002', customerId: 'C002', productId: 'P001', quantity: 3, totalAmount: 105.00, orderDate: '2026-10-06', status: 'Pending', paymentStatus: 'Unpaid' },
];

export const initialCollections: Collection[] = [
  { id: 'CL001', customerId: 'C001', orderId: 'O001', emptyJugsReturned: 2, filledJugsReleased: 2, containerBalance: 2, collectionDate: '2026-10-06', collectedBy: 'Staff A' },
  { id: 'CL002', customerId: 'C002', orderId: 'O002', emptyJugsReturned: 0, filledJugsReleased: 0, containerBalance: 3, collectionDate: '2026-10-06', collectedBy: 'Staff B' },
];

export const initialExpenses: Expense[] = [
  { id: 'E001', date: '2026-10-06', category: 'Electricity', description: 'Daily power cost', amount: 250.00 },
  { id: 'E002', date: '2026-10-06', category: 'Supplies', description: 'Water test kit reagents', amount: 85.00 },
];

export const initialMeterReadings: MeterReading[] = [
  { id: 'M001', date: '2026-10-01', previousReading: 1250, currentReading: 1285, cubicMetersUsed: 35, costPerCubicMeter: 12.50, totalCost: 437.50 },
];

export const initialDailySummary: DailySummary = {
  date: new Date().toISOString().split('T')[0],
  totalSales: 195.00,
  totalCollections: 90.00,
  totalExpenses: 335.00,
  netIncome: -140.00,
  ordersCount: 2,
  containersOut: 5,
};
