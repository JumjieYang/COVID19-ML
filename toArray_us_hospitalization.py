#!/usr/local/bin/python3
import csv
import pandas as pd

csvfile = open('aggregated_cc_by.csv','r')
reader = csv.reader(csvfile)

csvfile_2 = open('aggregated_cc_by_us.csv','w')
writer = csv.writer(csvfile_2)

#only keep cases that have information of sub_region
for item in reader:
    if reader.line_num == 1:
        writer.writerow(item)
        continue
    if 'US-' in item[0]:
        writer.writerow(item)

#drop columns without information of hospitalized
f = pd.read_csv("aggregated_cc_by_us.csv")
kcol = ['open_covid_region_code','region_name', 'date','hospitalized_new','hospitalized_cumulative']
new_f = f[kcol]
new_f.to_csv("us_hospitalization.csv",index=False)

#trasfer csv to array 
data = pd.read_csv("us_hospitalization.csv",header=None)
list = data.values.tolist()
print(list[0])
print(list[1])




csvfile_2.close()
csvfile.close()
