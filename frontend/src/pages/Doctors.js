import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import axios from 'axios';
import toast from 'react-hot-toast';
import { 
  Users, 
  Star, 
  Calendar, 
  Clock, 
  MapPin, 
  Filter,
  Search,
  User,
  Phone,
  Mail,
  Award,
  Loader2,
  X
} from 'lucide-react';

const Doctors = () => {
  const { user } = useAuth();
  const [doctors, setDoctors] = useState([]);
  const [filteredDoctors, setFilteredDoctors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedSpecialty, setSelectedSpecialty] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [showBookingModal, setShowBookingModal] = useState(false);
  const [selectedDoctor, setSelectedDoctor] = useState(null);
  const [bookingForm, setBookingForm] = useState({
    appointment_date: '',
    appointment_time: '',
    symptoms: ''
  });

  const specialties = [
    'All Specialties',
    'General Medicine',
    'Cardiology',
    'Pediatrics',
    'Dermatology',
    'Orthopedics',
    'Neurology',
    'Psychiatry',
    'Gynecology',
    'Ophthalmology'
  ];

  useEffect(() => {
    fetchDoctors();
  }, []);

  useEffect(() => {
    filterDoctors();
  }, [doctors, selectedSpecialty, searchTerm]);

  const fetchDoctors = async () => {
    try {
      const response = await axios.get('/api/doctors');
      setDoctors(response.data.doctors);
    } catch (error) {
      toast.error('Failed to fetch doctors');
    } finally {
      setLoading(false);
    }
  };

  const filterDoctors = () => {
    let filtered = [...doctors];

    // Filter by specialty
    if (selectedSpecialty && selectedSpecialty !== 'All Specialties') {
      filtered = filtered.filter(doctor => 
        doctor.specialty.toLowerCase().includes(selectedSpecialty.toLowerCase())
      );
    }

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(doctor =>
        doctor.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        doctor.specialty.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    setFilteredDoctors(filtered);
  };

  const handleBooking = (doctor) => {
    if (!user) {
      toast.error('Please login to book an appointment');
      return;
    }
    setSelectedDoctor(doctor);
    setShowBookingModal(true);
  };

  const handleBookingSubmit = async (e) => {
    e.preventDefault();
    
    if (!bookingForm.appointment_date || !bookingForm.appointment_time) {
      toast.error('Please select date and time');
      return;
    }

    try {
      const response = await axios.post('/api/appointments', {
        doctor_id: selectedDoctor.id,
        appointment_date: bookingForm.appointment_date,
        appointment_time: bookingForm.appointment_time,
        symptoms: bookingForm.symptoms.split(',').map(s => s.trim()).filter(s => s)
      });

      toast.success('Appointment booked successfully!');
      setShowBookingModal(false);
      setSelectedDoctor(null);
      setBookingForm({
        appointment_date: '',
        appointment_time: '',
        symptoms: ''
      });
    } catch (error) {
      toast.error(error.response?.data?.error || 'Failed to book appointment');
    }
  };

  const renderStars = (rating) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;

    for (let i = 0; i < fullStars; i++) {
      stars.push(<Star key={i} className="h-4 w-4 fill-yellow-400 text-yellow-400" />);
    }

    if (hasHalfStar) {
      stars.push(<Star key="half" className="h-4 w-4 fill-yellow-400 text-yellow-400" />);
    }

    const emptyStars = 5 - Math.ceil(rating);
    for (let i = 0; i < emptyStars; i++) {
      stars.push(<Star key={`empty-${i}`} className="h-4 w-4 text-gray-300" />);
    }

    return stars;
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Loader2 className="h-8 w-8 animate-spin text-primary-600" />
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center">
        <div className="flex justify-center mb-4">
          <Users className="h-12 w-12 text-primary-600" />
        </div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Find Your Doctor
        </h1>
        <p className="text-gray-600">
          Connect with qualified healthcare professionals for consultations and appointments
        </p>
      </div>

      {/* Filters */}
      <div className="card">
        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Search Doctors
            </label>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search by name or specialty..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="input-field pl-10"
              />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Specialty
            </label>
            <select
              value={selectedSpecialty}
              onChange={(e) => setSelectedSpecialty(e.target.value)}
              className="input-field"
            >
              {specialties.map((specialty) => (
                <option key={specialty} value={specialty}>{specialty}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Doctors Grid */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredDoctors.map((doctor) => (
          <div key={doctor.id} className="card hover:shadow-lg transition-shadow">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center space-x-3">
                <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center">
                  <User className="h-6 w-6 text-primary-600" />
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900">{doctor.name}</h3>
                  <p className="text-sm text-gray-600">{doctor.specialty}</p>
                </div>
              </div>
              <div className="flex items-center space-x-1">
                {renderStars(doctor.rating)}
                <span className="text-sm text-gray-600 ml-1">({doctor.rating})</span>
              </div>
            </div>

            <div className="space-y-2 mb-4">
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <Award className="h-4 w-4" />
                <span>{doctor.experience} experience</span>
              </div>
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <MapPin className="h-4 w-4" />
                <span>Online Consultation</span>
              </div>
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <span className="font-medium text-green-600">${doctor.consultation_fee}</span>
                <span>consultation fee</span>
              </div>
            </div>

            <div className="flex items-center justify-between">
              <span className={`badge ${doctor.available ? 'badge-success' : 'badge-warning'}`}>
                {doctor.available ? 'Available' : 'Busy'}
              </span>
              <button
                onClick={() => handleBooking(doctor)}
                disabled={!doctor.available}
                className="btn-primary text-sm disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Book Appointment
              </button>
            </div>
          </div>
        ))}
      </div>

      {filteredDoctors.length === 0 && (
        <div className="text-center py-12">
          <Users className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No doctors found</h3>
          <p className="text-gray-600">Try adjusting your search criteria</p>
        </div>
      )}

      {/* Booking Modal */}
      {showBookingModal && selectedDoctor && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900">Book Appointment</h2>
              <button
                onClick={() => setShowBookingModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="h-6 w-6" />
              </button>
            </div>

            <div className="mb-4">
              <h3 className="font-medium text-gray-900">{selectedDoctor.name}</h3>
              <p className="text-sm text-gray-600">{selectedDoctor.specialty}</p>
            </div>

            <form onSubmit={handleBookingSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Appointment Date
                </label>
                <input
                  type="date"
                  value={bookingForm.appointment_date}
                  onChange={(e) => setBookingForm({...bookingForm, appointment_date: e.target.value})}
                  min={new Date().toISOString().split('T')[0]}
                  className="input-field"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Appointment Time
                </label>
                <select
                  value={bookingForm.appointment_time}
                  onChange={(e) => setBookingForm({...bookingForm, appointment_time: e.target.value})}
                  className="input-field"
                  required
                >
                  <option value="">Select time</option>
                  <option value="09:00">9:00 AM</option>
                  <option value="10:00">10:00 AM</option>
                  <option value="11:00">11:00 AM</option>
                  <option value="14:00">2:00 PM</option>
                  <option value="15:00">3:00 PM</option>
                  <option value="16:00">4:00 PM</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Symptoms (optional)
                </label>
                <textarea
                  value={bookingForm.symptoms}
                  onChange={(e) => setBookingForm({...bookingForm, symptoms: e.target.value})}
                  placeholder="Describe your symptoms..."
                  className="input-field"
                  rows="3"
                />
              </div>

              <div className="flex space-x-3">
                <button
                  type="button"
                  onClick={() => setShowBookingModal(false)}
                  className="btn-secondary flex-1"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn-primary flex-1"
                >
                  Book Appointment
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Doctors; 