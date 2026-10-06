import { useState } from 'react';
import { X } from 'lucide-react';
import type { MeterReading } from '../types/waterRefilling';

interface Props {
  open: boolean;
  onClose: () => void;
  onSubmit: (reading: Omit<MeterReading, 'id'>) => void;
  theme: 'light' | 'dark';
}

export function MeterReadingModal({ open, onClose, onSubmit, theme }: Props) {
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
 
