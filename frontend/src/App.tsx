// src/App.tsx

import React from 'react';
import { ReactNotifications } from 'react-notifications-component';
import Dashboard from './components/Dashboard';
import 'react-notifications-component/dist/theme.css';

function App() {
  return (
    <>
      <ReactNotifications />
      <Dashboard />
    </>
  );
}

export default App;