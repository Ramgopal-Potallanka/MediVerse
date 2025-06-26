import pandas as pd

# Load both datasets
new_df = pd.read_csv('mediverse_251_to_307_updated.csv')
train_df = pd.read_csv('real_world_symptoms_synthetic.csv')

# Merge on all unique columns (union)
merged_df = pd.concat([train_df, new_df], ignore_index=True, sort=False)

# Remove duplicates
merged_df = merged_df.drop_duplicates()

# Save the merged dataset
merged_df.to_csv('real_world_symptoms_synthetic_merged.csv', index=False)

print(f"Merged dataset saved as real_world_symptoms_synthetic_merged.csv with {merged_df.shape[0]} rows and {merged_df.shape[1]} columns.") 