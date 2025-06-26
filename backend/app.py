from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
from datetime import datetime, timedelta
import json
import bcrypt
from dotenv import load_dotenv
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import numpy as np
from googletrans import Translator
import uuid
import joblib
import traceback
from rapidfuzz import process, fuzz

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Initialize extensions
jwt = JWTManager(app)
CORS(app)

# Initialize translator
translator = Translator()

# Mock database (in production, use MongoDB)
users_db = {}
doctors_db = {}
appointments_db = {}
health_records_db = {}

# Sample symptom-condition dataset
symptoms_data = {
    'fever': ['common_cold', 'flu', 'covid19', 'malaria'],
    'headache': ['migraine', 'tension_headache', 'sinusitis', 'hypertension'],
    'cough': ['common_cold', 'bronchitis', 'pneumonia', 'asthma'],
    'fatigue': ['anemia', 'depression', 'hypothyroidism', 'chronic_fatigue'],
    'nausea': ['food_poisoning', 'gastritis', 'migraine', 'pregnancy'],
    'chest_pain': ['angina', 'heart_attack', 'anxiety', 'costochondritis'],
    'abdominal_pain': ['appendicitis', 'gastritis', 'ulcer', 'gallstones'],
    'dizziness': ['vertigo', 'anemia', 'dehydration', 'inner_ear_problem'],
    'shortness_of_breath': ['asthma', 'anxiety', 'pneumonia', 'heart_problem'],
    'back_pain': ['muscle_strain', 'herniated_disc', 'kidney_stone', 'arthritis']
}

# Sample doctors data
sample_doctors = [
    {
        'id': 'doc1',
        'name': 'Dr. Sarah Johnson',
        'specialty': 'General Medicine',
        'experience': '15 years',
        'rating': 4.8,
        'available': True,
        'consultation_fee': 50
    },
    {
        'id': 'doc2',
        'name': 'Dr. Michael Chen',
        'specialty': 'Cardiology',
        'experience': '20 years',
        'rating': 4.9,
        'available': True,
        'consultation_fee': 80
    },
    {
        'id': 'doc3',
        'name': 'Dr. Priya Sharma',
        'specialty': 'Pediatrics',
        'experience': '12 years',
        'rating': 4.7,
        'available': True,
        'consultation_fee': 60
    }
]

# Initialize doctors database
for doctor in sample_doctors:
    doctors_db[doctor['id']] = doctor

# Supported languages
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'hi': 'Hindi',
    'te': 'Telugu',
    'ta': 'Tamil',
    'kn': 'Kannada',
    'bn': 'Bengali'
}

# Load trained model and columns
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'public_symptom_model.pkl')
DATASET_PATH = os.path.join(os.path.dirname(__file__), 'real_world_symptoms_synthetic_merged.csv')
try:
    model = joblib.load(MODEL_PATH)
    # Only use columns that are not 'prognosis', do not start with 'Unnamed:', and are numeric (symptoms/precautions)
    df = pd.read_csv(DATASET_PATH, nrows=1)
    exclude_cols = set(['prognosis', 'advice', 'severity', 'suggested_medication'])
    symptom_columns = [c.strip() for c in df.columns if c.strip() not in exclude_cols and not c.strip().startswith('Unnamed:') and pd.api.types.is_numeric_dtype(df[c])]
    class_names = model.classes_ if hasattr(model, 'classes_') else []
except Exception as e:
    print(f"Model loading error: {e}")
    model = None
    symptom_columns = []
    class_names = []

# Medical advice mapping for each disease
MEDICAL_ADVICE = {
    'Common Cold': {
        'immediate_action': [
            'Rest at home and drink plenty of fluids.',
            'You can use a humidifier to ease congestion.',
            'Wash your hands often to avoid spreading germs.'
        ],
        'home_remedies': ['Drink warm fluids.', 'Use saline nasal drops.'],
        'medications': ['Paracetamol for fever.', 'Decongestants if needed.'],
        'when_to_see_doctor': ['If symptoms last more than 10 days.', 'If you have trouble breathing.'],
        'emergency_signs': ['Severe shortness of breath.', 'Chest pain.']
    },
    'Flu': {
        'immediate_action': [
            'Stay in bed and rest as much as possible.',
            'Drink water and clear fluids to stay hydrated.',
            'Avoid contact with others to prevent spreading the flu.'
        ],
        'home_remedies': ['Warm soups.', 'Steam inhalation.'],
        'medications': ['Paracetamol for fever.', 'Antiviral drugs if prescribed.'],
        'when_to_see_doctor': ['High fever lasting more than 3 days.', 'Difficulty breathing.'],
        'emergency_signs': ['Bluish lips or face.', 'Severe chest pain.']
    },
    'Migraine': {
        'immediate_action': [
            'Lie down in a quiet, dark room.',
            'Drink water and avoid skipping meals.',
            'Use a cold pack on your forehead if it helps.'
        ],
        'home_remedies': ['Apply cold packs to forehead.', 'Practice relaxation techniques.'],
        'medications': ['Ibuprofen or acetaminophen.', 'Migraine-specific medications if prescribed.'],
        'when_to_see_doctor': ['If headaches are frequent or severe.', 'If you have vision changes.'],
        'emergency_signs': ['Sudden severe headache.', 'Weakness or numbness.']
    },
    'Chickenpox': {
        'immediate_action': [
            'Do not scratch the rash to avoid infection.',
            'Stay away from school or work until all blisters have crusted over.',
            'Keep fingernails trimmed short.'
        ],
        'home_remedies': ['Oatmeal baths.', 'Calamine lotion.'],
        'medications': ['Antihistamines for itching.', 'Acetaminophen for fever.'],
        'when_to_see_doctor': ['If rash spreads to eyes.', 'If you have trouble breathing.'],
        'emergency_signs': ['Difficulty breathing.', 'Persistent vomiting.']
    },
    'Food Poisoning': {
        'immediate_action': ['Drink oral rehydration solutions.', 'Rest.'],
        'home_remedies': ['Eat bland foods.', 'Avoid dairy and fatty foods.'],
        'medications': ['ORS for dehydration.', 'Antiemetics if prescribed.'],
        'when_to_see_doctor': ['If vomiting lasts more than 24 hours.', 'If you see blood in stool.'],
        'emergency_signs': ['Signs of dehydration.', 'High fever.']
    },
    'COVID-19': {
        'immediate_action': ['Isolate yourself.', 'Monitor oxygen levels.'],
        'home_remedies': ['Warm fluids.', 'Steam inhalation.'],
        'medications': ['Paracetamol for fever.', 'Consult doctor for antivirals.'],
        'when_to_see_doctor': ['If you have trouble breathing.', 'If symptoms worsen after 5 days.'],
        'emergency_signs': ['Severe shortness of breath.', 'Chest pain.']
    },
    'Strep Throat': {
        'immediate_action': ['Rest and drink fluids.', 'Avoid sharing utensils.'],
        'home_remedies': ['Warm salt water gargle.', 'Honey and lemon tea.'],
        'medications': ['Antibiotics if prescribed.', 'Pain relievers.'],
        'when_to_see_doctor': ['If sore throat lasts more than a week.', 'If you have a rash.'],
        'emergency_signs': ['Difficulty breathing.', 'Swelling of face or neck.']
    },
    'Allergies': {
        'immediate_action': ['Avoid allergens.', 'Rinse nose with saline.'],
        'home_remedies': ['Use air purifiers.', 'Shower after being outdoors.'],
        'medications': ['Antihistamines.', 'Nasal sprays.'],
        'when_to_see_doctor': ['If symptoms persist.', 'If you have wheezing.'],
        'emergency_signs': ['Severe shortness of breath.', 'Swelling of lips or tongue.']
    },
    'Dengue': {
        'immediate_action': ['Rest and drink fluids.', 'Monitor for bleeding.'],
        'home_remedies': ['Papaya leaf juice (folk remedy).'],
        'medications': ['Paracetamol for fever.', 'Avoid NSAIDs.'],
        'when_to_see_doctor': ['If you have severe abdominal pain.', 'If you see blood in vomit or stool.'],
        'emergency_signs': ['Severe bleeding.', 'Difficulty breathing.']
    },
    'Typhoid': {
        'immediate_action': ['Drink clean water.', 'Rest.'],
        'home_remedies': ['Eat soft, bland foods.'],
        'medications': ['Antibiotics as prescribed.', 'ORS for dehydration.'],
        'when_to_see_doctor': ['If high fever persists.', 'If you have confusion or delirium.'],
        'emergency_signs': ['Severe abdominal pain.', 'Persistent vomiting.']
    },
    'Malaria': {
        'immediate_action': ['Seek medical care for diagnosis.', 'Rest and hydrate.'],
        'home_remedies': ['None recommended.'],
        'medications': ['Antimalarial drugs as prescribed.'],
        'when_to_see_doctor': ['If fever returns after treatment.', 'If you have confusion.'],
        'emergency_signs': ['Seizures.', 'Severe anemia.']
    },
    'Asthma': {
        'immediate_action': ['Use inhaler as prescribed.', 'Sit upright and try to stay calm.'],
        'home_remedies': ['Avoid triggers.', 'Practice breathing exercises.'],
        'medications': ['Inhaled bronchodilators.', 'Steroids if prescribed.'],
        'when_to_see_doctor': ['If you need inhaler more than usual.', 'If symptoms wake you at night.'],
        'emergency_signs': ['Severe shortness of breath.', 'Bluish lips or face.']
    },
}

# Medical rules for severe diseases
SEVERE_DISEASE_RULES = {
    'Paralysis (brain hemorrhage)': [
        'weakness_in_limbs',
        'slurred_speech',
        'muscle_weakness',
        'loss_of_balance',
        'weakness_of_one_body_side'
    ],
    # Add more severe diseases and their required symptoms here
}

# Map user-friendly symptom names to dataset columns (updated to match synthetic dataset)
SYMPTOM_MAP = {
    'fever': ['fever'],
    'headache': ['headache'],
    'cough': ['cough'],
    'fatigue': ['fatigue'],
    'nausea': ['nausea'],
    'chest pain': ['chest_pain'],
    'abdominal pain': ['abdominal_pain'],
    'dizziness': ['dizziness'],
    'shortness of breath': ['shortness_of_breath'],
    'back pain': ['back_pain'],
    'sore throat': ['sore_throat'],
    'runny nose': ['runny_nose'],
    'muscle aches': ['muscle_aches'],
    'loss of appetite': ['loss_of_appetite'],
    'insomnia': ['insomnia'],
    'anxiety': ['anxiety'],
    'depression': ['depression'],
    'rash': ['rash'],
    'swelling': ['swelling'],
    'joint pain': ['joint_pain'],
    'vomiting': ['vomiting'],
    'diarrhoea': ['diarrhoea'],
    'constipation': ['constipation'],
    'weight loss': ['weight_loss'],
    'weight gain': ['weight_gain'],
    'high fever': ['high_fever'],
    'mild fever': ['mild_fever'],
    'breathlessness': ['breathlessness'],
    'pain behind the eyes': ['pain_behind_the_eyes'],
    'chills': ['chills'],
    'sweating': ['sweating'],
    'muscle weakness': ['muscle_weakness'],
    'blurred vision': ['blurred_vision'],
    'skin rash': ['skin_rash'],
    'itching': ['itching'],
    'ulcers on tongue': ['ulcers_on_tongue'],
    'burning micturition': ['burning_micturition'],
    'yellowish skin': ['yellowish_skin'],
    'dark urine': ['dark_urine'],
    'dehydration': ['dehydration'],
    'excessive hunger': ['excessive_hunger'],
    'facial pain': ['facial_pain'],
    'congestion': ['congestion'],
    'night sweats': ['night_sweats'],
    # Add more mappings as needed
}

# List of common diseases for generic symptoms
COMMON_DISEASES = set([
    'Common Cold', 'Flu', 'Viral Fever', 'Migraine', 'Allergy', 'Sinusitis', 'Gastroenteritis', 'Food Poisoning', 'Chicken pox', 'Typhoid', 'Dengue', 'Malaria', 'Bronchitis', 'Tension Headache', 'Seasonal Allergy', 'COVID-19', 'Strep Throat', 'Asthma', 'Pneumonia', 'Tonsillitis', 'Pharyngitis', 'Otitis Media', 'Conjunctivitis', 'Acute Bronchitis', 'Acute Sinusitis', 'Acute Gastroenteritis', 'Acute Pharyngitis', 'Acute Tonsillitis', 'Acute Otitis Media', 'Acute Conjunctivitis', 'Acute Bronchitis', 'Acute Sinusitis', 'Acute Gastroenteritis', 'Acute Pharyngitis', 'Acute Tonsillitis', 'Acute Otitis Media', 'Acute Conjunctivitis'
])
# List of generic symptoms
GENERIC_SYMPTOMS = set([
    'fever', 'high_fever', 'mild_fever', 'headache', 'cough', 'fatigue', 'nausea', 'chest pain', 'abdominal pain', 'dizziness', 'shortness of breath', 'back pain', 'sore throat', 'runny nose', 'muscle aches', 'loss of appetite', 'insomnia', 'anxiety', 'depression', 'rash', 'swelling', 'joint pain'
])

# Symptom-specific advice for high-risk symptoms
SYMPTOM_ADVICE = {
    'fever': 'For fever: Drink plenty of fluids and rest. Use a cool compress if needed.',
    'headache': 'For headache: Rest in a quiet, dark room and drink water.',
    'cough': 'For cough: Drink warm fluids and avoid irritants like smoke.',
    'fatigue': 'For fatigue: Get extra sleep and avoid overexertion.',
    'nausea': 'For nausea: Eat small, bland meals and sip clear fluids.',
    'chest pain': 'If you have chest pain, especially with shortness of breath or sweating, seek emergency care immediately.',
    'abdominal pain': 'For abdominal pain: Rest and avoid heavy meals. If pain is severe or persistent, see a doctor.',
    'dizziness': 'For dizziness: Sit or lie down until it passes. Stand up slowly.',
    'shortness of breath': 'If you have trouble breathing or feel breathless at rest, get medical help right away.',
    'back pain': 'For back pain: Rest, use a heating pad, and avoid heavy lifting.',
    'sore throat': 'For sore throat: Gargle with warm salt water and drink warm liquids.',
    'runny nose': 'For runny nose: Use tissues and wash your hands often.',
    'muscle aches': 'For muscle aches: Rest and use a warm compress.',
    'loss of appetite': 'For loss of appetite: Eat small, frequent meals.',
    'insomnia': 'For insomnia: Keep a regular sleep schedule and avoid screens before bed.',
    'anxiety': 'For anxiety: Practice deep breathing and relaxation techniques.',
    'depression': 'For depression: Talk to someone you trust and seek professional help if needed.',
    'rash': 'If your rash is spreading quickly or you have swelling of the face or tongue, get emergency help.',
    'swelling': 'For swelling: Elevate the affected area and apply a cold pack.',
    'joint pain': 'For joint pain: Rest the joint and use ice or heat as needed.',
    'vomiting': 'If you cannot keep fluids down or see blood in vomit, see a doctor as soon as possible.',
    'diarrhoea': 'For diarrhoea: Drink oral rehydration solutions and avoid dairy.',
    'constipation': 'For constipation: Eat fiber-rich foods and drink water.',
    'weight loss': 'For unexplained weight loss: See a doctor for evaluation.',
    'weight gain': 'For sudden weight gain: Monitor your diet and activity.',
    'high fever': 'For high fever: Take paracetamol and see a doctor if it persists.',
    'mild fever': 'For mild fever: Rest and drink fluids.',
    'breathlessness': 'If you feel breathless at rest, seek medical help immediately.',
    'pain behind the eyes': 'For pain behind the eyes: Rest and avoid bright lights.',
    'chills': 'For chills: Keep warm and rest.',
    'sweating': 'For sweating: Stay hydrated.',
    'muscle weakness': 'For muscle weakness: Rest and avoid strenuous activity.',
    'blurred vision': 'For blurred vision: Avoid driving and see a doctor if it persists.',
    'skin rash': 'For skin rash: Avoid scratching and use soothing lotions.',
    'itching': 'For itching: Use a cold compress and avoid irritants.',
    'ulcers on tongue': 'For mouth ulcers: Avoid spicy foods and use a saltwater rinse.',
    'burning micturition': 'For burning urination: Drink plenty of water and see a doctor if it persists.',
    'yellowish skin': 'For yellowish skin: See a doctor to check for jaundice.',
    'dark urine': 'For dark urine: Drink more water and see a doctor if it continues.',
    'dehydration': 'For dehydration: Drink oral rehydration solutions.',
    'excessive hunger': 'For excessive hunger: Monitor your blood sugar if diabetic.',
    'facial pain': 'For facial pain: Use a warm compress and rest.',
    'congestion': 'For congestion: Use steam inhalation and stay hydrated.',
    'night sweats': 'For night sweats: Keep your room cool and wear light clothing.'
}

def translate_text(text, target_lang='en'):
    """Translate text to target language"""
    try:
        if target_lang == 'en':
            return text
        result = translator.translate(text, dest=target_lang)
        return result.text
    except:
        return text

def analyze_symptoms(symptoms_list):
    """Analyze symptoms and return possible conditions"""
    conditions = {}
    
    for symptom in symptoms_list:
        symptom_lower = symptom.lower()
        for key, value in symptoms_data.items():
            if key in symptom_lower or symptom_lower in key:
                for condition in value:
                    if condition in conditions:
                        conditions[condition] += 1
                    else:
                        conditions[condition] = 1
    
    # Calculate confidence scores
    total_symptoms = len(symptoms_list)
    results = []
    
    for condition, count in conditions.items():
        confidence = min((count / total_symptoms) * 100, 95)
        results.append({
            'condition': condition.replace('_', ' ').title(),
            'confidence': round(confidence, 1),
            'severity': 'High' if confidence > 70 else 'Medium' if confidence > 40 else 'Low'
        })
    
    # Sort by confidence
    results.sort(key=lambda x: x['confidence'], reverse=True)
    return results[:5]  # Return top 5 conditions

def get_medical_advice(conditions, user_profile=None):
    """Generate medical advice based on conditions"""
    advice = {
        'immediate_action': [],
        'home_remedies': [],
        'medications': [],
        'when_to_see_doctor': [],
        'emergency_signs': []
    }
    
    for condition in conditions:
        condition_name = condition['condition'].lower()
        
        if 'covid' in condition_name:
            advice['immediate_action'].append('Get tested for COVID-19')
            advice['home_remedies'].append('Rest, stay hydrated, monitor symptoms')
            advice['when_to_see_doctor'].append('If symptoms worsen or breathing difficulties')
            advice['emergency_signs'].append('Difficulty breathing, chest pain, confusion')
        
        elif 'heart' in condition_name or 'angina' in condition_name:
            advice['immediate_action'].append('Seek immediate medical attention')
            advice['emergency_signs'].append('Chest pain, shortness of breath, arm pain')
        
        elif 'fever' in condition_name or 'flu' in condition_name:
            advice['home_remedies'].append('Rest, fluids, over-the-counter fever reducers')
            advice['medications'].append('Acetaminophen or Ibuprofen for fever')
            advice['when_to_see_doctor'].append('If fever persists for more than 3 days')
        
        elif 'headache' in condition_name:
            advice['home_remedies'].append('Rest in a quiet, dark room')
            advice['medications'].append('Over-the-counter pain relievers')
            advice['when_to_see_doctor'].append('If headache is severe or accompanied by other symptoms')
    
    return advice

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'MediVerse API is running'})

@app.route('/api/translate', methods=['POST'])
def translate():
    """Translate text to target language"""
    data = request.get_json()
    text = data.get('text', '')
    target_lang = data.get('target_lang', 'en')
    
    translated_text = translate_text(text, target_lang)
    return jsonify({'translated_text': translated_text})

@app.route('/api/symptoms/check', methods=['POST'])
def check_symptoms():
    data = request.get_json()
    symptoms = data.get('symptoms', [])
    language = data.get('language', 'en')
    age = data.get('age', None)
    gender = data.get('gender', None)

    print(f"Received symptoms: {symptoms}")
    print(f"Symptom columns: {symptom_columns}")

    # --- FUZZY MATCHING FOR USER SYMPTOMS ---
    # Use keys from SYMPTOM_MAP if available, else symptom_columns
    known_symptoms = list(SYMPTOM_MAP.keys()) if len(SYMPTOM_MAP) > 0 else symptom_columns
    mapped_symptoms = []
    for user_symptom in symptoms:
        match, score, _ = process.extractOne(user_symptom, known_symptoms, scorer=fuzz.ratio)
        if score >= 80:
            mapped_symptoms.append(match)
        else:
            mapped_symptoms.append(user_symptom)  # fallback to original if no good match
    symptoms = mapped_symptoms
    print(f"Fuzzy-mapped symptoms: {symptoms}")
    # --- END FUZZY MATCHING ---

    # Use ML model if available
    if model and symptom_columns:
        # Map user symptoms to dataset columns
        input_data = {col: 0 for col in symptom_columns}
        for user_symptom in symptoms:
            mapped = SYMPTOM_MAP.get(user_symptom, [user_symptom])
            for col in mapped:
                if col in input_data:
                    input_data[col] = 1
        input_df = pd.DataFrame([input_data])
        print(f"Input DataFrame for prediction:\n{input_df}")
        print(f"Model columns: {symptom_columns}")
        print(f"Model class names: {class_names}")
        print(f"Input DataFrame shape: {input_df.shape}")
        try:
            if hasattr(model, 'predict_proba'):
                probs = model.predict_proba(input_df)[0]
                print(f"Model probabilities: {probs}")
                top_indices = probs.argsort()[-3:][::-1]
                results = []
                for idx in top_indices:
                    results.append({
                        'condition': class_names[idx],
                        'probability': float(probs[idx])
                    })
                main_condition = results[0]['condition']
                top_prob = results[0]['probability']
                advice = MEDICAL_ADVICE.get(main_condition, {})
                # --- STRONGER GENERIC SYMPTOM LOGIC ---
                mapped_symptoms = set()
                for s in symptoms:
                    mapped_symptoms.update(SYMPTOM_MAP.get(s, [s]))
                # Always merge symptom-specific advice for all predictions
                emergency_alerts = advice.get('emergency_signs', []) if advice else []
                immediate_advice = advice.get('immediate_action', ['Drink water and rest.'])
                symptom_advice_list = []
                for user_symptom in symptoms:
                    if user_symptom in SYMPTOM_ADVICE:
                        advice_text = SYMPTOM_ADVICE[user_symptom]
                        if advice_text not in symptom_advice_list:
                            symptom_advice_list.append(advice_text)
                # Prepend all unique symptom-specific advice to immediate_advice
                for advice_text in reversed(symptom_advice_list):
                    if advice_text not in immediate_advice:
                        immediate_advice = [advice_text] + immediate_advice
                # --- END always merge symptom-specific advice ---
                if mapped_symptoms.issubset(GENERIC_SYMPTOMS):
                    # Only allow common diseases for generic symptoms
                    common_indices = [i for i, name in enumerate(class_names) if name in COMMON_DISEASES]
                    common_probs = [(class_names[i], probs[i]) for i in common_indices]
                    # Sort by probability descending
                    common_probs.sort(key=lambda x: x[1], reverse=True)
                    top_common = common_probs[:3]
                    norm_results = [
                        {'condition': top_common[i][0], 'probability': float(top_common[i][1])} for i in range(len(top_common))
                    ]
                    if not norm_results:
                        return {
                            'result': 'Not enough information for a confident prediction. Please provide more specific symptoms or consult a doctor.',
                            'top_conditions': [],
                            'medical_advice': {},
                            'advice_block': {}
                        }
                    main_condition = norm_results[0]['condition']
                    advice = MEDICAL_ADVICE.get(main_condition, {})
                    # Risk logic
                    risk = 'Low'
                    risk_icon = '🟢'
                    if age is not None:
                        try:
                            age_val = int(age)
                            # Age-specific advice for children and young adults (simple language)
                            if 1 <= age_val < 10:
                                if advice.get('immediate_action', []) and isinstance(advice['immediate_action'], list):
                                    advice['immediate_action'] = [
                                        'Make sure your child drinks water and gets plenty of rest.',
                                        'If your child feels worse or you are worried, call your doctor.'
                                    ] + advice['immediate_action']
                            elif 10 <= age_val < 18:
                                if advice.get('immediate_action', []) and isinstance(advice['immediate_action'], list):
                                    advice['immediate_action'] = [
                                        'Drink water, rest, and avoid heavy exercise.',
                                        'Tell an adult if you feel worse or have new symptoms.'
                                    ] + advice['immediate_action']
                            elif 18 <= age_val < 30:
                                if advice.get('immediate_action', []) and isinstance(advice['immediate_action'], list):
                                    advice['immediate_action'] = [
                                        'Drink water and rest as much as possible.',
                                        'If you feel very sick or your symptoms get worse, see a doctor.'
                                    ] + advice['immediate_action']
                            if age_val > 60:
                                risk = 'High'
                                risk_icon = '🔴'
                                if advice.get('immediate_action', []) and isinstance(advice['immediate_action'], list):
                                    advice['immediate_action'] = [
                                        'You may get sick more easily. Drink water, rest, and ask someone to check on you.',
                                        'If you feel worse or have trouble breathing, get medical help right away.'
                                    ] + advice['immediate_action']
                            elif age_val >= 40:
                                risk = 'Medium'
                                risk_icon = '🟡'
                                if advice.get('immediate_action', []) and isinstance(advice['immediate_action'], list):
                                    advice['immediate_action'] = [
                                        'Take it easy, drink water, and rest.',
                                        "If you don't feel better in a few days, talk to your doctor."
                                    ] + advice['immediate_action']
                        except:
                            pass
                    return {
                        'result': main_condition,
                        'top_conditions': norm_results,
                        'medical_advice': advice,
                        'advice_block': {
                            'age': age,
                            'gender': gender,
                            'immediate_advice': immediate_advice,
                            'risk': risk,
                            'risk_icon': risk_icon,
                            'emergency_alerts': emergency_alerts
                        }
                    }
                # --- END STRONGER GENERIC SYMPTOM LOGIC ---
                # If we reach here, return the top prediction as fallback
                return {
                    'result': main_condition,
                    'top_conditions': results,
                    'medical_advice': advice,
                    'advice_block': {
                        'age': age,
                        'gender': gender,
                        'immediate_advice': immediate_advice,
                        'risk': 'Low',
                        'risk_icon': '🟢',
                        'emergency_alerts': advice.get('emergency_signs', [])
                    }
                }
            else:
                prediction = model.predict(input_df)[0]
                advice = MEDICAL_ADVICE.get(prediction, {})
                return {'result': prediction, 'top_conditions': [], 'medical_advice': advice}
        except Exception as e:
            print(f"Prediction error: {e}")
            traceback.print_exc()
            return {'result': 'Prediction error', 'top_conditions': [], 'medical_advice': {}, 'error': str(e)}
    else:
        print("Model or symptom_columns not available!")
        return {'result': 'Model not available. Please contact admin.', 'error': 'Model not available.'}

@app.route('/api/auth/register', methods=['POST'])
def register():
    """User registration"""
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    
    if not all([email, password, name]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if email in users_db:
        return jsonify({'error': 'User already exists'}), 409
    
    # Hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Create user
    user_id = str(uuid.uuid4())
    users_db[email] = {
        'id': user_id,
        'email': email,
        'password': hashed_password,
        'name': name,
        'created_at': datetime.now().isoformat(),
        'health_profile': {
            'age': None,
            'gender': None,
            'medical_history': [],
            'medications': [],
            'allergies': []
        }
    }
    
    # Create access token
    access_token = create_access_token(identity=email)
    
    return jsonify({
        'message': 'User registered successfully',
        'access_token': access_token,
        'user': {
            'id': user_id,
            'email': email,
            'name': name
        }
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login"""
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')
    
    if not all([email, password]):
        return jsonify({'error': 'Missing email or password'}), 400
    
    user = users_db.get(email)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if not bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return jsonify({'error': 'Invalid password'}), 401
    
    # Create access token
    access_token = create_access_token(identity=email)
    
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': {
            'id': user['id'],
            'email': user['email'],
            'name': user['name']
        }
    })

@app.route('/api/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get user profile"""
    current_user_email = get_jwt_identity()
    user = users_db.get(current_user_email)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'user': {
            'id': user['id'],
            'email': user['email'],
            'name': user['name'],
            'health_profile': user['health_profile']
        }
    })

@app.route('/api/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
    current_user_email = get_jwt_identity()
    user = users_db.get(current_user_email)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    # Update health profile
    if 'health_profile' in data:
        user['health_profile'].update(data['health_profile'])
    
    return jsonify({
        'message': 'Profile updated successfully',
        'health_profile': user['health_profile']
    })

@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    """Get available doctors"""
    specialty = request.args.get('specialty')
    
    doctors = list(doctors_db.values())
    
    if specialty:
        doctors = [d for d in doctors if specialty.lower() in d['specialty'].lower()]
    
    return jsonify({'doctors': doctors})

@app.route('/api/appointments', methods=['POST'])
@jwt_required()
def book_appointment():
    """Book appointment with doctor"""
    current_user_email = get_jwt_identity()
    user = users_db.get(current_user_email)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    doctor_id = data.get('doctor_id')
    appointment_date = data.get('appointment_date')
    appointment_time = data.get('appointment_time')
    symptoms = data.get('symptoms', [])
    
    if not all([doctor_id, appointment_date, appointment_time]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    doctor = doctors_db.get(doctor_id)
    if not doctor:
        return jsonify({'error': 'Doctor not found'}), 404
    
    # Create appointment
    appointment_id = str(uuid.uuid4())
    appointment = {
        'id': appointment_id,
        'user_id': user['id'],
        'doctor_id': doctor_id,
        'doctor_name': doctor['name'],
        'appointment_date': appointment_date,
        'appointment_time': appointment_time,
        'symptoms': symptoms,
        'status': 'scheduled',
        'created_at': datetime.now().isoformat()
    }
    
    appointments_db[appointment_id] = appointment
    
    return jsonify({
        'message': 'Appointment booked successfully',
        'appointment': appointment
    }), 201

@app.route('/api/appointments', methods=['GET'])
@jwt_required()
def get_appointments():
    """Get user appointments"""
    current_user_email = get_jwt_identity()
    user = users_db.get(current_user_email)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    user_appointments = [
        apt for apt in appointments_db.values()
        if apt['user_id'] == user['id']
    ]
    
    return jsonify({'appointments': user_appointments})

@app.route('/api/languages', methods=['GET'])
def get_languages():
    """Get supported languages"""
    return jsonify({'languages': SUPPORTED_LANGUAGES})

@app.route('/api/symptoms/test_predict', methods=['GET'])
def test_predict():
    # Simulate a prediction with ['fever', 'headache']
    test_data = {'symptoms': ['fever', 'headache'], 'language': 'en'}
    with app.test_request_context(json=test_data):
        return check_symptoms()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 