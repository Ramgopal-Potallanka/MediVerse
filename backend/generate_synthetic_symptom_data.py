import pandas as pd
import numpy as np

# Define symptoms and diseases
symptoms = [
    'fever', 'headache', 'cough', 'fatigue', 'nausea', 'chest_pain', 'abdominal_pain', 'dizziness',
    'shortness_of_breath', 'back_pain', 'sore_throat', 'runny_nose', 'muscle_aches', 'loss_of_appetite',
    'insomnia', 'anxiety', 'depression', 'rash', 'swelling', 'joint_pain', 'vomiting', 'diarrhoea',
    'constipation', 'weight_loss', 'weight_gain', 'high_fever', 'mild_fever', 'breathlessness',
    'pain_behind_the_eyes', 'chills', 'sweating', 'muscle_weakness', 'blurred_vision', 'skin_rash',
    'itching', 'ulcers_on_tongue', 'burning_micturition', 'yellowish_skin', 'dark_urine', 'dehydration'
]
diseases = [
    'Common Cold', 'Flu', 'Migraine', 'Chickenpox', 'Typhoid', 'Dengue', 'Malaria', 'Diabetes',
    'Hypertension', 'Asthma', 'Pneumonia', 'Gastroenteritis', 'Arthritis', 'Depression', 'Allergy',
    'Bronchitis', 'Sinusitis', 'Food Poisoning', 'Jaundice', 'Tuberculosis'
]

# Define symptom patterns for each disease (simplified, for demo)
disease_symptoms = {
    'Common Cold': ['fever', 'cough', 'sore_throat', 'runny_nose', 'fatigue'],
    'Flu': ['high_fever', 'cough', 'headache', 'muscle_aches', 'fatigue'],
    'Migraine': ['headache', 'nausea', 'vomiting', 'blurred_vision', 'insomnia'],
    'Chickenpox': ['fever', 'rash', 'itching', 'fatigue', 'headache'],
    'Typhoid': ['high_fever', 'abdominal_pain', 'headache', 'fatigue', 'constipation'],
    'Dengue': ['high_fever', 'rash', 'joint_pain', 'pain_behind_the_eyes', 'muscle_aches'],
    'Malaria': ['high_fever', 'chills', 'sweating', 'headache', 'nausea'],
    'Diabetes': ['weight_loss', 'fatigue', 'blurred_vision', 'excessive_hunger', 'dehydration'],
    'Hypertension': ['headache', 'dizziness', 'chest_pain', 'fatigue', 'blurred_vision'],
    'Asthma': ['shortness_of_breath', 'cough', 'chest_pain', 'fatigue', 'anxiety'],
    'Pneumonia': ['high_fever', 'cough', 'chest_pain', 'breathlessness', 'fatigue'],
    'Gastroenteritis': ['vomiting', 'diarrhoea', 'abdominal_pain', 'nausea', 'dehydration'],
    'Arthritis': ['joint_pain', 'swelling', 'fatigue', 'muscle_weakness', 'depression'],
    'Depression': ['depression', 'insomnia', 'fatigue', 'anxiety', 'weight_loss'],
    'Allergy': ['itching', 'rash', 'runny_nose', 'sore_throat', 'fatigue'],
    'Bronchitis': ['cough', 'chest_pain', 'fatigue', 'shortness_of_breath', 'mild_fever'],
    'Sinusitis': ['headache', 'facial_pain', 'runny_nose', 'congestion', 'fatigue'],
    'Food Poisoning': ['vomiting', 'diarrhoea', 'abdominal_pain', 'nausea', 'dehydration'],
    'Jaundice': ['yellowish_skin', 'dark_urine', 'fatigue', 'abdominal_pain', 'nausea'],
    'Tuberculosis': ['cough', 'weight_loss', 'fever', 'night_sweats', 'fatigue']
}

# Ensure all symptoms in disease_symptoms are in the symptoms list
for dsym in disease_symptoms.values():
    for s in dsym:
        if s not in symptoms:
            symptoms.append(s)

n_samples_per_disease = 15
rows = []
np.random.seed(42)
for disease in diseases:
    base_symptoms = disease_symptoms.get(disease, [])
    for _ in range(n_samples_per_disease):
        row = {sym: 0 for sym in symptoms}
        # Set base symptoms to 1
        for sym in base_symptoms:
            row[sym] = 1
        # Randomly add noise: flip 1-2 symptoms
        noise = np.random.choice(symptoms, size=np.random.randint(0, 3), replace=False)
        for n in noise:
            row[n] = 1 if row[n] == 0 else 0
        row['prognosis'] = disease
        rows.append(row)

# Create DataFrame and save
synthetic_df = pd.DataFrame(rows)
synthetic_df.to_csv('backend/real_world_symptoms_synthetic.csv', index=False)
print(f"Synthetic dataset saved as backend/real_world_symptoms_synthetic.csv with {len(synthetic_df)} rows and {len(synthetic_df.columns)} columns.") 