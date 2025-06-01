import pandas as pd

# Load your uploaded test.csv
test_df = pd.read_csv("0_DataPreparation/test.csv")

# URLs for external data
umsatz_url = "https://raw.githubusercontent.com/opencampus-sh/einfuehrung-in-data-science-und-ml/main/umsatzdaten_gekuerzt.csv"
wetter_url = "https://raw.githubusercontent.com/opencampus-sh/einfuehrung-in-data-science-und-ml/main/wetter.csv"
kiwo_url = "https://raw.githubusercontent.com/opencampus-sh/einfuehrung-in-data-science-und-ml/main/kiwo.csv"

# Load external data
umsatz_df = pd.read_csv(umsatz_url)
wetter_df = pd.read_csv(wetter_url)
kiwo_df = pd.read_csv(kiwo_url)

# Preview column names to choose correct keys
print("Test columns:", test_df.columns.tolist())
print("Umsatz columns:", umsatz_df.columns.tolist())
print("Wetter columns:", wetter_df.columns.tolist())
print("KiWo columns:", kiwo_df.columns.tolist())

# For umsatz: Select only 'Datum' and 'Umsatz' columns (adjust column names as needed)
# Assuming the umsatz column is named 'Umsatz' - adjust if different
umsatz_subset = umsatz_df[['Datum', 'Umsatz']]  # Only keep Datum and Umsatz

# First merge: test_df with umsatz subset (only Umsatz variable added)
merged_df = pd.merge(test_df, umsatz_subset, on="Datum", how="left")

# Second merge: result with wetter_df (full join - all weather variables)
merged_df = pd.merge(merged_df, wetter_df, on="Datum", how="outer")

# Final merge: with kiwo_df (full join - all KiWo variables)
merged_df = pd.merge(merged_df, kiwo_df, on="Datum", how="outer")

# Optional: sort by date if Datum is a date column
merged_df['Datum'] = pd.to_datetime(merged_df['Datum'], errors='coerce')
merged_df = merged_df.sort_values('Datum')

# Show the final merged result
print("\nFinal merged dataframe shape:", merged_df.shape)
print("\nFinal columns:", merged_df.columns.tolist())
print("\nFirst few rows:")
print(merged_df.head())

# Save for inspection
merged_df.to_csv("0_DataPreparation/merged_output.csv", index=False)
print("\nMerged data saved to '0_DataPreparation/merged_output.csv'")