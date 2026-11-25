#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("employee_data.csv")
df.head()


# In[29]:


numeric_cols = ['Age', 'Salary', 'Performance_Rating']
summary = df[numeric_cols].agg([
    'mean',
    'median',
    'min',
    'max',
    'std'
])
print(summary)


# In[30]:


department_analysis = df.groupby('Department').agg(
    Average_Salary=('Salary', 'mean'),
    Minimum_Salary=('Salary', 'min'),
    Maximum_Salary=('Salary', 'max'),
    Employee_Count=('Salary', 'count')
)
print(department_analysis)


# In[31]:


city_analysis = df.groupby('City').agg(
    Average_Salary=('Salary', 'mean'),
    Average_Age=('Age', 'mean'),
    Employee_Count=('Salary', 'count')
)
print(city_analysis)


# In[32]:


gender_analysis = df.groupby('Gender').agg(
    Average_Salary=('Salary', 'mean'),
    Median_Salary=('Salary', 'median'),
    Employee_Count=('Salary', 'count')
)
print(gender_analysis)


# In[33]:


contract_analysis = df.groupby('Performance_Rating').agg(
    Average_Salary=('Salary', 'mean'),
    Average_Experience=('Age', 'mean'),
    Employee_Count=('Salary', 'count')
)

print(contract_analysis)


# In[34]:


corr_matrix = df[numeric_cols].corr()
print(corr_matrix)


# In[35]:


corr_pairs = corr_matrix.where(
    np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
)
top_3 = corr_pairs.stack().sort_values(
    key=abs,
    ascending=False
).head(3)
print("Top 3 Correlation Relationships:")
print(top_3)


# In[36]:


# Question 1: Which department has the highest average salary?

dept_salary = df.groupby('Department')['Salary'].mean()
highest_dept = dept_salary.idxmax()
highest_salary = dept_salary.max()

print("Question 1: Which department has the highest average salary?")
print("Answer:", highest_dept)
print("Average Salary:", round(highest_salary, 2))


# In[37]:


# Question 2: Which city has the highest number of employees?

city_count = df['City'].value_counts()
highest_city = city_count.idxmax()
employee_count = city_count.max()

print("Question 2: Which city has the highest number of employees?")
print("Answer:", highest_city)
print("Number of Employees:", employee_count)


# In[38]:


# Question 3: What is the average salary of male and female employees?

gender_salary = df.groupby('Gender')['Salary'].mean()

print("Question 3: What is the average salary by gender?")
print(gender_salary.round(2))


# In[39]:


budget_data = {
    'Department': ['IT', 'HR', 'Finance', 'Sales'],
    'Budget': [500000, 200000, 350000, 400000]
}

budget_df = pd.DataFrame(budget_data)

print(budget_df)


# In[40]:


merged_df = pd.merge(
    df,
    budget_df,
    on='Department',
    how='left'
)
print(merged_df.head())


# In[41]:


# Bonus question

pivot = pd.pivot_table(
    df,
    index='Department',
    columns='Gender',
    values='Salary',
    aggfunc='count',
    fill_value=0
)

print(pivot)

