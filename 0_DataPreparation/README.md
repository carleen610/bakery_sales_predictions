# Data Import and Preparation

## Overview

In the following, the import and data preparation steps are discussed in detail. The datasets were provided by the course organisation (KiWo, sales, and weather data).  

In the first step, the provided data was merged and cleaned/imputed. Then, categorical variables were identified and defined where it seemed reasonable.  

Many additional variables were created — mainly just for entertainment purposes.  

In a final step, the data was prepared for further analysis by splitting it into training, validation, and test sets. These were stored as `.csv` files.


## Data Importing
The provided data was imported using the built-in functions from `pandas`, based on the links provided by opencampus.
```python
pd.read_csv(...)
```

The links can be accessed via:
+ umsatz_url = "https://raw.githubusercontent.com/opencampus-sh/einfuehrung-in-data-science-und-ml/main/umsatzdaten_gekuerzt.csv"
+ wetter_url = "https://raw.githubusercontent.com/opencampus-sh/einfuehrung-in-data-science-und-ml/main/wetter.csv"
+ kiwo_url = "https://raw.githubusercontent.com/opencampus-sh/einfuehrung-in-data-science-und-ml/main/kiwo.csv"


## Merging the Data

In the first step, the `umsatz` and `test` DataFrames were concatenated — although this was probably not a necessary step. For this, we used the built-in functions from `pandas`:

```python
merged_df = pd.concat([umsatz_df, test_df], axis=0, ignore_index=True)
```

The actual merging was then performed by left-merging first the `wetter` DataFrame and then the `kiwo` DataFrame. As the key, we used the `"Datum"` column:

```python
merged_df = pd.merge(merged_df, wetter_df, on="Datum", how="left")
merged_df = pd.merge(merged_df, kiwo_df, on="Datum", how="left")
```


## Data Cleaning

Since the Kieler Woche dataset was missing the dates where there was no KiWo, the corresponding column was mostly filled with `NaN` values.  

To fix this and make `KielerWoche` a categorical variable, the `NaN`s were replaced with `0`:

```python
merged_df["KielerWoche"] = merged_df["KielerWoche"].fillna(0)
```


## Handling Missing Values

In the previous step of merging the DataFrames, a number of missing values were introduced into `merged_df`. The reason for this is that the weather dataset is not complete.  

First, the index of `merged_df` was set to the `"Datum"` column:

```python
merged_df = merged_df.set_index("Datum")
```

Then, for the columns `Temperatur`, `Windgeschwindigkeit`, and `Bewoelkung`, a temporal interpolation was applied:

```python
merged_df["Temperatur"] = merged_df["Temperatur"].interpolate(method="time")
merged_df["Windgeschwindigkeit"] = merged_df["Windgeschwindigkeit"].interpolate(method="time")
merged_df["Bewoelkung"] = merged_df["Bewoelkung"].interpolate(method="time")
```

Finally, for the `Wettercode` column, a forward fill / backward fill was used. This is because the weather code is somewhat strangely encoded — adjacent values can represent vastly different weather conditions:

```python
merged_df["Wettercode"] = merged_df["Wettercode"].fillna(method="ffill").fillna(method="bfill")
```

---

## Construction of New Variables

To enrich the dataset, we both engineered features from existing variables and added entirely new ones.

### Feature-engineered variables:
+ **Sales_daily**: Sums the total daily sales.
+ **Avg_sales_per_group_month_weekday**: Inspired by the kind of experience-based forecasting a skilled *Bäckereifachverkäufer* might do — estimating what typically sells in a given month on a particular weekday.

### Additional variables:
+ **Holidays**: Includes major public holidays like Christmas. These were manually extended to also cover the days before holidays, which often behave similarly.
+ **DAX**: A simple economic indicator reflecting the performance of the German stock index.
+ **Weekdays**: Captures cyclic behavior — e.g., buying fresh bread on Mondays or treating yourself to a croissant on the weekend.
+ **Sunhours**: Number of hours of sunshine per day.
+ **Fussball**: Flags major football events such as the World Cup or European Championship.
+ **Schulferien**: Hardcoded school holidays, including winter, Easter, summer, autumn, and Christmas breaks.

---

## Data Transformation

Several columns were converted to categorical variables:

+ **Wettercode**: Encoded as categorical because adjacent codes can represent very different weather conditions.
+ **Holidays**: Differentiates between major holidays (e.g., Easter, Christmas) and more minor ones (e.g., "Brückentage").
+ **Wochentag**: Converted to capture recurring weekly behavior.
+ **Schulferien**: Coded as categorical to reflect varying impacts (e.g., summer holidays likely have a stronger effect than autumn).
+ **Datum**: Converted to datetime and sorted to ensure temporal order:

```python
merged_df["Datum"] = pd.to_datetime(merged_df["Datum"])
merged_df = merged_df.sort_values("Datum")
```

merged_df = merged_df.sort_values('Datum')
```
