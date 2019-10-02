#!/usr/bin/env python
# coding: utf-8

# Data Questions:
# 
# Steps:
# 1. Import data
# 2. Clean data
# 3. Output cleaned file
# 4. Import clean file
# 5. Import columns into new Panda dataframe
# 6. Analyse with the pd.describe() function
# 7. Plot some of the graphs 

# In[38]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import os


# First, need to import the data into python

# Data Dictionary
# 
# https://www.cdc.gov/nchs/data_access/vitalstatsonline.htm#Mortality_Multiple
# 
# MannerOfDeath = 2:Suicide
# 
# DeathDow = 
# 1:Sunday
# 2:Monday
# 3:Tuesday
# 4:Wednesday
# 5:Thursday
# 6:Friday
# 7:Saturday
# 
# DeathMonth:
# 10:October
# 11:November
# 12:December
# 01:January
# 02:February
# 03:March
# 04:April
# 05:May
# 06:June
# 07:July
# 08:August
# 09:September

# In[4]:


#read in the new data set again. 
newData = pd.read_csv("..\MiniProject1\Suicide.csv")


# In[23]:


#print summary statistics for the newData dataframe

print(newData.describe(),'\n','\n','\n', newData.head(),'\n','\n', 'The column names in the data are:{}'.format(list(newData)))


# In[5]:


print("The new dataframe is:",newData.shape[0], 'x', newData.shape[1])


# In[24]:


#want to perform the descriptive statistics on a single columns... lets create a function that pulls the column from a dataframe and calculates the mean, max, min)
#newData.isna().count()

#identified that the .csv has white spaces and needs to be removed
newData.columns = newData.columns.str.replace(' ', '') 

#view the head of the data to validate
newData.head()


# now need to use the new dataset and generate some descriptive statistics

# In[25]:


gender = newData.groupby('Sex').Age.count()
print('The following are the count of suicides for 2017 by', gender)


# In[26]:


#female = gender[0]
#male = gender[1]


# In[28]:


#(1) Create a new dataframe with just count of Age by Gender
analysis1 = newData.groupby(['Age','Sex'], sort=True).size().reset_index(name='Count')
#type(analysis1)
#analysis1_age = analysis1[['Age', 'Sex']]

#last two rows have values of 999, need them removed.
analysis1.drop(analysis1.tail(2).index,inplace=True)

#create a pivot table to plot against
analysis1 = pd.pivot_table(analysis1, index= 'Age', columns = 'Sex', aggfunc=sum)

#output dataframe to .csv file in local directory
analysis1.to_csv('analysis1.csv', sep=',', encoding='utf-8')
#analysis1


# Plot the age differences to view the similarities between males and females

# In[40]:


#analysis1.plot.bar(rot=0, subplots=True) <- plots both male and female in different graphs
analysis1_plot = analysis1.plot(title="Total Suicides by Age", use_index=False, figsize=(20,10))

#save the plot
fig = analysis1_plot.get_figure()
fig.savefig('../MiniProject1/analysis1_plot.png', transparent = False)


# 1B. What is the mean age for males and females suicide for 2017?

# In[107]:


male = newData.loc[(newData['Sex'] == ' M')]
male = male.groupby(['Age', 'DeathDoW'], sort=True).size().reset_index(name='Count')

#last 3 rows have age = 999, need removed
male.drop(male.tail(3).index,inplace=True)
male_mean = male['Age'].mean()

male_max = male['Age'].max()

print('The average male suicide age for 2017 is {} and the max age is {}.'.format(int(male_mean), male_max))


# In[112]:


female = newData.loc[(newData['Sex'] == ' F')]
female = female.groupby(['Age', 'DeathDoW'], sort=True).size().reset_index(name='Count')

#last 2 rows have age = 999, need removed
female.drop(female.tail(2).index,inplace=True)

female_min = female['Age'].min()

female_mean = female['Age'].mean()

female_max = female['Age'].max()

print('The minimum age is {}, the average for 2017 is {}, and the max age is {}.'.format(female_min, int(female_mean), female_max))


# #(2) How many suicides by day of the week?

# In[42]:


analysis2 = newData[['Age', 'Sex', 'DeathDoW']].sort_values('Age')


#analysis2 = newData.groupby(['Age','Sex', 'DeathDoW'], sort=True).size().reset_index(name='Count')


#need to remove the last 8 rows because age  = 999
analysis2.drop(analysis2.tail(8).index,inplace=True)

analysis2 = pd.pivot_table(analysis2, index= 'DeathDoW', columns = 'Sex', aggfunc='count')

#remove last row because there is no day 9, it is unknown
analysis2.drop(analysis2.tail(1).index,inplace=True)


analysis2_plot = analysis2.plot(title="Suicides by Day", use_index=False, figsize=(20,10))

analysis2.to_csv('analysis2.csv', sep=',', encoding='utf-8')

#save the plot
fig = analysis2_plot.get_figure()
fig.savefig('../MiniProject1/analysis2_plot.png', transparent = False)

print(analysis2_plot, analysis2)


# In[179]:


female_monday = analysis2.iloc[1,0]
male_monday = analysis2.iloc[1,1]

print('The day in 2017 with the most Suicides is Monday with {} female and {} male deaths.'.format(female_monday, male_monday))


# (3) What is the suicides by month count? 

# In[43]:


analysis3 = newData[['Age', 'Sex', 'DeathMonth']].sort_values('Age')

#analysis2 = newData.groupby(['Age','Sex', 'DeathDoW'], sort=True).size().reset_index(name='Count')


#need to remove the last 8 rows because age  = 999
analysis3.drop(analysis3.tail(8).index,inplace=True)

analysis3 = pd.pivot_table(analysis3, index= 'DeathMonth', columns = 'Sex', aggfunc='count')

analysis3_plot = analysis3.plot(title="Suicides by Day", use_index=False, figsize = (20,10))

analysis3.to_csv('analysis3.csv', sep=',', encoding='utf-8')

#save the plot
fig = analysis3_plot.get_figure()
fig.savefig('../MiniProject1/analysis3_plot.png', transparent = False)

print(analysis3_plot, analysis3)


# (4) What month to day combination resulsts in the highest suicides?

# In[6]:


analysis4 = newData[['Sex', 'DeathMonth', 'DeathDoW']]


analysis4 = newData.groupby(['Sex', 'DeathMonth', 'DeathDoW'], sort=True).size().reset_index(name='Count')

#need to remove the last 8 rows because age  = 999
#analysis4.drop(analysis3.tail(8).index,inplace=True)

analysis4 = pd.pivot_table(analysis4, index= 'DeathMonth', columns = ['Sex', 'DeathDoW'])


#plot the dataframe to see where the most values occur
analysis4_plot = analysis4.plot(title="Suicides by Death", use_index=False, kind = 'bar', figsize=(20,10))

#save the plot
fig = analysis4_plot.get_figure()
fig.savefig('../MiniProject1/analysis4_plot.png', transparent = False)

print(analysis4_plot, analysis4)


# In[44]:


# making boolean series for a team name 
#filter1 = analysis4.where["DeathMonth"]== 
analysis4.max()

analysis4['max_value'] = analysis4.max(axis=1)

analysis4.to_csv('analysis4.csv', sep=',', encoding='utf-8')

analysis4


# In[ ]:




