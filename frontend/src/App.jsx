import { useState } from 'react'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')

  return (
    <div className="app">
      <header className="navbar">
        <h1>💧 AquaFlow</h1>
        <nav>
          {['dashboard', 'orders', 'inventory', 'users'].map(tab => (
            <button
              key={tab}
              className={activeTab === tab ? 'active' : ''}
              onClick={() => setActiveTab(tab)}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </nav>
      </header>

      <main className="content">
        {activeTab === 'dashboard' && (
          <div className="dashboard">
            <h2>Dashboard Overview</h2>
            <div className="stats-grid">
              <div className="stat-card">
                <h3>Today's Orders</h3>
                <p className="value">24</p>
              </div>
              <div className="stat-card">
                <h3>Active Refill Stations</h3>
                <p className="value">8</p>
              </div>
              <div className="stat-card">
                <h3>Water Stock (Liters)</h3>
                <p className="value">4,250</p>
              </div>
              <div className="stat-card">
                <h3>Monthly Revenue</h3>
                <p className="value">₱ 28,450</p>
              </div>
            </div>
          </div>
        )}
        <p>Selected: {activeTab}</p>
      </main>
    </div>
  )
}

export default App
