import { useState } from 'react'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center p-8">
      <h1 className="text-4xl font-bold text-cyan-400 mb-8">AquaFlow — Water Station Dashboard</h1>
      
      <div className="bg-gray-800 rounded-xl p-8 shadow-2xl border border-cyan-500/20">
        <p className="text-xl mb-4">Daily Sales: ₱12,450.00</p>
        <p className="text-lg text-gray-300 mb-6">Active Orders: 24</p>
        
        <button 
          onClick={() => setCount(count + 1)}
          className="bg-cyan-600 hover:bg-cyan-500 px-6 py-3 rounded-lg font-semibold transition-colors"
        >
          Orders Today: {count}
        </button>
      </div>
    </div>
  )
}

export default App