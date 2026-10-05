import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { ToastProvider } from './components/Toast'; // add this line

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ToastProvider> {/* wrap everything */}
      <App />
    </ToastProvider>
  </React.StrictMode>
);
