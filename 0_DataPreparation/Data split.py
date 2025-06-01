import pandas as pd
from datetime import datetime

# Load the merged dataset from the first script
merged_df = pd.read_csv("0_DataPreparation/merged_output.csv")

# Convert Datum column to datetime if not already done
merged_df['Datum'] = pd.to_datetime(merged_df['Datum'])

# Define date ranges for splitting
train_start = datetime(2013, 7, 1)
train_end = datetime(2017, 7, 31)
val_start = datetime(2017, 8, 1)
val_end = datetime(2018, 7, 31)
test_start = datetime(2018, 8, 1)
test_end = datetime(2019, 7, 31)

# Split the dataset based on date ranges
train_set = merged_df[(merged_df['Datum'] >= train_start) & 
                      (merged_df['Datum'] <= train_end)].copy()

validation_set = merged_df[(merged_df['Datum'] >= val_start) & 
                          (merged_df['Datum'] <= val_end)].copy()

test_set = merged_df[(merged_df['Datum'] >= test_start) & 
                     (merged_df['Datum'] <= test_end)].copy()

# Display information about the splits
print("Dataset Split Summary:")
print("=" * 50)
print(f"Original dataset shape: {merged_df.shape}")
print(f"Date range: {merged_df['Datum'].min()} to {merged_df['Datum'].max()}")
print()

print(f"Training set shape: {train_set.shape}")
print(f"Training date range: {train_set['Datum'].min()} to {train_set['Datum'].max()}")
print(f"Training period: 01.07.2013 to 31.07.2017")
print()

print(f"Validation set shape: {validation_set.shape}")
print(f"Validation date range: {validation_set['Datum'].min()} to {validation_set['Datum'].max()}")
print(f"Validation period: 01.08.2017 to 31.07.2018")
print()

print(f"Test set shape: {test_set.shape}")
print(f"Test date range: {test_set['Datum'].min()} to {test_set['Datum'].max()}")
print(f"Test period: 01.08.2018 to 31.07.2019")
print()

# Check for any missing dates or gaps
total_expected_days = (test_end - train_start).days + 1
total_actual_days = len(train_set) + len(validation_set) + len(test_set)
print(f"Expected total days: {total_expected_days}")
print(f"Actual total days in splits: {total_actual_days}")

# Save the split datasets
train_set.to_csv("0_DataPreparation/train_set.csv", index=False)
validation_set.to_csv("0_DataPreparation/validation_set.csv", index=False)
test_set.to_csv("0_DataPreparation/test_set.csv", index=False)

print("\nDatasets saved:")
print("- Training set: '0_DataPreparation/train_set.csv'")
print("- Validation set: '0_DataPreparation/validation_set.csv'")
print("- Test set: '0_DataPreparation/test_set.csv'")

# Display first few rows of each set for verification
print("\n" + "="*50)
print("TRAINING SET - First 5 rows:")
print(train_set.head())

print("\n" + "="*50)
print("VALIDATION SET - First 5 rows:")
print(validation_set.head())

print("\n" + "="*50)
print("TEST SET - First 5 rows:")
print(test_set.head())

# Optional: Display some statistics about each dataset
print("\n" + "="*50)
print("DATASET STATISTICS:")
print("\nTraining Set Statistics:")
print(train_set.describe())

print("\nValidation Set Statistics:")
print(validation_set.describe())

print("\nTest Set Statistics:")
print(test_set.describe())