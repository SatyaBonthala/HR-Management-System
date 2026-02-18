import { useState, useEffect } from 'react';
import { employeeAPI, onboardingAPI } from '../api';
import { useLocation } from 'react-router-dom';

export default function Onboarding() {
  const location = useLocation();
  const [employees, setEmployees] = useState([]);
  const [selectedEmployee, setSelectedEmployee] = useState(null);
  const [checklist, setChecklist] = useState(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [chatMessage, setChatMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [chatLoading, setChatLoading] = useState(false);

  useEffect(() => {
    loadEmployees();
  }, []);

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const empId = params.get('employee');
    if (empId && employees.length > 0) {
      const emp = employees.find(e => e.id === parseInt(empId));
      if (emp) setSelectedEmployee(emp);
    }
  }, [location, employees]);

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

  const generateChecklist = async () => {
    if (!selectedEmployee) return;
    
    setGenerating(true);
    try {
      const response = await onboardingAPI.createChecklist(selectedEmployee.id, {
        name: selectedEmployee.name,
        position: selectedEmployee.position,
        department: selectedEmployee.department,
        hire_date: selectedEmployee.hire_date,
      });
      setChecklist(response.data);
    } catch (error) {
      console.error('Error generating checklist:', error);
      alert('Error generating checklist: ' + (error.response?.data?.detail || error.message));
    } finally {
      setGenerating(false);
    }
  };

  const handleChatSubmit = async (e) => {
    e.preventDefault();
    if (!chatMessage.trim() || !selectedEmployee) return;

    const userMessage = chatMessage;
    setChatMessage('');
    setChatHistory([...chatHistory, { role: 'employee', content: userMessage }]);
    setChatLoading(true);

    try {
      const response = await onboardingAPI.askQuestion(selectedEmployee.id, {
        message: userMessage,
        employee_data: {
          name: selectedEmployee.name,
          position: selectedEmployee.position,
          department: selectedEmployee.department,
        },
        conversation_history: chatHistory,
      });

      setChatHistory([
        ...chatHistory,
        { role: 'employee', content: userMessage },
        { role: 'agent', content: response.data.response },
      ]);
    } catch (error) {
      console.error('Error sending message:', error);
      alert('Error: ' + (error.response?.data?.detail || error.message));
    } finally {
      setChatLoading(false);
    }
  };

  if (loading) {
    return <div className="flex justify-center items-center h-64">Loading...</div>;
  }

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Onboarding</h1>
        <p className="mt-2 text-gray-600">AI-powered employee onboarding assistance</p>
      </div>

      {!selectedEmployee ? (
        <div className="card">
          <h2 className="text-xl font-bold mb-4">Select an Employee</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {employees.map((emp) => (
              <button
                key={emp.id}
                onClick={() => setSelectedEmployee(emp)}
                className="text-left p-4 border-2 border-gray-200 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition-all"
              >
                <div className="flex items-center gap-3 mb-2">
                  <div className="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                    <span className="text-lg">👤</span>
                  </div>
                  <div>
                    <h3 className="font-bold text-gray-900">{emp.name}</h3>
                    <p className="text-sm text-gray-600">{emp.position}</p>
                  </div>
                </div>
              </button>
            ))}
          </div>
          {employees.length === 0 && (
            <div className="text-center py-8">
              <p className="text-gray-600">No employees found. Add employees first.</p>
            </div>
          )}
        </div>
      ) : (
        <div className="space-y-6">
          <div className="card">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="w-16 h-16 bg-gradient-to-br from-primary-400 to-primary-600 rounded-full flex items-center justify-center">
                  <span className="text-2xl text-white">👨‍💼</span>
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">{selectedEmployee.name}</h2>
                  <p className="text-gray-600">{selectedEmployee.position} • {selectedEmployee.department}</p>
                </div>
              </div>
              <button
                onClick={() => {
                  setSelectedEmployee(null);
                  setChecklist(null);
                  setChatHistory([]);
                }}
                className="btn btn-secondary"
              >
                ← Back
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Onboarding Checklist */}
            <div className="card">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-bold text-gray-900">📋 Onboarding Checklist</h3>
                <button
                  onClick={generateChecklist}
                  disabled={generating}
                  className="btn btn-primary text-sm"
                >
                  {generating ? '⏳ Generating...' : '🤖 Generate AI Checklist'}
                </button>
              </div>

              {checklist ? (
                <div className="space-y-3">
                  {checklist.checklist?.map((task, idx) => (
                    <div key={idx} className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg">
                      <input
                        type="checkbox"
                        checked={task.completed}
                        onChange={() => {
                          const updated = [...checklist.checklist];
                          updated[idx].completed = !updated[idx].completed;
                          setChecklist({ ...checklist, checklist: updated });
                        }}
                        className="mt-1 w-4 h-4 text-primary-600 rounded focus:ring-primary-500"
                      />
                      <div className="flex-1">
                        <p className={`font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                          {task.name}
                        </p>
                        <span className={`text-xs px-2 py-1 rounded ${
                          task.priority === 'high'
                            ? 'bg-red-100 text-red-800'
                            : task.priority === 'medium'
                            ? 'bg-yellow-100 text-yellow-800'
                            : 'bg-green-100 text-green-800'
                        }`}>
                          {task.priority}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8">
                  <div className="text-4xl mb-3">🤖</div>
                  <p className="text-gray-600 mb-4">
                    Generate a personalized onboarding checklist using AI
                  </p>
                  <button onClick={generateChecklist} className="btn btn-primary">
                    Generate Checklist
                  </button>
                </div>
              )}
            </div>

            {/* AI Chat Assistant */}
            <div className="card flex flex-col h-[600px]">
              <h3 className="text-xl font-bold text-gray-900 mb-4">💬 AI Onboarding Assistant</h3>
              
              <div className="flex-1 overflow-y-auto space-y-3 mb-4">
                {chatHistory.length === 0 ? (
                  <div className="text-center py-8">
                    <div className="text-4xl mb-3">🤖</div>
                    <p className="text-gray-600 mb-2">Ask me anything about onboarding!</p>
                    <div className="text-sm text-gray-500 space-y-1">
                      <p>• "What do I need to do on my first day?"</p>
                      <p>• "How do I set up my email?"</p>
                      <p>• "Where can I find the employee handbook?"</p>
                    </div>
                  </div>
                ) : (
                  chatHistory.map((msg, idx) => (
                    <div
                      key={idx}
                      className={`flex ${msg.role === 'employee' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div
                        className={`max-w-[80%] rounded-lg px-4 py-2 ${
                          msg.role === 'employee'
                            ? 'bg-primary-600 text-white'
                            : 'bg-gray-100 text-gray-900'
                        }`}
                      >
                        <p className="text-sm">{msg.content}</p>
                      </div>
                    </div>
                  ))
                )}
                {chatLoading && (
                  <div className="flex justify-start">
                    <div className="bg-gray-100 rounded-lg px-4 py-2">
                      <p className="text-sm text-gray-600">Thinking...</p>
                    </div>
                  </div>
                )}
              </div>

              <form onSubmit={handleChatSubmit} className="flex gap-2">
                <input
                  type="text"
                  className="input flex-1"
                  placeholder="Ask your onboarding question..."
                  value={chatMessage}
                  onChange={(e) => setChatMessage(e.target.value)}
                  disabled={chatLoading}
                />
                <button
                  type="submit"
                  disabled={chatLoading || !chatMessage.trim()}
                  className="btn btn-primary"
                >
                  Send
                </button>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
