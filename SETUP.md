# 🚀 MediVerse Setup Guide

This guide will help you set up and run the MediVerse application on your local machine.

## 📋 Prerequisites

Before you begin, make sure you have the following installed:

- **Node.js** (v16 or higher) - [Download here](https://nodejs.org/)
- **Python** (v3.8 or higher) - [Download here](https://www.python.org/downloads/)
- **Git** - [Download here](https://git-scm.com/)

## 🛠️ Installation Steps

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd medical
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env file with your configuration
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install Node.js dependencies
npm install
```

### 4. Environment Configuration

Create a `.env` file in the `backend` directory with the following variables:

```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production

# Database Configuration (for MongoDB)
MONGODB_URI=mongodb://localhost:27017/mediverse

# API Keys (optional for development)
GOOGLE_TRANSLATE_API_KEY=your-google-translate-api-key
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

## 🚀 Running the Application

### Option 1: Using the Startup Scripts

**Windows:**
```bash
start.bat
```

**macOS/Linux:**
```bash
chmod +x start.sh
./start.sh
```

### Option 2: Manual Startup

**Terminal 1 - Backend:**
```bash
cd backend
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

## 🌐 Accessing the Application

Once both servers are running:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **API Health Check**: http://localhost:5000/api/health

## 📱 Features Available

### 1. Symptom Checker
- Navigate to `/symptoms`
- Add multiple symptoms
- Get AI-powered analysis
- Receive medical advice

### 2. Doctor Booking
- Navigate to `/doctors`
- Browse available doctors
- Filter by specialty
- Book appointments

### 3. User Profile
- Register/Login at `/register` or `/login`
- Manage health profile
- View appointment history
- Update medical information

### 4. Multilingual Support
- Available in 6 languages
- Language selector in navigation
- Translated symptom analysis

## 🔧 Development

### Backend Development

The Flask backend includes:
- RESTful API endpoints
- JWT authentication
- Symptom analysis with AI
- Doctor management
- Appointment booking
- Multilingual support

### Frontend Development

The React frontend includes:
- Modern UI with Tailwind CSS
- Responsive design
- Form validation
- Real-time notifications
- Protected routes

## 🧪 Testing

### Backend Testing
```bash
cd backend
python -m pytest
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 📊 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login

### Symptoms
- `POST /api/symptoms/check` - Analyze symptoms
- `POST /api/translate` - Translate text

### Profile
- `GET /api/profile` - Get user profile
- `PUT /api/profile` - Update profile

### Doctors
- `GET /api/doctors` - Get available doctors

### Appointments
- `GET /api/appointments` - Get user appointments
- `POST /api/appointments` - Book appointment

## 🔒 Security Features

- JWT token authentication
- Password hashing with bcrypt
- CORS protection
- Input validation
- SQL injection prevention

## 🚨 Troubleshooting

### Common Issues

1. **Port already in use**
   - Change ports in configuration files
   - Kill existing processes

2. **Module not found errors**
   - Ensure virtual environment is activated
   - Reinstall dependencies

3. **CORS errors**
   - Check CORS configuration in backend
   - Verify frontend URL in backend config

4. **Database connection issues**
   - Ensure MongoDB is running
   - Check connection string

### Getting Help

If you encounter issues:
1. Check the console logs
2. Verify all dependencies are installed
3. Ensure all environment variables are set
4. Check network connectivity

## 📈 Performance Optimization

### Backend
- Enable caching for frequently accessed data
- Optimize database queries
- Use connection pooling

### Frontend
- Implement lazy loading
- Optimize bundle size
- Use React.memo for components

## 🚀 Deployment

### Backend Deployment
- Use Gunicorn for production
- Set up environment variables
- Configure reverse proxy (Nginx)

### Frontend Deployment
- Build production bundle: `npm run build`
- Serve static files
- Configure CDN

## 📝 License

This project is licensed under the MIT License.

---

**Happy coding! 🩺💻** 