import { useState, useEffect } from 'react';
import { positionAPI } from '../api';

export default function Positions() {
  const [positions, setPositions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    department: '',
    description: '',
    required_skills: '',
    experience_required: 0,
    salary_range: '',
  });

  useEffect(() => {
    loadPositions();
  }, []);

  const loadPositions = async () => {
    try {
      const response = await positionAPI.getAll();
      setPositions(response.data);
    } catch (error) {
      console.error('Error loading positions:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await positionAPI.create({
        ...formData,
        required_skills: formData.required_skills.split(',').map(s => s.trim()),
      });
      setShowForm(false);
      setFormData({
        title: '',
        department: '',
        description: '',
        required_skills: '',
        experience_required: 0,
        salary_range: '',
      });
      loadPositions();
    } catch (error) {
      console.error('Error creating position:', error);
      alert('Error creating position: ' + (error.response?.data?.detail || error.message));
    }
  };

  if (loading) {
    return <div className="flex justify-center items-center h-64">Loading...</div>;
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Job Positions</h1>
          <p className="mt-2 text-gray-600">Manage open positions and job listings</p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="btn btn-primary"
        >
          {showForm ? '✕ Cancel' : '➕ Create Position'}
        </button>
      </div>

      {showForm && (
        <div className="card mb-6">
          <h2 className="text-xl font-bold mb-4">Create New Position</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="label">Job Title</label>
              <input
                type="text"
                className="input"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
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
              <label className="label">Description</label>
              <textarea
                className="input"
                rows="4"
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                required
              />
            </div>
            <div>
              <label className="label">Required Skills (comma-separated)</label>
              <input
                type="text"
                className="input"
                value={formData.required_skills}
                onChange={(e) => setFormData({ ...formData, required_skills: e.target.value })}
                placeholder="Python, React, SQL"
                required
              />
            </div>
            <div>
              <label className="label">Years of Experience Required</label>
              <input
                type="number"
                className="input"
                value={formData.experience_required}
                onChange={(e) => setFormData({ ...formData, experience_required: parseInt(e.target.value) })}
                min="0"
                required
              />
            </div>
            <div>
              <label className="label">Salary Range</label>
              <input
                type="text"
                className="input"
                value={formData.salary_range}
                onChange={(e) => setFormData({ ...formData, salary_range: e.target.value })}
                placeholder="$80,000 - $120,000"
              />
            </div>
            <div className="flex gap-3">
              <button type="submit" className="btn btn-primary">
                Create Position
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

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {positions.map((position) => (
          <div key={position.id} className="card hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between mb-4">
              <div>
                <h3 className="text-xl font-bold text-gray-900">{position.title}</h3>
                <p className="text-sm text-primary-600 font-medium">{position.department}</p>
              </div>
              <span className={`px-3 py-1 text-xs font-medium rounded-full ${
                position.is_active 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-gray-100 text-gray-800'
              }`}>
                {position.is_active ? '🟢 Active' : '⚫ Closed'}
              </span>
            </div>
            
            <p className="text-gray-700 mb-4 line-clamp-3">{position.description}</p>
            
            <div className="space-y-2 mb-4">
              <div className="flex items-center text-sm text-gray-600">
                <span className="font-medium mr-2">💼 Experience:</span>
                {position.experience_required}+ years
              </div>
              {position.salary_range && (
                <div className="flex items-center text-sm text-gray-600">
                  <span className="font-medium mr-2">💰 Salary:</span>
                  {position.salary_range}
                </div>
              )}
            </div>
            
            <div>
              <p className="text-xs font-medium text-gray-700 mb-2">Required Skills:</p>
              <div className="flex flex-wrap gap-1">
                {position.required_skills?.map((skill, idx) => (
                  <span key={idx} className="px-2 py-1 text-xs bg-purple-100 text-purple-800 rounded">
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>

      {positions.length === 0 && (
        <div className="card text-center py-12">
          <div className="text-6xl mb-4">💼</div>
          <h3 className="text-xl font-bold text-gray-900 mb-2">No positions yet</h3>
          <p className="text-gray-600 mb-4">Create your first job position to start hiring</p>
          <button onClick={() => setShowForm(true)} className="btn btn-primary">
            ➕ Create Position
          </button>
        </div>
      )}
    </div>
  );
}
