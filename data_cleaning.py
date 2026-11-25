import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("Employee_Data.csv")

print("\nDataset Information:")
df.info()
print("\nFirst 5 Rows:")
print(df.head())

print(df.isnull().sum())
print("Duplicate Rows:", df.duplicated().sum())


df['Age'] = df['Age'].fillna(df['Age'].median())
df['Salary'] = df['Salary'].fillna(df['Salary'].median())
df['City'] = df['City'].fillna(df['City'].mode()[0])
df['Performance_Rating'] = df['Performance_Rating'].fillna(df['Performance_Rating'].mode()[0])
df['Joining_Date_Missing'] = df['Joining_Date'].isnull()

df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
df['Salary'] = pd.to_numeric(df['Salary'], errors='coerce')
df['Performance_Rating'] = pd.to_numeric(df['Performance_Rating'], errors='coerce')
df['Joining_Date'] = pd.to_datetime(
    df['Joining_Date'],
    format='mixed',
    dayfirst=True,
    errors='coerce'
)

df['Name'] = df['Name'].str.strip().str.title()
df['Gender'] = df['Gender'].str.strip().str.title()
df['Department'] = df['Department'].str.strip().str.upper()
df['City'] = df['City'].str.strip().str.title()
print(df[['Name','Gender','Department','City']].head(10))

print("Duplicates Before:", df.duplicated().sum())
df = df.drop_duplicates()
print("Duplicates After:", df.duplicated().sum())
print(df[df.duplicated(subset=['Employee_ID'], keep=False)])

def detect_outliers(data, column):

    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)

    IQR = Q3 - Q1

    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR

    outliers = data[
        (data[column] < lower_limit) |
        (data[column] > upper_limit)
    ]

    print("\nColumn:", column)
    print("Lower Limit:", lower_limit)
    print("Upper Limit:", upper_limit)
    print("Outliers:")
    print(outliers[['Employee_ID', column]])

    return outliers
age_outliers = detect_outliers(df, 'Age')
salary_outliers = detect_outliers(df, 'Salary')

# Replace Age outliers with median
age_median = df['Age'].median()

df.loc[
    (df['Age'] < df['Age'].quantile(0.25) -
     1.5 * (df['Age'].quantile(0.75) - df['Age'].quantile(0.25))) |
    (df['Age'] > df['Age'].quantile(0.75) +
     1.5 * (df['Age'].quantile(0.75) - df['Age'].quantile(0.25))),
    'Age'
] = age_median


# Replace Salary outliers with median
Q1 = df['Salary'].quantile(0.25)
Q3 = df['Salary'].quantile(0.75)
IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

salary_median = df['Salary'].median()

df.loc[
    (df['Salary'] < lower) | (df['Salary'] > upper),
    'Salary'
] = salary_median
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
sns.boxplot(y=df['Age'])
plt.title("Age Outliers")

plt.subplot(1, 2, 2)
sns.boxplot(y=df['Salary'])
plt.title("Salary Outliers")

plt.tight_layout()
# plt.show()


before_rows = len(df)

before_missing = df.isnull().sum().sum()

before_duplicates = df.duplicated().sum()

after_rows = len(df)

after_missing = df.isnull().sum().sum()

after_duplicates = df.duplicated().sum()

summary = pd.DataFrame({
    'Metric': ['Rows', 'Missing Values', 'Duplicates'],

    'Before Cleaning': [
        before_rows,
        before_missing,
        before_duplicates
    ],

    'After Cleaning': [
        after_rows,
        after_missing,
        after_duplicates
    ]
})

print(summary)

df.to_csv('clean_data.csv', index=False)

print("Cleaned dataset saved successfully!")

print("Final Dataset Shape:")
print(df.shape)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Records:")
print(df.duplicated().sum())

print("\nData Types:")
print(df.dtypes)

print("\nCleaned Dataset:")
print(df.head(20))