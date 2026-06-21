import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AppProvider, useApp } from './contexts/AppContext';
import Layout from './components/Layout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Students from './pages/Students';
import Admissions from './pages/Admissions';
import Classes from './pages/Classes';
import Income from './pages/Income';
import Expenses from './pages/Expenses';
import Installments from './pages/Installments';
import Teachers from './pages/Teachers';
import Salaries from './pages/Salaries';
import Events from './pages/Events';
import Reports from './pages/Reports';
import Users from './pages/Users';
import KidsArea from './pages/KidsArea';
import BusManagement from './pages/BusManagement';
import Inventory from './pages/Inventory';
import Calendar from './pages/Calendar';
import { Toaster } from 'react-hot-toast';
import { PageTransition } from './components/ui/PageTransition';
import { AnimatePresence } from 'framer-motion';
import { useLocation } from 'react-router-dom';

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { currentUser } = useApp();
  if (!currentUser) {
    return <Navigate to="/login" replace />;
  }
  return <>{children}</>;
}

function AppRoutes() {
  const { currentUser } = useApp();
  const location = useLocation();

  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/login" element={<PageTransition>{currentUser ? <Navigate to="/" replace /> : <Login />}</PageTransition>} />
        <Route path="/" element={<ProtectedRoute><Layout /></ProtectedRoute>}>
          <Route index element={<PageTransition><Dashboard /></PageTransition>} />
          <Route path="students" element={<PageTransition><Students /></PageTransition>} />
          <Route path="admissions" element={<PageTransition><Admissions /></PageTransition>} />
          <Route path="classes" element={<PageTransition><Classes /></PageTransition>} />
          <Route path="income" element={<PageTransition><Income /></PageTransition>} />
          <Route path="expenses" element={<PageTransition><Expenses /></PageTransition>} />
          <Route path="installments" element={<PageTransition><Installments /></PageTransition>} />
          <Route path="teachers" element={<PageTransition><Teachers /></PageTransition>} />
          <Route path="salaries" element={<PageTransition><Salaries /></PageTransition>} />
          <Route path="events" element={<PageTransition><Events /></PageTransition>} />
          <Route path="reports" element={<PageTransition><Reports /></PageTransition>} />
          <Route path="users" element={<PageTransition><Users /></PageTransition>} />
          <Route path="kids-area" element={<PageTransition><KidsArea /></PageTransition>} />
          <Route path="bus" element={<PageTransition><BusManagement /></PageTransition>} />
          <Route path="inventory" element={<PageTransition><Inventory /></PageTransition>} />
          <Route path="calendar" element={<PageTransition><Calendar /></PageTransition>} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AnimatePresence>
  );
}

import { LanguageProvider } from './contexts/LanguageContext';

export default function App() {
  return (
    <BrowserRouter>
      <LanguageProvider>
        <AppProvider>
          <Toaster position="top-center" reverseOrder={false} />
          <AppRoutes />
        </AppProvider>
      </LanguageProvider>
    </BrowserRouter>
  );
}
