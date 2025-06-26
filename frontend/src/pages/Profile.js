import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import axios from 'axios';
import toast from 'react-hot-toast';
import { 
  User, 
  Calendar, 
  Clock, 
  MapPin, 
  Edit, 
  Save, 
  X,
  Heart,
  Pill,
  AlertTriangle,
  Loader2
} from 'lucide-react';

const Profile = () => {
  const { user } = useAuth();
  const [profile, setProfile] = useState(null);
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [healthProfile, setHealthProfile] = useState({
    age: '',
    gender: '',
    medical_history: [],
    medications: [],
    allergies: []
  });
  const [newItem, setNewItem] = useState({
    medical_history: '',
    medications: '',
    allergies: ''
  });

  useEffect(() => {
    fetchProfile();
    fetchAppointments();
  }, []);

  const fetchProfile = async () => {
    try {
      const response = await axios.get('/api/profile');
      setProfile(response.data.user);
      setHealthProfile(response.data.user.health_profile);
    } catch (error) {
      toast.error('Failed to fetch profile');
    } finally {
      setLoading(false);
    }
  };

  const fetchAppointments = async () => {
    try {
      const response = await axios.get('/api/appointments');
      setAppointments(response.data.appointments);
    } catch (error) {
      console.error('Failed to fetch appointments:', error);
    }
  };

  const handleSave = async () => {
    try {
      await axios.put('/api/profile', {
        health_profile: healthProfile
      });
      toast.success('Profile updated successfully!');
      setEditing(false);
    } catch (error) {
      toast.error('Failed to update profile');
    }
  };

  const addItem = (type) => {
    if (newItem[type].trim()) {
      setHealthProfile(prev => ({
        ...prev,
        [type]: [...prev[type], newItem[type].trim()]
      }));
      setNewItem(prev => ({ ...prev, [type]: '' }));
    }
  };

  const removeItem = (type, index) => {
    setHealthProfile(prev => ({
      ...prev,
      [type]: prev[type].filter((_, i) => i !== index)
    }));
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'scheduled':
        return 'badge-warning';
      case 'completed':
        return 'badge-success';
      case 'cancelled':
        return 'badge-danger';
      default:
        return 'badge-secondary';
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Loader2 className="h-8 w-8 animate-spin text-primary-600" />
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center">
        <div className="flex justify-center mb-4">
          <User className="h-12 w-12 text-primary-600" />
        </div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          My Profile
        </h1>
        <p className="text-gray-600">
          Manage your health profile and view your appointments
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-8">
        {/* Personal Information */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Personal Information</h2>
          </div>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Name</label>
              <p className="mt-1 text-gray-900">{profile?.name}</p>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700">Email</label>
              <p className="mt-1 text-gray-900">{profile?.email}</p>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700">Member Since</label>
              <p className="mt-1 text-gray-900">
                {new Date(profile?.created_at).toLocaleDateString()}
              </p>
            </div>
          </div>
        </div>

        {/* Health Profile */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Health Profile</h2>
            <button
              onClick={() => setEditing(!editing)}
              className="flex items-center space-x-1 text-primary-600 hover:text-primary-700"
            >
              {editing ? <X className="h-4 w-4" /> : <Edit className="h-4 w-4" />}
              <span>{editing ? 'Cancel' : 'Edit'}</span>
            </button>
          </div>

          {editing ? (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Age</label>
                  <input
                    type="number"
                    value={healthProfile.age || ''}
                    onChange={(e) => setHealthProfile({...healthProfile, age: e.target.value})}
                    className="input-field"
                    placeholder="Enter age"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Gender</label>
                  <select
                    value={healthProfile.gender || ''}
                    onChange={(e) => setHealthProfile({...healthProfile, gender: e.target.value})}
                    className="input-field"
                  >
                    <option value="">Select gender</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                  </select>
                </div>
              </div>

              {/* Medical History */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Medical History
                </label>
                <div className="flex gap-2 mb-2">
                  <input
                    type="text"
                    value={newItem.medical_history}
                    onChange={(e) => setNewItem({...newItem, medical_history: e.target.value})}
                    className="input-field flex-1"
                    placeholder="Add medical condition"
                    onKeyPress={(e) => e.key === 'Enter' && addItem('medical_history')}
                  />
                  <button
                    onClick={() => addItem('medical_history')}
                    className="btn-primary px-3"
                  >
                    Add
                  </button>
                </div>
                <div className="flex flex-wrap gap-2">
                  {healthProfile.medical_history.map((item, index) => (
                    <span key={index} className="badge badge-warning flex items-center space-x-1">
                      <span>{item}</span>
                      <button
                        onClick={() => removeItem('medical_history', index)}
                        className="ml-1 hover:text-red-600"
                      >
                        <X className="h-3 w-3" />
                      </button>
                    </span>
                  ))}
                </div>
              </div>

              {/* Medications */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Current Medications
                </label>
                <div className="flex gap-2 mb-2">
                  <input
                    type="text"
                    value={newItem.medications}
                    onChange={(e) => setNewItem({...newItem, medications: e.target.value})}
                    className="input-field flex-1"
                    placeholder="Add medication"
                    onKeyPress={(e) => e.key === 'Enter' && addItem('medications')}
                  />
                  <button
                    onClick={() => addItem('medications')}
                    className="btn-primary px-3"
                  >
                    Add
                  </button>
                </div>
                <div className="flex flex-wrap gap-2">
                  {healthProfile.medications.map((item, index) => (
                    <span key={index} className="badge badge-success flex items-center space-x-1">
                      <span>{item}</span>
                      <button
                        onClick={() => removeItem('medications', index)}
                        className="ml-1 hover:text-red-600"
                      >
                        <X className="h-3 w-3" />
                      </button>
                    </span>
                  ))}
                </div>
              </div>

              {/* Allergies */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Allergies
                </label>
                <div className="flex gap-2 mb-2">
                  <input
                    type="text"
                    value={newItem.allergies}
                    onChange={(e) => setNewItem({...newItem, allergies: e.target.value})}
                    className="input-field flex-1"
                    placeholder="Add allergy"
                    onKeyPress={(e) => e.key === 'Enter' && addItem('allergies')}
                  />
                  <button
                    onClick={() => addItem('allergies')}
                    className="btn-primary px-3"
                  >
                    Add
                  </button>
                </div>
                <div className="flex flex-wrap gap-2">
                  {healthProfile.allergies.map((item, index) => (
                    <span key={index} className="badge badge-danger flex items-center space-x-1">
                      <span>{item}</span>
                      <button
                        onClick={() => removeItem('allergies', index)}
                        className="ml-1 hover:text-red-600"
                      >
                        <X className="h-3 w-3" />
                      </button>
                    </span>
                  ))}
                </div>
              </div>

              <button
                onClick={handleSave}
                className="btn-primary w-full"
              >
                Save Changes
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Age</label>
                  <p className="mt-1 text-gray-900">{healthProfile.age || 'Not specified'}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Gender</label>
                  <p className="mt-1 text-gray-900 capitalize">{healthProfile.gender || 'Not specified'}</p>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Medical History</label>
                {healthProfile.medical_history.length > 0 ? (
                  <div className="flex flex-wrap gap-2">
                    {healthProfile.medical_history.map((item, index) => (
                      <span key={index} className="badge badge-warning">{item}</span>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500 text-sm">No medical history recorded</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Current Medications</label>
                {healthProfile.medications.length > 0 ? (
                  <div className="flex flex-wrap gap-2">
                    {healthProfile.medications.map((item, index) => (
                      <span key={index} className="badge badge-success">{item}</span>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500 text-sm">No medications recorded</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Allergies</label>
                {healthProfile.allergies.length > 0 ? (
                  <div className="flex flex-wrap gap-2">
                    {healthProfile.allergies.map((item, index) => (
                      <span key={index} className="badge badge-danger">{item}</span>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500 text-sm">No allergies recorded</p>
                )}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Appointments */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Recent Appointments</h2>
        
        {appointments.length > 0 ? (
          <div className="space-y-4">
            {appointments.map((appointment) => (
              <div key={appointment.id} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-medium text-gray-900">{appointment.doctor_name}</h3>
                  <span className={`badge ${getStatusColor(appointment.status)}`}>
                    {appointment.status}
                  </span>
                </div>
                
                <div className="grid md:grid-cols-3 gap-4 text-sm text-gray-600">
                  <div className="flex items-center space-x-2">
                    <Calendar className="h-4 w-4" />
                    <span>{new Date(appointment.appointment_date).toLocaleDateString()}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Clock className="h-4 w-4" />
                    <span>{appointment.appointment_time}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <MapPin className="h-4 w-4" />
                    <span>Online Consultation</span>
                  </div>
                </div>

                {appointment.symptoms.length > 0 && (
                  <div className="mt-3">
                    <label className="block text-sm font-medium text-gray-700 mb-1">Symptoms</label>
                    <div className="flex flex-wrap gap-2">
                      {appointment.symptoms.map((symptom, index) => (
                        <span key={index} className="badge badge-secondary">{symptom}</span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <Calendar className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No appointments yet</h3>
            <p className="text-gray-600">Book your first appointment with a doctor</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Profile; 