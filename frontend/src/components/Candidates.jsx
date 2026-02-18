import { useState, useEffect } from 'react';
import { candidateAPI } from '../api';

export default function Candidates() {
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    skills: '',
    experience_years: 0,
    resume_text: '',
  });

  useEffect(() => {
    loadCandidates();
  }, []);

  const loadCandidates = async () => {
    try {
      const response = await candidateAPI.getAll();
      setCandidates(response.data);
    } catch (error) {
      console.error('Error loading candidates:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await candidateAPI.create({
        ...formData,
        skills: formData.skills.split(',').map(s => s.trim()),
      });
      setShowForm(false);
      setFormData({
        name: '',
        email: '',
        phone: '',
        skills: '',
        experience_years: 0,
        resume_text: '',
      });
      loadCandidates();
    } catch (error) {
      console.error('Error creating candidate:', error);
      alert('Error creating candidate: ' + (error.response?.data?.detail || error.message));
    }
  };

  if (loading) {
    return <div className="flex justify-center items-center h-64">Loading...</div>;
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Candidates</h1>
          <p className="mt-2 text-gray-600">Manage your candidate pool</p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="btn btn-primary"
        >
          {showForm ? '✕ Cancel' : '➕ Add Candidate'}
        </button>
      </div>

      {showForm && (
        <div className="card mb-6">
          <h2 className="text-xl font-bold mb-4">Add New Candidate</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
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
              <label className="label">Skills (comma-separated)</label>
              <input
                type="text"
                className="input"
                value={formData.skills}
                onChange={(e) => setFormData({ ...formData, skills: e.target.value })}
                placeholder="Python, React, SQL"
                required
              />
            </div>
            <div>
              <label className="label">Years of Experience</label>
              <input
                type="number"
                className="input"
                value={formData.experience_years}
                onChange={(e) => setFormData({ ...formData, experience_years: parseInt(e.target.value) })}
                min="0"
                required
              />
            </div>
            <div>
              <label className="label">Resume Text</label>
              <textarea
                className="input"
                rows="6"
                value={formData.resume_text}
                onChange={(e) => setFormData({ ...formData, resume_text: e.target.value })}
                placeholder="Paste resume content here..."
                required
              />
            </div>
            <div className="flex gap-3">
              <button type="submit" className="btn btn-primary">
                Create Candidate
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
        {candidates.map((candidate) => (
          <div key={candidate.id} className="card hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between mb-3">
              <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center">
                <span className="text-xl">👤</span>
              </div>
              <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">
                Active
              </span>
            </div>
            <h3 className="text-lg font-bold text-gray-900 mb-1">{candidate.name}</h3>
            <p className="text-sm text-gray-600 mb-2">{candidate.email}</p>
            {candidate.phone && (
              <p className="text-sm text-gray-600 mb-3">📞 {candidate.phone}</p>
            )}
            <div className="mb-3">
              <p className="text-xs font-medium text-gray-700 mb-1">Skills:</p>
              <div className="flex flex-wrap gap-1">
                {candidate.skills?.map((skill, idx) => (
                  <span key={idx} className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded">
                    {skill}
                  </span>
                ))}
              </div>
            </div>
            <p className="text-sm text-gray-600">
              Experience: <span className="font-medium">{candidate.experience_years} years</span>
            </p>
          </div>
        ))}
      </div>

      {candidates.length === 0 && (
        <div className="card text-center py-12">
          <div className="text-6xl mb-4">👥</div>
          <h3 className="text-xl font-bold text-gray-900 mb-2">No candidates yet</h3>
          <p className="text-gray-600 mb-4">Add your first candidate to get started</p>
          <button onClick={() => setShowForm(true)} className="btn btn-primary">
            ➕ Add Candidate
          </button>
        </div>
      )}
    </div>
  );
}
