#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


df1= pd.read_csv(r"C:\Users\Admin\Downloads\Sales_September_2019.csv")
df2= pd.read_csv(r"C:\Users\Admin\Downloads\Sales_October_2019.csv")
df3= pd.read_csv(r"C:\Users\Admin\Downloads\Sales_November_2019.csv")
df4= pd.read_csv(r"C:\Users\Admin\Downloads\Sales_May_2019.csv")
df5= pd.read_csv(r"C:\Users\Admin\Downloads\Sales_March_2019.csv")
df6= pd.read_csv(r"C:\Users\Admin\Downloads\Sales_June_2019.csv")
df7= pd.read_csv(r"C:\Users\Admin\Downloads\Sales_July_2019.csv")
df8= pd.read_csv(r"C:\Users\Admin\Downloads\Sales_January_2019.csv")
df9= pd.read_csv(r"C:\Users\Admin\Downloads\Sales_February_2019.csv")
df10= pd.read_csv(r"C:\Users\Admin\Downloads\Sales_February_2019.csv")
df11= pd.read_csv(r"C:\Users\Admin\Downloads\Sales_December_2019.csv")
df12= pd.read_csv(r"C:\Users\Admin\Downloads\Sales_April_2019.csv")


# In[3]:


all_months_data=pd.concat([df1,df2,df3,df4,df5,df6,df7,df8,df9,df10,df11,df12])


# In[4]:


all_months_data.head()


# Cleaning the data - dropping rows with missing values

# In[5]:


cleaned_data=all_months_data.dropna()


# In[6]:


cleaned_data[cleaned_data.isna().any(axis=1)]


# In[7]:


cleaned_data.size/all_months_data.size #very less amount of data lost 


# In[8]:


cleaned_data


# In[9]:


cleaned_data.describe()


# What was the best month for sales? How much was earned that month?

# Adding month column

# In[10]:


cleaned_data['Month']=cleaned_data['Order Date'].str[0:2].astype(int)
##So checking or data


# In[11]:


cleaned_data=cleaned_data[cleaned_data['Order Date'].str[0:2]!='Or']
cleaned_data


# In[12]:


cleaned_data.size/all_months_data.size


# In[13]:


cleaned_data['Month']=cleaned_data['Order Date'].str[0:2].astype(int)


# In[14]:


cleaned_data.head()


# # What was the best month for sales? How much was earned that month?
# 

# In[15]:


cleaned_data['Quantity Ordered'].describe()
cleaned_data['Price Each'].describe()


# In[17]:


cleaned_data['Price Each']=pd.to_numeric(cleaned_data['Price Each'])
cleaned_data['Quantity Ordered']=pd.to_numeric(cleaned_data['Quantity Ordered'])


# In[18]:


cleaned_data['Total_Sales']=cleaned_data['Price Each']*cleaned_data['Quantity Ordered']


# In[19]:


results=cleaned_data.groupby('Month').sum()
results
#results['Total_Sales'].max()


# In[26]:


import matplotlib.pyplot as plt
months=range(1,13)
plt.bar(months,results['Total_Sales'])


# In[29]:


# So the best month for Sales was December and 4613443.34 was the amount of Total Sales earned that month


# # Which city had the highest number of Sales

# In[27]:


cleaned_data['City']=cleaned_data['Purchase Address'].apply(lambda x:x.split(',')[1])


# In[28]:


cleaned_data['City']


# In[29]:


grpd_city_data=cleaned_data.groupby('City').sum('Total_Sales')
grpd_city_data
grpd_city_data[grpd_city_data['Total_Sales']==grpd_city_data['Total_Sales'].max()]


# # Hence San Francisco is the city with the highest total sales.

# # What time should we display advertisements to maximize the likelihood of customer's buying product.

# Extracting hr from order date

# In[30]:


cleaned_data['Order Date']=pd.to_datetime(cleaned_data['Order Date'])


# In[31]:


cleaned_data['Hour'] = cleaned_data['Order Date'].dt.hour
cleaned_data.groupby('Hour').count()


# In[47]:


plt.plot(range(0,24),cleaned_data.groupby('Hour').count()['Order ID'])


# # Hence u can see that at 19 (7 pm) the order are maximum and the second hr at which max orders were placed is 11 am 
# Hence at 11 am or 7 pm we should display advertisements to maximize the likelihood of customer's buying product.
# 

# # What products are mostly sold together?

# 
# To see if duplicate order ids are there or not

# In[33]:


df=cleaned_data[cleaned_data['Order ID'].duplicated(keep=False)]
df


# In[34]:


df['All Products']=df.groupby('Order ID')['Product'].transform(lambda x:",".join(x))


# In[35]:


df


# In[36]:


df =df[['Order ID','All Products']].drop_duplicates()


# In[37]:


df.head(100)


# In[38]:


df['All Products'].value_counts()


# In[39]:


from itertools import combinations
from collections import Counter
count=Counter()
for row in df['All Products']:
    row_list=row.split(",")
    count.update(Counter(combinations(row_list,2)))
for key,value in count.most_common(10):
    print(key,value)


# # Hence , we can say that 'Google Phone', 'USB-C Charging Cable' are sold most together

# In[40]:


cleaned_data.groupby('Product')['Quantity Ordered'].sum().sort_values(ascending=False)


# # Hence , we can say that 'AAA Batteries (4-pack)' is the product which is sold most in the year 2019

# # To determine why it is sold most , we can plot a graph of prices , quantity ordered for each product 

# In[41]:


productgrp= cleaned_data.groupby('Product')
quantity_ordered=productgrp['Quantity Ordered'].sum()

products = [pair for pair, df in productgrp]
plt.bar(products, quantity_ordered)
plt.xticks(products, rotation='vertical', size=8)
plt.show()




# In[42]:


quantity_ordered


# In[43]:


prices=productgrp['Price Each'].mean()
prices


# In[46]:


fig,ax1=plt.subplots()
ax2=ax1.twinx()
ax1.bar(products,quantity_ordered)
ax2.plot(products,prices)
ax1.bar(products, quantity_ordered, color='g')
ax2.plot(products, prices, color='b')

ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered', color='g')
ax2.set_ylabel('Price ($)', color='b')
ax1.set_xticklabels(products, rotation='vertical', size=8)
fig.show()


# # Since the prices of AA Batteries is very low (i.e., since it seems to be the cheapest product among all) most of the people could easily afford it . This could possibly one reason for it to be the most selling product. Also , the avg lifespan of AA battery is usually less than the other mentioned electronic products , so it is a frequently purchased product and this could be another reason for it to be most selling product.

# In[ ]:





# In[ ]:




