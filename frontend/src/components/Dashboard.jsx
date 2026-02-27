import { useState, useEffect } from 'react';
import { candidateAPI, positionAPI, applicationAPI, employeeAPI } from '../api';

export default function Dashboard() {
  const [stats, setStats] = useState({
    candidates: 0,
    positions: 0,
    applications: 0,
    employees: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const [candidates, positions, applications, employees] = await Promise.all([
        candidateAPI.getAll(),
        positionAPI.getAll(),
        applicationAPI.getAll(),
        employeeAPI.getAll(),
      ]);

      setStats({
        candidates: candidates.data.length,
        positions: positions.data.length,
        applications: applications.data.length,
        employees: employees.data.length,
      });
    } catch (error) {
      console.error('Error loading stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const statCards = [
    { label: 'Total Candidates', value: stats.candidates, icon: '👥', color: 'bg-blue-500' },
    { label: 'Open Positions', value: stats.positions, icon: '💼', color: 'bg-green-500' },
    { label: 'Applications', value: stats.applications, icon: '📝', color: 'bg-purple-500' },
    { label: 'Employees', value: stats.employees, icon: '👨‍💼', color: 'bg-orange-500' },
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading...</div>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-2 text-gray-600">Welcome to your HR Management System</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {statCards.map((stat) => (
          <div key={stat.label} className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">{stat.label}</p>
                <p className="mt-2 text-3xl font-bold text-gray-900">{stat.value}</p>
              </div>
              <div className={`${stat.color} w-12 h-12 rounded-lg flex items-center justify-center text-2xl`}>
                {stat.icon}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-4">🤖 AI-Powered Features</h2>
          <div className="space-y-3">
            <div className="flex items-start">
              <div className="flex-shrink-0 w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                <span className="text-primary-600 font-bold">1</span>
              </div>
              <div className="ml-3">
                <p className="font-medium text-gray-900">Intelligent Resume Screening</p>
                <p className="text-sm text-gray-600">AI analyzes resumes and matches candidates to positions</p>
              </div>
            </div>
            {/* <div className="flex items-start">
              <div className="flex-shrink-0 w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                <span className="text-primary-600 font-bold">2</span>
              </div>
              <div className="ml-3">
                <p className="font-medium text-gray-900">Personalized Onboarding</p>
                <p className="text-sm text-gray-600">Generate custom onboarding checklists for new hires</p>
              </div>
            </div>
            <div className="flex items-start">
              <div className="flex-shrink-0 w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                <span className="text-primary-600 font-bold">3</span>
              </div>
              <div className="ml-3">
                <p className="font-medium text-gray-900">24/7 Onboarding Assistant</p>
                <p className="text-sm text-gray-600">AI chatbot answers employee questions instantly</p>
              </div>
            </div> */}
          </div>
        </div>

        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-4">🚀 Quick Actions</h2>
          <div className="grid grid-cols-2 gap-3">
            <button className="btn btn-primary text-left py-3">
              <div className="text-lg mb-1">➕ Add Position</div>
              <div className="text-xs opacity-90">Create new job opening</div>
            </button>
            <button className="btn btn-primary text-left py-3">
              <div className="text-lg mb-1">👤 Add Candidate</div>
              <div className="text-xs opacity-90">Register new candidate</div>
            </button>
            <button className="btn btn-primary text-left py-3">
              <div className="text-lg mb-1">📄 New Application</div>
              <div className="text-xs opacity-90">Submit application</div>
            </button>
            <button className="btn btn-primary text-left py-3">
              <div className="text-lg mb-1">👨‍💼 Add Employee</div>
              <div className="text-xs opacity-90">Add new employee</div>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
