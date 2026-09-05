import pandas as pd
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Load the CLEANED dataset (not the raw one)
data = pd.read_csv('cleaned_customer_data.csv')
data['signup_date'] = pd.to_datetime(data['signup_date'])


# ENRICHMENT 1: Age Bracket

bins = [0, 18, 25, 35, 45, 60, 120]
labels = ['<18', '18-25', '26-35', '36-45', '46-60', '60+']
data['age_bracket'] = pd.cut(data['age'], bins=bins, labels=labels)


# ENRICHMENT 2: Signup Cohort

data['signup_cohort'] = data['signup_date'].dt.to_period('M').astype(str)

# ---------------------------------------------------------------
# ENRICHMENT 3: Phone Number Validity Flag

API_KEY = os.getenv('my_api_key')
SAMPLE_SIZE = 5

data['phone_valid'] = "Not Checked"
sample_indices = data.sample(n=SAMPLE_SIZE, random_state=42).index

for idx in sample_indices:
    phone = str(data.loc[idx, 'phone_number'])
    url = f"http://apilayer.net/api/validate?access_key={API_KEY}&number={phone}&country_code=ID"

    for attempt in range(3):
        try:
            resp = requests.get(url, timeout=15).json()
            result = resp.get('valid', None)
            data.loc[idx, 'phone_valid'] = str(result) if result is not None else "Check Failed"
            print(f"Checked {phone}: valid={resp.get('valid')}")
            break
        except Exception as e:
            print(f"Attempt {attempt+1} failed for {phone}: {e}")
            time.sleep(2)
    time.sleep(1.5)

print("\nPhone validation summary:")
print(data['phone_valid'].value_counts(dropna=False))


data.to_csv('enriched_customer_data.csv', index=False)

# Verify the save actually worked
check = pd.read_csv('enriched_customer_data.csv')
print("\n=== Verification: sampled rows in saved file ===")
print(check.loc[sample_indices, ['phone_number', 'phone_valid']])