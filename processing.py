import pandas as pd
import numpy as np

# load csv into pandas dataframe, we use online data for the best accuracy
search_trend_url ="https://raw.githubusercontent.com/google-research/open-covid-19-data/master/data/exports/search_trends_symptoms_dataset/United%20States%20of%20America/2020_US_weekly_symptoms_dataset.csv"
search_trend_df = pd.read_csv(search_trend_url)

# after loading the dataset to dataframe, we now first look at how many parameters do we have
print(len(search_trend_df.columns.values))

# since we have 430 parameters, let's have a look at the data, determine if can drop some of the columns
pd.set_option('expand_frame_repr', False)
print(search_trend_df.iloc[np.r_[0:10, -10:0]])

# since we have several NaN columns, we can drop the columns with null values to get better result
search_trend_df = search_trend_df.dropna(axis=1, how='all')
search_trend_df = search_trend_df.drop(['country_region_code', 'country_region', 'sub_region_1_code','sub_region_1'], axis=1)

# let's check the dataset again
print(search_trend_df.iloc[np.r_[0:10, -10:0]])

# we still see a lot NaNs, lets check number of NaNs in each column
print(search_trend_df.isnull().sum())

# # maybe need to drop several columns later
# cols_drop = []
# for col in search_trend_df.columns.values:
#     if search_trend_df[col].isnull().sum() > len(search_trend_df)/2:
#         cols_drop.append(col)
# # Briefly have a look at the columns need to be dropped.
# print(cols_drop)
# search_trend_df = search_trend_df.drop(cols,drop, axis=1)


# now, check the hospitalization cases, use the online data for best accuracy
hospitalization_url ="https://raw.githubusercontent.com/google-research/open-covid-19-data/master/data/exports/cc_by/aggregated_cc_by.csv"
hospitalization_df = pd.read_csv(hospitalization_url)

# let's have a look at hospitalization dataset
print(hospitalization_df)

# we only need data from US
hospitalization_df = hospitalization_df[hospitalization_df['open_covid_region_code'].str.contains('^US-')]

# check the dataset again
print(hospitalization_df)

# we only need hospitalized_new from this dataset, so we abandon unnecessary data
hospitalization_df = hospitalization_df[['open_covid_region_code', 'date', 'hospitalized_new']]

# have a look at the dataframe
print(hospitalization_df.iloc[np.r_[0:10, -10:0]])

# since the dataset is daily basis, but we need a weekly basis data, we need to resample the data to weekly basis
hospitalization_df['date'] = pd.to_datetime(hospitalization_df['date'], format='%Y-%m-%d')
hospitalization_df = hospitalization_df.groupby(['open_covid_region_code',]).resample('W', on='date',loffset='1d').sum()
hospitalization_df = hospitalization_df.reset_index()

# # In case the way above is not available(deprecated), we can use the method below
# hospitalization_df = hospitalization_df.set_index('date')
# hospitalization_df.index = hospitalization_df.index + pd.tseries.frequencies.to_offset('1d')
# hospitalization_df = hospitalization_df.reset_index()

# check the dataset again
print(hospitalization_df.iloc[np.r_[0:10, -10:0]])

# now we merge the datasets
search_trend_df['date'] = pd.to_datetime(search_trend_df['date'], format='%Y-%m-%d')
result = search_trend_df.merge(hospitalization_df, on=['open_covid_region_code', 'date'])
print(result)

# export to csv
result.to_csv('result.csv', index=False)


