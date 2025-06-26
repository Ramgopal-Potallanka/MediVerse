# 🩺 MediVerse - AI-Powered Health Support Platform

## 📋 Project Overview

MediVerse is a comprehensive healthcare platform that leverages artificial intelligence and modern web technologies to provide users with symptom analysis, medical advice, and doctor consultation services. The platform features a multilingual interface supporting 6 Indian languages and uses a machine learning model to predict possible health conditions based on user-reported symptoms.

## ✨ Key Features

- 🤖 **AI Symptom Checker**: Analyze symptoms and get possible conditions using a trained ML model (Naive Bayes, 91.67% accuracy)
- 💊 **Medical Advice**: Personalized recommendations, home remedies, and emergency guidance
- 👨‍⚕️ **Doctor Booking**: Connect with healthcare professionals and book appointments
- 🌐 **Multilingual Support**: Available in English, Hindi, Telugu, Tamil, Kannada, and Bengali (Google Translate API)
- 📋 **Health Profile**: Store and manage health records
- 🔒 **Secure & Private**: JWT authentication, password encryption, and CORS protection

## 🛠️ Technology Stack

### Frontend
- **React.js 18.2.0**: UI library for building interactive interfaces
- **React Router DOM 6.3.0**: Routing for single-page applications
- **Tailwind CSS 3.3.2**: Utility-first CSS framework
- **Axios 1.4.0**: HTTP client for API requests
- **React Hook Form 7.45.4**: Form management and validation
- **React Hot Toast 2.4.1**: Toast notifications
- **Lucide React 0.263.1**: Icon toolkit

### Backend
- **Flask 2.3.3**: Python web framework
- **Flask-CORS 4.0.0**: Cross-origin resource sharing
- **Flask-JWT-Extended 4.5.3**: JWT authentication
- **Gunicorn 21.2.0**: WSGI HTTP server for deployment
- **python-dotenv 1.0.0**: Environment variable management

### Machine Learning & Data Science
- **Scikit-learn 1.3.0**: Machine learning (Naive Bayes classifier)
- **Pandas 2.0.3**: Data manipulation
- **NumPy 1.24.3**: Numerical computing
- **SciPy 1.15.3**: Scientific computing
- **Joblib 1.5.1**: Model serialization

### Database & Storage
- **MongoDB**: NoSQL database (planned/optional, mock DB in code)
- **PyMongo 4.5.0**: MongoDB driver for Python
- **GridFS**: File storage for large files

### External APIs & Services
- **Google Translate API**: Real-time translation
- **Twilio 8.8.0**: SMS and communication services
- **Googletrans 4.0.0**: Python wrapper for Google Translate

### Development & Testing
- **Jest**: JavaScript testing framework
- **React Testing Library**: React component testing
- **ESLint**: Linting and code quality
- **PostCSS 8.4.24**: CSS processing
- **Autoprefixer 10.4.14**: CSS vendor prefixing

## 📊 AI Model Performance

- **Test Accuracy**: 91.67%
- **Test Precision**: 91.25%
- **Test Recall**: 91.67%
- **Test F1-Score**: 91.43%
- **Cross-validated Accuracy**: 94.00% ± 2.49%
- **Supported Conditions**: 20+ diseases (Allergy, Asthma, Bronchitis, Chickenpox, COVID-19, Dengue, Diabetes, Flu, Food Poisoning, Hypertension, Malaria, Migraine, Pneumonia, Sinusitis, Tuberculosis, Typhoid, and more)

## 🏗️ Project Structure

```
medical/
├── frontend/                 # React.js frontend
│   ├── public/              # Static assets
│   │   ├── components/      # UI components
│   │   ├── contexts/        # React context providers
│   │   ├── pages/           # Page components
│   │   └── App.js           # Main app
│   ├── package.json         # Frontend dependencies
│   └── tailwind.config.js   # Tailwind CSS config
├── backend/                  # Flask backend
│   ├── app.py               # Main Flask app
│   ├── config.py            # Configurations
│   ├── venv/                # Python virtual environment
│   └── requirements.txt     # Python dependencies
├── public_symptom_model.pkl  # Trained ML model
├── model_metrics_report.txt  # Model performance
└── README.md                 # Project documentation
```

## 🚀 Getting Started

### Prerequisites
- Node.js (v16+)
- Python (v3.8+)
- MongoDB (optional, for production)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd medical
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
pip install -r requirements.txt
# Create .env file and add your configuration
```

### 3. Frontend Setup
```bash
cd ../frontend
npm install
# Create .env file if needed
```

### 4. Start the Application
```bash
# Terminal 1 - Backend
cd backend
python app.py
# Terminal 2 - Frontend
cd frontend
npm start
```

## 🌐 Supported Languages
- English
- Hindi
- Telugu
- Tamil
- Kannada
- Bengali

## 🔐 Security Features
- JWT Authentication
- Password encryption (bcrypt)
- CORS protection
- Input validation

## 🔧 API Endpoints (Backend)
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login user
- `GET /api/profile` - Get user profile (JWT required)
- `PUT /api/profile` - Update profile (JWT required)
- `POST /api/symptoms/check` - Analyze symptoms
- `GET /api/doctors` - List doctors
- `POST /api/appointments` - Book appointment (JWT required)
- `GET /api/appointments` - Get appointments (JWT required)
- `POST /api/translate` - Translate text
- `GET /api/languages` - List supported languages
- `GET /api/health` - Health check

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## 📄 License
This project is licensed under the MIT License.

---

**Built with ❤️ for better healthcare access** 