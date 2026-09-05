import pandas as pd
data=pd.read_csv('customers.csv',dtype={"phone_number":str})
pd.set_option('display.max_rows', None)

data['signup_date']=pd.to_datetime(data['signup_date'])


print("Missing age before:",data['age'].isnull().sum())
print("Duplicate rows found:", data.duplicated(subset=['name','email']).sum())
print("Missing States before : ",data['state'].isnull().sum())
print("Duplicates in customer id before :  ",data['customer_id'].duplicated().sum())
data=data.drop_duplicates(subset=['name','email'])
data=data.drop_duplicates(subset=['customer_id'])
data=data.fillna({"state":"unknown"})
data['age'] = data['age'].fillna(data.groupby('gender')['age'].transform('median'))
data['age']=data["age"].astype(int)


print("Missing age After : ",data['age'].isnull().sum())
print("Duplicate rows found After :", data.duplicated().sum())
print("Missing States after : ",data['state'].isnull().sum())
print("Duplicates in customer id after:  ",data['customer_id'].duplicated().sum())


# row index reset after these duplicates are deleted 
data=data.reset_index(drop=True)
data['name']=data['name'].str.strip()# remove any white spaces 
print(data['subscribe'].value_counts())
print(data['gender'].value_counts())
print(data['phone_number'].dtype)
print(data['phone_number'].astype(str).str.len().value_counts())
print(data['phone_number'].astype(str).str.startswith('0').sum())
print(data['phone_number'].astype(str).str.len().min())
print(data['phone_number'].astype(str).str.len().max())
data.to_csv('cleaned_customer_data.csv',index=False)