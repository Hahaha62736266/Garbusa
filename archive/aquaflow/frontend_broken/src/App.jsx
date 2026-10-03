import { useEffect, useState } from "react";
import { aquaApi } from "./api/aquaApi";

function App() {
  const [connected, setConnected] = useState(false);
  const [stations, setStations] = useState([]);
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  
  const [form, setForm] = useState({
    station_id: "",
    volume_liters: "",
    customer_name: "",
    amount_paid: "",
    payment_method: "cash"
  });

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    try {
      await aquaApi.getHealth().then(() => setConnected(true));
      const [stationsData, recordsData] = await Promise.all([
        aquaApi.getStations(),
        aquaApi.getRecords()
      ]);
      setStations(stationsData);
      setRecords(recordsData);
    } catch (err) {
      console.error("Load failed:", err);
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      await aquaApi.addRecord({
        ...form,
        volume_liters: parseFloat(form.volume_liters),
        amount_paid: parseFloat(form.amount_paid)
      });
      setForm({ station_id: "", volume_liters: "", customer_name: "", amount_paid: "", payment_method: "cash" });
      await loadData();
    } catch (err) {
      alert("Failed to add record!");
    }
  }

  async function handleDelete(id) {
    if (!confirm("Delete this record?")) return;
    await aquaApi.deleteRecord(id);
    await loadData();
  }

  if (loading) return <div className="loading">Loading AquaFlow...</div>;

  return (
    <div className="app">
      <header>
        <h1>💧 AquaFlow — Water Refilling Management</h1>
        <span className={`status ${connected ? "ok" : "err"}`}>
          {connected ? "● Connected" : "○ Disconnected"}
        </span>
      </header>

      <main>
        <section className="form-card">
          <h2>New Refill Record</h2>
          <form onSubmit={handleSubmit}>
            <select
              value={form.station_id}
              onChange={(e) => setForm({...form, station_id: e.target.value})}
              required
            >
              <option value="">Select Station</option>
              {stations.map(s => (
                <option key={s.id} value={s.id}>{s.name} — {s.location}</option>
              ))}
            </select>

            <input
              type="number" step="0.1" placeholder="Volume (Liters)"
              value={form.volume_liters}
              onChange={(e) => setForm({...form, volume_liters: e.target.value})}
              required
            />
            <input
              type="text" placeholder="Customer Name"
              value={form.customer_name}
              onChange={(e) => setForm({...form, customer_name: e.target.value})}
            />
            <input
              type="number" step="0.01" placeholder="Amount Paid (₱)"
              value={form.amount_paid}
              onChange={(e) => setForm({...form, amount_paid: e.target.value})}
              required
            />
            <select
              value={form.payment_method}
              onChange={(e) => setForm({...form, payment_method: e.target.value})}
            >
              <option value="cash">Cash</option>
              <option value="gcash">GCash</option>
              <option value="transfer">Bank Transfer</option>
            </select>

            <button type="submit">Add Record</button>
          </form>
        </section>

        <section className="records-card">
          <h2>Refilling Records ({records.length})</h2>
          <table>
            <thead>
              <tr>
                <th>Station</th>
                <th>Volume (L)</th>
                <th>Customer</th>
                <th>Amount</th>
                <th>Method</th>
                <th>Date/Time</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {records.map(r => (
                <tr key={r.id}>
                  <td>{r.station_name}</td>
                  <td>{r.volume_liters}</td>
                  <td>{r.customer_name || "—"}</td>
                  <td>₱{r.amount_paid}</td>
                  <td>{r.payment_method}</td>
                  <td>{new Date(r.recorded_at).toLocaleString()}</td>
                  <td>
                    <button className="del-btn" onClick={() => handleDelete(r.id)}>Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      </main>
    </div>
  );
}

export default App;
