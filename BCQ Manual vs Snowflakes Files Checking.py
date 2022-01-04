#!/usr/bin/env python
# coding: utf-8

# In[351]:


#installing datacompy, a package that compares two dataframes/data tables through giving statistical output containing  
#similarities and differences between the two tables
#datacompy documentation : https://capitalone.github.io/datacompy/api/modules.html


# In[352]:


pip install datacompy


# In[353]:


import pandas as pd
import numpy as np
import sys
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 40)


# In[354]:


#read files - standard format would be pd.read_excel(r'file_loc')
df1 = pd.read_excel (r'C:\Users\johna\Downloads\BCQ_CleanupTestFiles\BGI BCQ Summary November 2021.xlsx')
#to choose specific columns/ range of columns use:
# df1 = pd.read_excel(file_loc, usecols = "A,C:AA") *file_loc should be your file path/ file location
# column range or use_cols can be (ex. "A:E", "A,E:F") as range will be inclusive of both sides
df2 = pd.read_csv(r'C:\Users\johna\Downloads\BCQ_CleanupTestFiles\NMMS_Snowflake_BGIBCQtotal.csv', index_col=False)


# In[355]:


df1


# In[356]:


#changing header of df1
header_row = 1
df1.columns = df1.iloc[header_row]
df1


# In[357]:


#drop first two rows
#N = number of rows
N = 2
df1 = df1.iloc[N: , :]
df1


# In[358]:


#Reset Index
df1 = df1.reset_index(drop=True)
df1


# In[359]:


#transpose dataframe
df1_transposed = df1.T # or df1.transpose()
df1_transposed


# In[360]:


#drop first two rows of transposed dataframe
N = 2
df1_transposed = df1_transposed.iloc[N: , :]
df1_transposed


# In[361]:


#labelling index
df1_transposed.index.name = 'CUSTOMER'
df1_transposed


# In[362]:


#get only last column which contains list of total bcq values of a customer
df1_transposed.drop(df1_transposed.iloc[:, 0:744], inplace = True, axis = 1)
df1_transposed


# In[363]:


df1_transposed.sort_index(ascending = False)
df1_transposed


# In[364]:


#rename column 744 to BCQ_TOTAL
df1_newtransposed =  df1_transposed.rename(columns={744: 'BCQ_TOTAL'})
df1_newtransposed


# In[365]:


#Manual File Totals
df1_newtransposed.sort_index(ascending = False)
df1_newtransposed


# In[366]:


df2


# In[367]:


#Set index of snowflake data to customer
df2.set_index("CUSTOMER", inplace = True)
df2


# In[368]:


#Snowflake  Totals
df2.sort_index(ascending = False)


# In[369]:


#import datacompy to compare two dataframes
import datacompy
compare = datacompy.Compare(
df1_newtransposed,
df2,
on_index = True, #You can also specify a list of columns
abs_tol=0.0001,
rel_tol=0,
ignore_spaces= False,
cast_column_names_lower=False,
df1_name= 'Manual',
df2_name= 'Snowflake')


# In[370]:


#comparison report
print(compare.report(sample_count= 100, column_count = 14))


# In[371]:


#write output to a text file (optional)
#change file name if writing another output
with open("NMMS_BGI_crossreferencing_bcqtotal.txt", "w") as report_file:
    print(compare.report(sample_count= 100, column_count = 14), file=report_file)
    report_file.close()


# In[372]:


#Return all rows with any columns that have a mismatch
#note df1 = Manual, df2 = Snowflake
compare.all_mismatch()


# In[373]:


#Get records/rows unique to df1/manual file data
df1_uniquerows = compare.df1_unq_rows 
df1_uniquerows


# In[374]:


#Get records/rows unique to df2/Snowflake Data
df2_uniquerows = compare.df2_unq_rows 
df2_uniquerows


# In[ ]:




