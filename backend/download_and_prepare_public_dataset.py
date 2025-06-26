import pandas as pd
import requests
import zipfile
import io

# Download the dataset from a public source (Kaggle Disease Prediction)
# If Kaggle API is not available, instruct user to download manually
url = 'https://github.com/akshat0007/Disease-Prediction-Using-Machine-Learning/raw/master/Training.csv'
try:
    print('Downloading public dataset...')
    df = pd.read_csv(url)
    # Clean column names
    df.columns = [c.strip().replace(' ', '_').replace('/', '_').lower() for c in df.columns]
    # Rename target column
    if 'prognosis' not in df.columns:
        df.rename(columns={df.columns[-1]: 'prognosis'}, inplace=True)
    # Save cleaned dataset
    df.to_csv('public_symptoms_dataset.csv', index=False)
    print('Public dataset saved as public_symptoms_dataset.csv')
except Exception as e:
    print('Failed to download automatically. Please download the dataset from Kaggle and place it as public_symptoms_dataset.csv in the backend directory.')
    print('Error:', e) 