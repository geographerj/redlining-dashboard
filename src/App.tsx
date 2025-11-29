import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { LenderProvider } from './context/LenderContext';
import { LenderSelection } from './components/LenderSelection';
import { StateView } from './components/StateView';
import { CBSAView } from './components/CBSAView';
import { CountyView } from './components/CountyView';
import { LendingRecord } from './utils/dataProcessor';
import './App.css';

// Data loading hook
function useData() {
  const [data, setData] = useState<LendingRecord[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const response = await fetch('/data/all-bank-data.json');
        const jsonData = await response.json();
        setData(jsonData);
      } catch (error) {
        console.error('Error loading data:', error);
        // Fallback: try to load individual files
        try {
          const frostResponse = await fetch('/data/frost-bank-data.json');
          const websterResponse = await fetch('/data/webster-bank-data.json');
          const frostData = await frostResponse.json();
          const websterData = await websterResponse.json();
          setData([...frostData, ...websterData]);
        } catch (fallbackError) {
          console.error('Error loading fallback data:', fallbackError);
        }
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  return { data, loading };
}

function AppContent() {
  const { data, loading } = useData();

  if (loading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh',
        fontSize: '1.2rem',
        color: '#818390'
      }}>
        Loading data...
      </div>
    );
  }

  return (
    <Routes>
      <Route path="/" element={<LenderSelection />} />
      <Route 
        path="/state/:lender?" 
        element={<StateView data={data} />} 
      />
      <Route 
        path="/cbsa/:lender/:state" 
        element={<CBSAView data={data} />} 
      />
      <Route 
        path="/county/:lender/:state/:cbsa" 
        element={<CountyView data={data} />} 
      />
      <Route 
        path="/compare/both" 
        element={<StateView data={data} />} 
      />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

function App() {
  return (
    <LenderProvider>
      <BrowserRouter basename={process.env.PUBLIC_URL}>
        <div className="App" style={{ minHeight: '100vh', backgroundColor: '#F9FAFB' }}>
          <AppContent />
        </div>
      </BrowserRouter>
    </LenderProvider>
  );
}

export default App;

