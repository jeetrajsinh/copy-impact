// frontend/src/App.tsx
import Navbar from './components/layout/Navbar';
import DashboardPage from './pages/DashboardPage';

function App() {
  return (
    <div className="min-h-screen bg-dark-bg">
      <Navbar />
      <DashboardPage /> {/* The DashboardPage now includes the Sidebar */}
    </div>
  );
}
export default App;