import pandas as pd
import numpy as np
# load csv into pandas dataframe
search_trend_url ="https://raw.githubusercontent.com/google-research/open-covid-19-data/master/data/exports/search_trends_symptoms_dataset/United%20States%20of%20America/2020_US_weekly_symptoms_dataset.csv"
search_trend_df = pd.read_csv(search_trend_url)

# check how many parameters do we have
print(len(search_trend_df.columns.values))

# have a look at the dataframe
print(search_trend_df.iloc[np.r_[0:10, -10:0]])

# since we have several NaN columns, we can drop the columns with null values to get better result
search_trend_df = search_trend_df.dropna(axis=1, how='all')

# now, check the length of the parameters again
print(len(search_trend_df.columns.values))

# look at the dataframe again
print(search_trend_df.iloc[np.r_[0:10, -10:0]])

# now, we reduce 430 columns to 127 columns, then let's see if we can drop more
cols = search_trend_df.columns.values[:5]
pd.set_option('expand_frame_repr', False)
print(search_trend_df[cols].head(5))

# Since we are checking the data for US, and according to the data, we can drop merge 5 cols into one
search_trend_df = search_trend_df.drop(axis=1,columns=['country_region_code','country_region','sub_region_1','sub_region_1_code'])

# look at the dataframe again
cols = search_trend_df.columns.values[:5]
print(search_trend_df[cols].tail(5))

# # now, check number of nulls in each column
# print(search_trend_df.isnull().sum())
#
# # maybe need to drop several columns later
# cols_drop = []
# for col in search_trend_df.columns.values:
#     if search_trend_df[col].isnull().sum() > len(search_trend_df)/2:
#         cols_drop.append(col)
# print(cols_drop)



# now, check the hospitalization cases
hospitalization_url ="https://raw.githubusercontent.com/google-research/open-covid-19-data/master/data/exports/cc_by/aggregated_cc_by.csv"
hospitalization_df = pd.read_csv(hospitalization_url,parse_dates=['date'], engine = 'python')

# Since we need to merge these two datasets, we just need data from hospitalization_df matched with search_trend_df
hospitalization_df = hospitalization_df[hospitalization_df['open_covid_region_code'].str.contains('^US-')]
print(hospitalization_df)

# since we have several NaN columns, we can drop the columns with null values to get better result
hospitalization_df = hospitalization_df.dropna(axis=1, how='all')

# # have a look at the dataframe
print(hospitalization_df.iloc[np.r_[0:10, -10:0]])

# since we don't need region_name, we will drop this
hospitalization_df = hospitalization_df.drop(axis=1,columns=['region_name'])

# then we need to resample the data to weekly basis
hospitalization_df['date'] = pd.to_datetime(hospitalization_df['date'],format='%Y-%m-%d')
hospitalization_df = hospitalization_df.groupby(['open_covid_region_code',]).resample('W', on='date',loffset='1d').sum()
print(hospitalization_df)