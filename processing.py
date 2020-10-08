import pandas as pd
import numpy as np
# load csv into pandas dataframe
search_trend_df = pd.read_csv('2020_US_weekly_symptoms_dataset.csv')

# since we have several NaN columns, we can drop the columns with null values to get better result
search_trend_df = search_trend_df.dropna(axis=1, how='all')

# now, check the hospitalization cases
hospitalization_df = pd.read_csv('aggregated_cc_by.csv', parse_dates=['date'], engine='python')

# Since we need to merge these two datasets, we just need data from hospitalization_df matched with search_trend_df
hospitalization_df = hospitalization_df[hospitalization_df['open_covid_region_code'].str.contains('^US-')]

# since we have several NaN columns, we can drop the columns with null values to get better result
hospitalization_df = hospitalization_df[['open_covid_region_code', 'region_name', 'date', 'hospitalized_new']]
hospitalization_df = hospitalization_df.dropna(axis=0, how='all')

# then we need to resample the data to weekly basis
hospitalization_df['date'] = pd.to_datetime(hospitalization_df['date'], format='%Y-%m-%d')
hospitalization_df = hospitalization_df.groupby(['open_covid_region_code', ]).resample('W', on='date', loffset='1d', closed="left").sum()
print(hospitalization_df)
