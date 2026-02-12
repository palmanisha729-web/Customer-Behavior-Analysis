import pandas as pd
import numpy as np
df = pd.read_csv("data.csv")
df.info()
df.describe(include='all')
df.isnull().sum()
df['Review Rating']=df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))
df.columns=df.columns.str.lower()
df.columns= df.columns.str.replace(' ','_')
df=df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})
df.head()

#feature enginerring
#creating columns to for different age groups 
labels=['Young-Adults','Adult','Middle-aged','Senior']
df['age_group']=pd.qcut(df['age'],q=4,labels=labels)
df[['age','age_group']].head(10)
df['frequency_of_purchases']
df.groupby('frequency_of_purchases').count()

#creating a frequency purchse days column 
frequency_mapping={
    "Fortnightly":14,
    "Bi-Weekly":14,
    "Weekly":7,
    "Monthly":30,
    "Quarterly":90,
    "Every 3 months":90,
    "Annually":365
}

df['purchase_frequency_days']=df['frequency_of_purchases'].map(frequency_mapping)
if (df["discount_applied"]==df['promo_code_used']).all():
    df=df.drop('promo_code_used',axis=1)


from sqlalchemy import create_engine

# Step 1: Connect to PostgreSQL
# Replace placeholders with your actual details
username = "username"      # default user
password = "password" # the password you set during installation
host = "localhost"         # if running locally
port = "5432"              # default PostgreSQL port
database = "customer_behavior"    # the database you created in pgAdmin

engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")

# Step 2: Load DataFrame into PostgreSQL
table_name = "customer"   # choose any table name
df.to_sql(table_name, engine, if_exists="replace", index=False)

print(f"Data successfully loaded into table '{table_name}' in database '{database}'.")