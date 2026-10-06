// src/water-refilling/types/waterRefilling.ts

export interface Customer {
  id: string;
  fullName: string;
  contactNumber: string;
  address: string;
  containerOwned: number;
  containerBalance: number;
  registrationDate: string;
}

export interface Product {
  id: string;
  name: string;
  pricePerUnit: number;
  description: string;
  stockAvailable: number;
}

export interface Order {
  id: string;
  customerId: string;
  productId: string;
  quantity: number;
  totalAmount: number;
  orderDate: string;
  status: 'Pending' | 'Delivered' | 'Cancelled';
  paymentStatus: 'Unpaid' | 'Paid' | 'Partial';
}

export interface Collection {
  id: string;
  customerId: string;
  orderId?: string;
  emptyJugsReturned: number;
  filledJugsReleased: number;
  containerBalance: number;
  collectionDate: string;
  collectedBy: string;
}

export interface Expense {
  id: string;
  date: string;
  category: string;
  description: string;
  amount: number;
}

export interface MeterReading {
  id: string;
  date: string;
  previousReading: number;
  currentReading: number;
  cubicMetersUsed: number;
  costPerCubicMeter: number;
  totalCost: number;
}

export interface DailySummary {
  date: string;
  totalSales: number;
  totalCollections: number;
  totalExpenses: number;
  netIncome: number;
  ordersCount: number;
  containersOut: number;
}

export type TabView = 'pos' | 'orders' | 'customers' | 'monitor' | 'financials';

export interface FilterItem {
  key: string;
  label: string;
  value: string;
}
