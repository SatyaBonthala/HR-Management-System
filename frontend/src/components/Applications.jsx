import { useState, useEffect } from 'react';
import { applicationAPI, candidateAPI, positionAPI } from '../api';

export default function Applications() {
  const [applications, setApplications] = useState([]);
  const [candidates, setCandidates] = useState([]);
  const [positions, setPositions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    candidate_id: '',
    position_id: '',
  });
  const [selectedApp, setSelectedApp] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [appsRes, candsRes, posRes] = await Promise.all([
        applicationAPI.getAll(),
        candidateAPI.getAll(),
        positionAPI.getAll(),
      ]);
      
      // Format applications to include ai_screening object
      const formattedApps = appsRes.data.map(app => ({
        ...app,
        ai_screening: app.screening_notes || app.strengths || app.concerns ? {
          match_score: app.match_score || 0,
          summary: app.screening_notes || "",
          strengths: app.strengths || [],
          concerns: app.concerns || [],
          recommendation: app.recommendation || "review"
        } : null
      }));
      
      setApplications(formattedApps);
      setCandidates(candsRes.data);
      setPositions(posRes.data);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Check for duplicate application
    const isDuplicate = applications.some(
      app => app.candidate_id === formData.candidate_id && app.position_id === formData.position_id
    );
    
    if (isDuplicate) {
      alert('This candidate has already applied for this position!');
      return;
    }
    
    // Validate candidate and position exist
    const candidateExists = candidates.some(c => c.id === formData.candidate_id);
    const positionExists = positions.some(p => p.id === formData.position_id);
    
    if (!candidateExists) {
      alert('Selected candidate not found. Please select a valid candidate.');
      return;
    }
    
    if (!positionExists) {
      alert('Selected position not found. Please select a valid position.');
      return;
    }
    
    try {
      const response = await applicationAPI.create(formData);
      setShowForm(false);
      setFormData({ candidate_id: '', position_id: '' });
      
      // Format the response to add ai_screening object
      const formattedApp = {
        ...response.data,
        ai_screening: response.data.screening_notes || response.data.strengths || response.data.concerns ? {
          match_score: 0, // Will be updated after screening completes
          summary: response.data.screening_notes || "",
          strengths: response.data.strengths || [],
          concerns: response.data.concerns || [],
          recommendation: response.data.recommendation || "review"
        } : null
      };
      
      setSelectedApp(formattedApp);
      
      // Show info message that screening is in progress
      alert('✅ Application submitted successfully! AI screening is running in the background. Refresh the page in a few seconds to see the results.');
      
      // Reload after a delay to get AI screening results
      setTimeout(() => loadData(), 3000);
    } catch (error) {
      console.error('Error creating application:', error);
      const errorMsg = error.response?.data?.detail || error.message;
      alert(`Error creating application: ${errorMsg}\n\nTip: Check if the candidate and position exist, and if this application was already submitted.`);
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      pending: 'bg-yellow-100 text-yellow-800',
      screening: 'bg-blue-100 text-blue-800',
      interview: 'bg-purple-100 text-purple-800',
      offered: 'bg-green-100 text-green-800',
      hired: 'bg-green-200 text-green-900',
      rejected: 'bg-red-100 text-red-800',
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  if (loading) {
    return <div className="flex justify-center items-center h-64">Loading...</div>;
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Applications</h1>
          <p className="mt-2 text-gray-600">Track and manage job applications with AI screening</p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={loadData}
            className="btn btn-secondary flex items-center gap-2"
            disabled={loading}
          >
            <span>🔄</span>
            {loading ? 'Loading...' : 'Refresh'}
          </button>
          <button
            onClick={() => setShowForm(!showForm)}
            className="btn btn-primary"
          >
            {showForm ? '✕ Cancel' : '➕ Submit Application'}
          </button>
        </div>
      </div>

      {showForm && (
        <div className="card mb-6">
          <h2 className="text-xl font-bold mb-4">Submit New Application</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="label">Select Candidate</label>
              <select
                className="input"
                value={formData.candidate_id}
                onChange={(e) => setFormData({ ...formData, candidate_id: parseInt(e.target.value) })}
                required
              >
                <option value="">Choose a candidate...</option>
                {candidates.map((cand) => (
                  <option key={cand.id} value={cand.id}>
                    {cand.name} ({cand.email})
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="label">Select Position</label>
              <select
                className="input"
                value={formData.position_id}
                onChange={(e) => setFormData({ ...formData, position_id: parseInt(e.target.value) })}
                required
              >
                <option value="">Choose a position...</option>
                {positions.filter(p => p.is_active).map((pos) => (
                  <option key={pos.id} value={pos.id}>
                    {pos.title} - {pos.department}
                  </option>
                ))}
              </select>
            </div>
            <div className="flex gap-3">
              <button type="submit" className="btn btn-primary">
                🤖 Submit & Run AI Screening
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

      {selectedApp && (
        <div className="card mb-6 border-2 border-primary-500">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold text-gray-900">🤖 AI Screening Result</h2>
            <button
              onClick={() => setSelectedApp(null)}
              className="text-gray-400 hover:text-gray-600"
            >
              ✕
            </button>
          </div>
          
          {selectedApp.ai_screening && (
            <div className="space-y-4">
              <div className="flex items-center gap-4">
                <div className="text-center">
                  <div className="text-4xl font-bold text-primary-600">
                    {selectedApp.ai_screening.match_score}
                  </div>
                  <div className="text-sm text-gray-600">Match Score</div>
                </div>
                <div className="flex-1">
                  <div className="w-full bg-gray-200 rounded-full h-4">
                    <div
                      className="bg-primary-600 h-4 rounded-full transition-all"
                      style={{ width: `${selectedApp.ai_screening.match_score}%` }}
                    />
                  </div>
                </div>
              </div>

              <div>
                <h3 className="font-bold text-gray-900 mb-2">Summary</h3>
                <p className="text-gray-700">{selectedApp.ai_screening.summary}</p>
              </div>

              <div>
                <h3 className="font-bold text-gray-900 mb-2">✅ Strengths</h3>
                <ul className="list-disc list-inside space-y-1">
                  {selectedApp.ai_screening.strengths?.map((strength, idx) => (
                    <li key={idx} className="text-gray-700">{strength}</li>
                  ))}
                </ul>
              </div>

              <div>
                <h3 className="font-bold text-gray-900 mb-2">⚠️ Concerns</h3>
                <ul className="list-disc list-inside space-y-1">
                  {selectedApp.ai_screening.concerns?.map((concern, idx) => (
                    <li key={idx} className="text-gray-700">{concern}</li>
                  ))}
                </ul>
              </div>

              <div className="pt-4 border-t">
                <span className="font-bold text-gray-900 mr-2">Recommendation:</span>
                <span className={`px-3 py-1 text-sm font-medium rounded-full ${
                  selectedApp.ai_screening.recommendation === 'recommend' 
                    ? 'bg-green-100 text-green-800'
                    : selectedApp.ai_screening.recommendation === 'review'
                    ? 'bg-yellow-100 text-yellow-800'
                    : 'bg-red-100 text-red-800'
                }`}>
                  {selectedApp.ai_screening.recommendation?.toUpperCase()}
                </span>
              </div>
            </div>
          )}
        </div>
      )}

      <div className="space-y-4">
        {applications.map((app) => {
          const candidate = candidates.find(c => c.id === app.candidate_id);
          const position = positions.find(p => p.id === app.position_id);
          const isScreening = app.status === 'screening';
          const hasScreeningResults = app.ai_screening && (app.ai_screening.summary || app.ai_screening.strengths?.length > 0);
          
          return (
            <div key={app.id} className="card hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-4 mb-3">
                    <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                      <span className="text-xl">📝</span>
                    </div>
                    <div>
                      <h3 className="text-lg font-bold text-gray-900">
                        {candidate?.name || 'Unknown'}
                      </h3>
                      <p className="text-sm text-gray-600">
                        Applied for: <span className="font-medium">{position?.title || 'Unknown'}</span>
                      </p>
                    </div>
                  </div>

                  {/* AI Screening Results */}
                  {hasScreeningResults ? (
                    <div className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-lg p-4 mt-3 border border-primary-200">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm font-medium text-gray-700">🤖 AI Match Score</span>
                        <span className="text-2xl font-bold text-primary-600">
                          {app.ai_screening.match_score || 0}
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2 mb-3">
                        <div
                          className="bg-primary-600 h-2 rounded-full transition-all"
                          style={{ width: `${app.ai_screening.match_score || 0}%` }}
                        />
                      </div>
                      <p className="text-sm text-gray-700 line-clamp-2 mb-2">{app.ai_screening.summary}</p>
                      <button
                        onClick={() => setSelectedApp(app)}
                        className="btn btn-primary text-sm py-1 px-3"
                      >
                        📊 View Full AI Analysis
                      </button>
                    </div>
                  ) : isScreening ? (
                    <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mt-3">
                      <div className="flex items-center gap-2 mb-2">
                        <div className="animate-spin text-xl">⏳</div>
                        <span className="font-medium text-yellow-800">AI Screening in Progress...</span>
                      </div>
                      <p className="text-sm text-yellow-700 mb-3">
                        Our AI agent is analyzing the resume and matching it to the job requirements. This usually takes 5-10 seconds.
                      </p>
                      <button
                        onClick={() => {
                          loadData();
                          setTimeout(() => {
                            const updatedApp = applications.find(a => a.id === app.id);
                            if (updatedApp?.ai_screening) {
                              setSelectedApp(updatedApp);
                            }
                          }, 1000);
                        }}
                        className="btn btn-secondary text-sm py-1 px-3"
                      >
                        🔄 Check for Results
                      </button>
                    </div>
                  ) : (
                    <div className="bg-gray-50 rounded-lg p-4 mt-3">
                      <p className="text-sm text-gray-600">
                        Application submitted. Awaiting screening.
                      </p>
                    </div>
                  )}
                </div>

                <div className="ml-4 flex flex-col gap-2">
                  <span className={`px-3 py-1 text-xs font-medium rounded-full ${getStatusColor(app.status)}`}>
                    {app.status}
                  </span>
                  {hasScreeningResults && app.ai_screening.recommendation && (
                    <span className={`px-3 py-1 text-xs font-medium rounded-full text-center ${
                      app.ai_screening.recommendation === 'recommend' 
                        ? 'bg-green-100 text-green-800'
                        : app.ai_screening.recommendation === 'review'
                        ? 'bg-yellow-100 text-yellow-800'
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {app.ai_screening.recommendation}
                    </span>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {applications.length === 0 && (
        <div className="card text-center py-12">
          <div className="text-6xl mb-4">📝</div>
          <h3 className="text-xl font-bold text-gray-900 mb-2">No applications yet</h3>
          <p className="text-gray-600 mb-4">Submit your first application to see AI screening in action</p>
          <button onClick={() => setShowForm(true)} className="btn btn-primary">
            ➕ Submit Application
          </button>
        </div>
      )}
    </div>
  );
}
