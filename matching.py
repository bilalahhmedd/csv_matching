# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np


'''
read file's first
'''

checkin_file = pd.read_csv('CheckIn.csv',dtype=object)
master_file = pd.read_csv('Mastersheet.csv')



# first of all merge status and Membership type columns of csv file

# merge column status and membership types as tmp
checkin_file['tmp'] = checkin_file[checkin_file.columns[3:5]].apply(lambda x: ' '.join(x.astype(str)), axis =1)


#drop columns from dataset
checkin_file=checkin_file.drop(['Status','Membership Type'], axis=1)

# replace all nan entries with empty string

# rename columns tmp to Membership Type
checkin_file = checkin_file.rename(columns = {'tmp':'Membership Type'},inplace = False)
checkin_file['Membership Type']=checkin_file['Membership Type'].replace('InActive 14 Day Pass','InActive 14 Day Member')
checkin_file['Membership Type']=checkin_file['Membership Type'].replace({'nan ':''},regex=True)
checkin_file['Membership Type']=checkin_file['Membership Type'].replace({'nan':''},regex=True)

checkin_file =checkin_file.sort_values(by= 'Email')

master_file = master_file.sort_values(by = 'Email')
master_file = master_file.rename(columns = {'Next Payment Date ':'Next Payment Date'},inplace=False)


checkin_file= checkin_file[master_file.columns]

checkin_file['Next Payment Date']=pd.to_datetime(checkin_file['Next Payment Date'],errors='coerce')
master_file['Next Payment Date']=pd.to_datetime(master_file['Next Payment Date'],errors='coerce')







'''
data clearning starts here
'''


# task 1 find entries with na emails in master file
master_na_email = master_file[master_file['Email'].isna()]

# now data frame with notna email 
master_is_email = master_file[master_file['Email'].notna()]
master_is_email = master_is_email[master_is_email['Email'] != " "]

master_is_email = master_is_email[master_is_email['Email'] != "Need email to add member in checkin"]


#	Need email to add member in checkin


master_is_email = master_is_email.sort_values(by='Email')

# reset index for both dataframes


master_file = master_file.rename(columns = {'Next Payment Date ':'Next Payment Date'},inplace=False)
master_is_email=master_is_email.reset_index(drop=True)
checkin_file = checkin_file.reset_index(drop=True)



#master_is_email.equals(checkin_file)
master_file = master_file.rename(columns = {'Next Payment Date ':'Next Payment Date'},inplace=False)


# now iterate thorugh both files
# find email which is available in master and not available in checkfile

master_email = master_is_email['Email']
checkin_email = checkin_file['Email']


# common emails for both series files
common_emails=np.intersect1d(master_is_email['Email'].values,checkin_file['Email'].values)



master_is_email=master_is_email.rename(columns={'Next Payment Date ':'Next Payment Date'})
matched = list()
matched_details = list()
unmatched = list()

checkin_file= checkin_file[master_is_email.columns]

for i,x in enumerate(master_email):
    cmp_cols = list()
    x_count=0
    for j, y in enumerate(checkin_email):
        if x ==y: # if x is equal to y
            result=list(master_is_email.loc(0)[i].str.lower()[:-1] == checkin_file.loc(0)[j].str.lower()[:-1])
            result.append(master_is_email.loc(0)[i][-1]==checkin_file.loc(0)[j][-1])
            matched_details.append({x:list(result)})
            x_count+=1
            
            print('count updated')
    if (x_count==0):
        unmatched.append(x)
    else:
        matched.append({x:x_count})
    print('value for '+x+' appended in tmp')
    

matched_1 = list()
unmatched_1 = list()

for i,x in enumerate(checkin_email):
    
    x_count=0
    for j, y in enumerate(master_email):
        if x ==y: # if x is equal to y
            x_count+=1
            print('count updated')
    if (x_count==0):
        unmatched_1.append(x)
    else:
        matched_1.append({x:x_count})
    print('value for '+x+' appended in tmp')
    

# let's see what can we do it








