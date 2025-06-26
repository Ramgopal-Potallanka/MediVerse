import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Stethoscope, 
  Brain, 
  Globe, 
  Shield, 
  Users, 
  Activity,
  ArrowRight,
  CheckCircle
} from 'lucide-react';

const Home = () => {
  const features = [
    {
      icon: Brain,
      title: 'AI Symptom Checker',
      description: 'Get instant analysis of your symptoms with our advanced AI technology'
    },
    {
      icon: Users,
      title: 'Connect with Doctors',
      description: 'Book appointments and get consultations with qualified healthcare professionals'
    },
    {
      icon: Globe,
      title: 'Multilingual Support',
      description: 'Available in 6 languages for better accessibility'
    },
    {
      icon: Shield,
      title: 'Secure & Private',
      description: 'Your health data is protected with end-to-end encryption'
    }
  ];

  const benefits = [
    'Instant symptom analysis',
    'Personalized medical advice',
    'Easy doctor booking',
    'Health record management',
    '24/7 availability',
    'No waiting in queues'
  ];

  return (
    <div className="space-y-16">
      {/* Hero Section */}
      <section className="text-center py-16">
        <div className="max-w-4xl mx-auto">
          <div className="flex justify-center mb-6">
            <Stethoscope className="h-16 w-16 text-primary-600" />
          </div>
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            Your Health, Our Priority
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Get instant medical guidance, connect with doctors, and manage your health 
            with our AI-powered platform. Available in multiple languages for everyone.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/symptoms"
              className="btn-primary text-lg px-8 py-3 flex items-center justify-center space-x-2"
            >
              <Activity className="h-5 w-5" />
              <span>Check Symptoms</span>
              <ArrowRight className="h-5 w-5" />
            </Link>
            <Link
              to="/doctors"
              className="btn-secondary text-lg px-8 py-3 flex items-center justify-center space-x-2"
            >
              <Users className="h-5 w-5" />
              <span>Find Doctors</span>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-white rounded-2xl shadow-sm">
        <div className="max-w-6xl mx-auto px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Why Choose MediVerse?
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              We combine cutting-edge AI technology with human expertise to provide 
              you with the best healthcare experience.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="text-center">
                <div className="flex justify-center mb-4">
                  <div className="p-3 bg-primary-100 rounded-full">
                    <feature.icon className="h-8 w-8 text-primary-600" />
                  </div>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-16">
        <div className="max-w-4xl mx-auto">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-6">
                Get Better Healthcare, Faster
              </h2>
              <p className="text-lg text-gray-600 mb-8">
                Skip the waiting room and get immediate medical guidance. Our AI-powered 
                platform helps you understand your symptoms and connects you with the 
                right healthcare professionals.
              </p>
              <div className="space-y-3">
                {benefits.map((benefit, index) => (
                  <div key={index} className="flex items-center space-x-3">
                    <CheckCircle className="h-5 w-5 text-medical-600 flex-shrink-0" />
                    <span className="text-gray-700">{benefit}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="bg-gradient-to-br from-primary-50 to-medical-50 p-8 rounded-2xl">
              <div className="text-center">
                <Stethoscope className="h-16 w-16 text-primary-600 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  Start Your Health Journey
                </h3>
                <p className="text-gray-600 mb-6">
                  Join thousands of users who trust MediVerse for their healthcare needs.
                </p>
                <Link
                  to="/register"
                  className="btn-primary w-full"
                >
                  Get Started Free
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-primary-600 rounded-2xl text-white">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-12">
            Trusted by Healthcare Professionals
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div>
              <div className="text-4xl font-bold mb-2">95%</div>
              <div className="text-primary-100">Accuracy Rate</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">50+</div>
              <div className="text-primary-100">Expert Doctors</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">10k+</div>
              <div className="text-primary-100">Happy Users</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="text-center py-16">
        <div className="max-w-2xl mx-auto">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Ready to Take Control of Your Health?
          </h2>
          <p className="text-lg text-gray-600 mb-8">
            Start your health journey today with MediVerse. Get instant symptom analysis 
            and connect with healthcare professionals.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/symptoms"
              className="btn-primary text-lg px-8 py-3"
            >
              Check Symptoms Now
            </Link>
            <Link
              to="/register"
              className="btn-secondary text-lg px-8 py-3"
            >
              Create Account
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home; 