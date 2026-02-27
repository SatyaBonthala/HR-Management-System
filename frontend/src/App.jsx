import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import Candidates from './components/Candidates';
import Positions from './components/Positions';
import Applications from './components/Applications';
import Employees from './components/Employees';
// import Onboarding from './components/Onboarding';

function Navigation() {
  const location = useLocation();
  
  const navItems = [
    { path: '/', label: 'Dashboard', icon: '📊' },
    { path: '/positions', label: 'Job Positions', icon: '💼' },
    { path: '/candidates', label: 'Candidates', icon: '👥' },
    { path: '/applications', label: 'Applications', icon: '📝' },
    { path: '/employees', label: 'Employees', icon: '👨‍💼' },
    // { path: '/onboarding', label: 'Onboarding', icon: '🚀' },
  ];

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <div className="flex-shrink-0 flex items-center">
              <h1 className="text-2xl font-bold text-primary-600">HR System</h1>
            </div>
            <div className="hidden sm:ml-8 sm:flex sm:space-x-4">
              {navItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`inline-flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors ${
                    location.pathname === item.path
                      ? 'bg-primary-100 text-primary-700'
                      : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                  }`}
                >
                  <span className="mr-2">{item.icon}</span>
                  {item.label}
                </Link>
              ))}
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navigation />
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/candidates" element={<Candidates />} />
            <Route path="/positions" element={<Positions />} />
            <Route path="/applications" element={<Applications />} />
            <Route path="/employees" element={<Employees />} />
            {/* <Route path="/onboarding" element={<Onboarding />} /> */}
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
