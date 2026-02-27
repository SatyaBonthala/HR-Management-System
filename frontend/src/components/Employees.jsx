import { useState, useEffect } from 'react';
import { employeeAPI } from '../api';

export default function Employees() {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    position: '',
    department: '',
    hire_date: '',
    salary: 0,
  });

  useEffect(() => {
    loadEmployees();
  }, []);

  const loadEmployees = async () => {
    try {
      const response = await employeeAPI.getAll();
      setEmployees(response.data);
    } catch (error) {
      console.error('Error loading employees:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await employeeAPI.create(formData);
      setShowForm(false);
      setFormData({
        name: '',
        email: '',
        phone: '',
        position: '',
        department: '',
        hire_date: '',
        salary: 0,
      });
      loadEmployees();
    } catch (error) {
      console.error('Error creating employee:', error);
      alert('Error creating employee: ' + (error.response?.data?.detail || error.message));
    }
  };

  if (loading) {
    return <div className="flex justify-center items-center h-64">Loading...</div>;
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Employees</h1>
          <p className="mt-2 text-gray-600">Manage your workforce</p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="btn btn-primary"
        >
          {showForm ? '✕ Cancel' : '➕ Add Employee'}
        </button>
      </div>

      {showForm && (
        <div className="card mb-6">
          <h2 className="text-xl font-bold mb-4">Add New Employee</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="label">Name</label>
                <input
                  type="text"
                  className="input"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  required
                />
              </div>
              <div>
                <label className="label">Email</label>
                <input
                  type="email"
                  className="input"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  required
                />
              </div>
              <div>
                <label className="label">Phone</label>
                <input
                  type="text"
                  className="input"
                  value={formData.phone}
                  onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                />
              </div>
              <div>
                <label className="label">Position</label>
                <input
                  type="text"
                  className="input"
                  value={formData.position}
                  onChange={(e) => setFormData({ ...formData, position: e.target.value })}
                  required
                />
              </div>
              <div>
                <label className="label">Department</label>
                <input
                  type="text"
                  className="input"
                  value={formData.department}
                  onChange={(e) => setFormData({ ...formData, department: e.target.value })}
                  required
                />
              </div>
              <div>
                <label className="label">Hire Date</label>
                <input
                  type="date"
                  className="input"
                  value={formData.hire_date}
                  onChange={(e) => setFormData({ ...formData, hire_date: e.target.value })}
                  required
                />
              </div>
              <div>
                <label className="label">Salary</label>
                <input
                  type="number"
                  className="input"
                  value={formData.salary}
                  onChange={(e) => setFormData({ ...formData, salary: parseFloat(e.target.value) })}
                  min="0"
                  step="1000"
                />
              </div>
            </div>
            <div className="flex gap-3">
              <button type="submit" className="btn btn-primary">
                Add Employee
              </button>
              <button
                type="button"
                onClick={() => setShowForm(false)}
                className="btn btn-secondary"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {employees.map((employee) => (
          <div key={employee.id} className="card hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between mb-3">
              <div className="w-12 h-12 bg-gradient-to-br from-primary-400 to-primary-600 rounded-full flex items-center justify-center">
                <span className="text-xl text-white">👨‍💼</span>
              </div>
              <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                employee.is_active 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-gray-100 text-gray-800'
              }`}>
                {employee.is_active ? 'Active' : 'Inactive'}
              </span>
            </div>
            
            <h3 className="text-lg font-bold text-gray-900 mb-1">{employee.name}</h3>
            <p className="text-sm text-primary-600 font-medium mb-3">{employee.position}</p>
            
            <div className="space-y-2 text-sm text-gray-600">
              <div className="flex items-center">
                <span className="mr-2">📧</span>
                {employee.email}
              </div>
              {employee.phone && (
                <div className="flex items-center">
                  <span className="mr-2">📞</span>
                  {employee.phone}
                </div>
              )}
              <div className="flex items-center">
                <span className="mr-2">🏢</span>
                {employee.department}
              </div>
              <div className="flex items-center">
                <span className="mr-2">📅</span>
                Joined: {new Date(employee.hire_date).toLocaleDateString()}
              </div>
            </div>
          </div>
        ))}
      </div>

      {employees.length === 0 && (
        <div className="card text-center py-12">
          <div className="text-6xl mb-4">👨‍💼</div>
          <h3 className="text-xl font-bold text-gray-900 mb-2">No employees yet</h3>
          <p className="text-gray-600 mb-4">Add your first employee to get started</p>
          <button onClick={() => setShowForm(true)} className="btn btn-primary">
            ➕ Add Employee
          </button>
        </div>
      )}
    </div>
  );
}
