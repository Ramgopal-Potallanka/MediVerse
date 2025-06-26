import os
import pandas as pd

# Always use the directory of this script for file paths
script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, 'real_world_symptoms.csv')
output_file = os.path.join(script_dir, 'real_world_symptoms_cleaned.csv')

# Load the dataset
df = pd.read_csv(input_file)

# Remove rows with any missing or invalid data
cleaned_df = df.dropna()

# Optionally, remove duplicate rows (if any)
cleaned_df = cleaned_df.drop_duplicates()

# Remove classes with fewer than 3 samples
disease_counts = cleaned_df['prognosis'].value_counts()
valid_diseases = disease_counts[disease_counts >= 3].index
cleaned_df = cleaned_df[cleaned_df['prognosis'].isin(valid_diseases)]

# Save the cleaned dataset
cleaned_df.to_csv(output_file, index=False)

print(f"Cleaned dataset saved as {output_file}. Rows before: {len(df)}, after: {len(cleaned_df)}") 