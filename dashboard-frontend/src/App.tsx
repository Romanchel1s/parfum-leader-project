import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import 'normalize.css';
import EmployeeManagerPage from './pages/EmployeeManagerPage';
import Header from './components/Header';
import CredentialsSignInPage from './pages/SignIn';
import { CircularProgress } from '@mui/material';
import { Session } from '@supabase/supabase-js';
import supabase from './api/supabaseClient';
import ProductManagmentPage from './pages/ProductManagmentPage';
import ProductNavigationPage from './pages/ProductNavigationPage';
import StoreStatsPage from './pages/StoreStatsPage';

const App: React.FC = () => {

  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      setLoading(false);
    });

    const { data: authListener } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
    });

    return () => {
      authListener.subscription.unsubscribe();
    };
  }, []);
  
  
  if (loading) return <CircularProgress />;

  return (
    <Router>
      <Header/>
      <Routes>
        <Route path="/" element={session? <Dashboard />: <Navigate to="/signin" />} />
        <Route path="/signin" element={<CredentialsSignInPage />} />
        <Route path="/employee-management" element={session? <EmployeeManagerPage />: <Navigate to="/signin" />} />
        <Route path="/product-management" element={session? <ProductNavigationPage />: <Navigate to="/signin" />} />
        <Route path="/products" element={session? <ProductManagmentPage />: <Navigate to="/signin" />} />
        <Route path="/store-management" element={session? <StoreStatsPage />: <Navigate to="/signin" />} />
      </Routes>
    </Router>
  );
};

export default App;
