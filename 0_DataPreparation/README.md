# Data Import and Preparation

## Overview
In the following, the import and data preparation are discussed in detail. The datasets were provided by the course organisation (KiWo, sales, and weather data). In the first step, the provided data was merged and imputed/cleaned. Then, categorical variables were identified and defined where it seemed reasonable. Many additional variables were defined – mainly just for entertainment purposes. In a final step, the data was prepared for further analysis by splitting it into training, validation, and test sets. These were stored as .csv files.

## Data Importing
The provided data was imported using the built-in functions from pandas, based on the links provided by opencampus.
```python
pd.read_csv(...)
```

The links can be accessed via:
+ umsatz_url = "https://raw.githubusercontent.com/opencampus-sh/einfuehrung-in-data-science-und-ml/main/umsatzdaten_gekuerzt.csv"
+ wetter_url = "https://raw.githubusercontent.com/opencampus-sh/einfuehrung-in-data-science-und-ml/main/wetter.csv"
+ kiwo_url = "https://raw.githubusercontent.com/opencampus-sh/einfuehrung-in-data-science-und-ml/main/kiwo.csv"

## Merging Data from different sources
In the first step, the Umsatz and Test data frames were concatenated, although this was probably not a necessary step. For this, we used the built-in functions from pandas:
```python
merged_df = pd.concat([umsatz_df, test_df], axis=0, ignore_index=True)
```
The actual merging was then performed by left-merging first the Wetter dataframe and then the Kiwo dataframe. As the key, we used the "Datum" column:
```python
merged_df = pd.merge(merged_df, wetter_df, on="Datum", how="left")
merged_df = pd.merge(merged_df, kiwo_df, on="Datum", how="left")
```


## Data Cleaning
Since the Kieler Woche dataset was missing the dates where there was no Kiwo, the column was mostly filled with Nans. To fix this and make Kiwo a cathegorical variable, the Nans were filled
```python
merged_df["KielerWoche"] = merged_df["KielerWoche"].fillna(0)
```

## Handling Missing Values
In the previous step of merging the dataframes, a lot of missing values were introduced to the merged_df. The reason for this is, that the datasets for Weather are not complete. First the index of the merged_df was set to the "Datum"-column. 
```python
merged_df = merged_df.set_index("Datum")
```
Then for the columns Temperatur, Windgeschwindigkeit and Bewoelkung, a temporal interpolation was used
```python
merged_df["Temperatur"] = merged_df["Temperatur"].interpolate(method="time")
merged_df["Windgeschwindigkeit"] = merged_df["Windgeschwindigkeit"].interpolate(method="time")
merged_df["Bewoelkung"] = merged_df["Bewoelkung"].interpolate(method="time")
```
Finally for the Wettercode-column, a forward fill / backward fill was used, because the wathercode is somewhat strangly encoded, where adjacend numbers can encode vastly differnet weathers.
```python
merged_df["Wettercode"] = merged_df["Wettercode"].fillna(method="ffill").fillna(method="bfill")
```
## Construction of New Variables
For the construction of new variables, we both decided to feature engineer our given variables and also to add new variables. 

The feature engineered variables are:
+ Sales_daily: Sums the total daily sales.
+ Avg_sales_per_group_month_weekday: The idea behind this was similar to what a skilled Bäckereifachverkäufer would intuitively tell the manager as a basic forecast. It’s based on memory from past years – how much of certain categories you typically sell in a certain month on a given weekday.

Additional variables are:
+ Holidays: Includes public holidays like Christmas etc. These were manually extended to also cover the days leading up to the holidays – as for most people, the day before the holiday often feels more like the holiday itself.
+ DAX: Used as a basic indicator of how well the German economy is doing.
+ Weekdays: There are cyclic pattern for the weekdays. Like buying new bread on mondays and treating yourselfs with a croissant on weekends
+ Sunhours: This feature represents the number of hours of sunshine per day
+ Fussball: This variable flags days with major football events such as the World Cup or European Championship.
+ Schulferien: Hardcoded school vacation periods were added, including winter, Easter, summer, autumn, and Christmas holidays.

# Data Transformation
Many columns were converted to cathegorical. These include: 
+ Wettercode: Converted to categorical because adjacent codes can represent vastly different weather conditions.
+ Holidays: Differentiates between important holidays like Easter and Christmas, and more common "Brückentag"-style holidays.
+ Wochentag: Weekdays were converted to capture recurring behavioral patterns.
+ Schulferien: Coded as categorical to reflect that some school holidays (e.g., summer or Christmas) are likely more impactful than others.
+ Datum: The column was converted to a datetime datatype, and the dataframe was sorted by date:
```python
merged_df["Datum"] = pd.to_datetime(merged_df["Datum"])
merged_df = merged_df.sort_values('Datum')
```
