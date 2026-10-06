// 1. Add useEffect to your import
import { useState, useEffect } from 'react';

// 2. Inside your component:
export default function CustomerList() {
  // ✅ DELETE your mock data line, replace with:
  const [customers, setCustomers] = useState([]);

  // ✅ PASTE the fetch code here
  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch('/api/water-refilling/customers');
        const data = await res.json();
        setCustomers(data);
      } catch (err) {
        console.error('Fetch error:', err);
      }
    };
    fetchData();
  }, []);

  // Your existing return/JSX stays exactly the same
  return ( /* ... */ );
}