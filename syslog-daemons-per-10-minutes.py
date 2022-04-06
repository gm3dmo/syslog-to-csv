#!/usr/bin/env python
# coding: utf-8

# # Syslog csv visualization
# 
# This script uses pandas to generate:
# 
# - Simple plot of of a syslog.csv. The csv file has been previously created by [syslog-to-csv.py](https://github.com/gm3dmo/syslog-to-csv/blob/main/syslog-to-csv.py)
# - Summary and count of the daemons which wrote to sylog in csv and markdown format.
# 

# In[ ]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pathlib
cwd = pathlib.Path.cwd()


# In[ ]:


pd.set_option('display.max_rows', 1000)
csv_file = cwd / 'syslog.csv'
df = pd.read_csv(csv_file)


# In[1]:


df.info()


# Create a pandas datetime column

# In[2]:


# Do conversions

# syslog = real_date
df['real_date'] = pd.to_datetime(df['unix_timestamp'],unit='s')
df.info()


# Create the *buckets*. We've chosen `600S` for the granularity of the bucket. Other frequencies can be chosen and are documented in the [offset-aliases](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases)

# In[4]:


buckets = df.groupby([pd.Grouper(key='real_date', axis=0, freq='600S'),'daemon']).count()


# In[5]:


buckets


# #### Which daemons are producing the most messages per 10 minutes?

# In[6]:


buckets_of_wiped_line = df.groupby([pd.Grouper(key='real_date', axis=0, freq='600S'),'daemon'])['wiped_line'].count().unstack()


# In[14]:


#buckets_of_wiped_line.plot()


# In[8]:


sns.lineplot(data = buckets_of_wiped_line)
plt.xticks(rotation=45)
plt.legend(title = "Lines written to syslog by daemon per 10 minutes", bbox_to_anchor=(1.05, 1))


# ### Generate summaries of the bucket data

# In[11]:


buckets_of_wiped_line.to_markdown('syslog-10-minute-breakdown.md')


# In[10]:


buckets_of_wiped_line.to_csv('syslog-10-minute-breakdown.csv')


# In[ ]:




