import React, { useState } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';
import { 
  Activity, 
  Brain, 
  Plus,
  X,
  Loader2
} from 'lucide-react';

const SymptomChecker = () => {
  const [symptoms, setSymptoms] = useState([]);
  const [currentSymptom, setCurrentSymptom] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('en');
  const [age, setAge] = useState('');
  const [gender, setGender] = useState('');

  const commonSymptoms = [
    'fever', 'headache', 'cough', 'fatigue', 'nausea', 'chest pain',
    'abdominal pain', 'dizziness', 'shortness of breath', 'back pain',
    'sore throat', 'runny nose', 'muscle aches', 'loss of appetite',
    'insomnia', 'anxiety', 'depression', 'rash', 'swelling', 'joint pain'
  ];

  const languages = {
    en: 'English',
    hi: 'हिंदी',
    te: 'తెలుగు',
    ta: 'தமிழ்',
    kn: 'ಕನ್ನಡ',
    bn: 'বাংলা'
  };

  const addSymptom = () => {
    if (currentSymptom.trim() && !symptoms.includes(currentSymptom.trim().toLowerCase())) {
      setSymptoms([...symptoms, currentSymptom.trim().toLowerCase()]);
      setCurrentSymptom('');
    }
  };

  const removeSymptom = (symptomToRemove) => {
    setSymptoms(symptoms.filter(symptom => symptom !== symptomToRemove));
  };

  const addCommonSymptom = (symptom) => {
    if (!symptoms.includes(symptom)) {
      setSymptoms([...symptoms, symptom]);
    }
  };

  const analyzeSymptoms = async () => {
    if (symptoms.length < 2) {
      toast.error('Please add at least 2 symptoms for analysis');
      return;
    }
    if (!age || !gender) {
      toast.error('Please enter your age and select gender');
      return;
    }
    setLoading(true);
    try {
      const response = await axios.post('/api/symptoms/check', {
        symptoms: symptoms,
        language: selectedLanguage,
        age: age,
        gender: gender
      });
      setAnalysis(response.data);
      if (
        response.data.result === 'Prediction error' ||
        response.data.result === 'Model not available. Please contact admin.'
      ) {
        toast.error(response.data.error || 'Failed to analyze symptoms');
      } else {
        toast.success('Analysis completed successfully!');
      }
    } catch (error) {
      toast.error(error.response?.data?.error || 'Failed to analyze symptoms');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center">
        <div className="flex justify-center mb-4">
          <Activity className="h-12 w-12 text-primary-600" />
        </div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          AI Symptom Checker
        </h1>
        <p className="text-gray-600">
          Describe your symptoms and get instant AI-powered analysis and medical advice
        </p>
      </div>

      {/* Age & Gender Fields Centered */}
      <div className="card flex flex-col items-center justify-center py-8 mb-4">
        <div className="flex flex-col items-center gap-6 w-full max-w-xs">
          <div className="w-full">
            <label className="text-sm font-medium text-gray-700 mb-1 block text-center">Age</label>
            <input
              type="number"
              min="0"
              max="120"
              value={age}
              onChange={e => setAge(e.target.value)}
              className="input-field w-full text-center"
              placeholder="Age"
            />
          </div>
          <div className="w-full">
            <label className="text-sm font-medium text-gray-700 mb-1 block text-center">Gender</label>
            <select
              value={gender}
              onChange={e => setGender(e.target.value)}
              className="input-field w-full text-center"
            >
              <option value="">Select</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
            </select>
          </div>
        </div>
      </div>

      {/* Symptom Input */}
      <h2 className="text-lg font-semibold text-gray-900 mb-4">
        Add Your Symptoms
      </h2>
      <div className="space-y-4">
        {/* Manual Input */}
        <div className="flex gap-2">
          <input
            type="text"
            value={currentSymptom}
            onChange={(e) => setCurrentSymptom(e.target.value)}
            placeholder="Enter a symptom (e.g., fever, headache)"
            className="input-field flex-1"
            onKeyPress={(e) => e.key === 'Enter' && addSymptom()}
          />
          <button
            onClick={addSymptom}
            className="btn-primary px-4"
          >
            <Plus className="h-4 w-4" />
          </button>
        </div>

        {/* Selected Symptoms */}
        {symptoms.length > 0 && (
          <div>
            <h3 className="text-sm font-medium text-gray-700 mb-2">Selected Symptoms:</h3>
            <div className="flex flex-wrap gap-2">
              {symptoms.map((symptom, index) => (
                <span
                  key={index}
                  className="badge badge-success flex items-center space-x-1"
                >
                  <span>{symptom}</span>
                  <button
                    onClick={() => removeSymptom(symptom)}
                    className="ml-1 hover:text-red-600"
                  >
                    <X className="h-3 w-3" />
                  </button>
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Common Symptoms */}
        <h3 className="text-sm font-medium text-gray-700 mb-2">Common Symptoms:</h3>
        <div className="flex flex-wrap gap-2">
          {commonSymptoms.map((symptom) => (
            <button
              key={symptom}
              onClick={() => addCommonSymptom(symptom)}
              disabled={symptoms.includes(symptom)}
              className={`badge ${
                symptoms.includes(symptom)
                  ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                  : 'bg-primary-100 text-primary-700 hover:bg-primary-200 cursor-pointer'
              }`}
            >
              {symptom}
            </button>
          ))}
        </div>

        {/* Analyze Button */}
        <div className="pt-4">
          <button
            onClick={analyzeSymptoms}
            disabled={symptoms.length < 2 || loading}
            className="btn-primary w-full flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <>
                <Loader2 className="h-5 w-5 animate-spin" />
                <span>Analyzing...</span>
              </>
            ) : (
              <>
                <Brain className="h-5 w-5" />
                <span>Analyze Symptoms</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Analysis Results */}
      {analysis && (
        <div className="space-y-6">
          {/* Most Likely Condition */}
          <div className="card">
            <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center space-x-2">
              <Brain className="h-5 w-5 text-primary-600" />
              <span>Most Likely Condition</span>
            </h2>
            <div className="mb-4">
              <span className="font-bold text-xl text-primary-700">{analysis.result}</span>
            </div>
            {/* Top 3 Conditions FIRST */}
            {Array.isArray(analysis.top_conditions) && analysis.top_conditions.length > 0 && (
              <div>
                <h3 className="text-md font-medium text-gray-800 mb-2">Top 3 Possible Conditions:</h3>
                <div className="space-y-2">
                  {analysis.top_conditions.map((cond, idx) => (
                    <div key={idx} className="border border-gray-200 rounded-lg p-3 flex items-center">
                      <span>{cond.condition}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
            {/* Advice Block */}
            {analysis.advice_block && (
              <div className="mb-4 flex flex-col gap-6">
                {/* Age & Gender Block */}
                <div className="bg-blue-50 rounded-2xl border border-blue-200 shadow p-6 flex flex-wrap gap-4 items-center">
                  <span className="inline-flex items-center px-3 py-1 rounded-full bg-blue-100 text-blue-800 font-semibold text-base">
                    <b>Age:</b> {analysis.advice_block.age || '-'}
                  </span>
                  <span className="inline-flex items-center px-3 py-1 rounded-full bg-blue-100 text-blue-800 font-semibold text-base">
                    <b>Gender:</b> {analysis.advice_block.gender || '-'}
                  </span>
                </div>
                {/* Risk Indicator Block */}
                <div className="bg-green-50 rounded-2xl border border-green-200 shadow p-6 flex items-center gap-3">
                  <b className="text-lg">Risk indicator:</b>
                  <span className={`inline-flex items-center px-2 py-1 rounded-full font-semibold text-base ${analysis.advice_block.risk === 'Low' ? 'bg-green-100 text-green-700' : analysis.advice_block.risk === 'Medium' ? 'bg-yellow-100 text-yellow-800' : 'bg-red-100 text-red-700'}`}>{analysis.advice_block.risk_icon} {analysis.advice_block.risk}</span>
                </div>
                {/* Immediate Advice Block */}
                <div className="bg-white rounded-2xl border border-blue-100 shadow p-6">
                  <div className="font-bold text-lg text-blue-900 mb-2">Immediate advice</div>
                  <ul className="list-disc ml-6 text-base text-gray-800 space-y-1">
                    {analysis.advice_block.immediate_advice.map((advice, idx) => (
                      <li key={idx}>{advice}</li>
                    ))}
                  </ul>
                </div>
                {/* Emergency Alerts Block */}
                {analysis.advice_block.emergency_alerts && analysis.advice_block.emergency_alerts.length > 0 && (
                  <div className="bg-red-50 rounded-2xl border border-red-200 shadow p-6">
                    <div className="font-bold text-lg text-red-700 mb-2 flex items-center gap-2">
                      <span>🚨 Emergency alerts:</span>
                    </div>
                    <ul className="list-disc ml-6 space-y-1">
                      {analysis.advice_block.emergency_alerts.map((alert, idx) => (
                        <li key={idx} className="text-red-700 font-medium">{alert}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>
          {/* Disclaimer */}
          <p className="text-sm text-yellow-800">
            <strong>Disclaimer:</strong> This analysis is for informational purposes only and should not replace professional medical advice. 
            Always consult with a healthcare provider for proper diagnosis and treatment.
          </p>
        </div>
      )}
    </div>
  );
};

export default SymptomChecker; 