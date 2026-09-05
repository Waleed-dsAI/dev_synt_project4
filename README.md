# Task 4 — Data Cleaning & AI-Powered Data Enrichment
Dataset
Source: Customer dataset (CSV), ~1000 records — name, age, gender, state, signup date, email, phone number, subscription status.

56 missing age values
54 missing state values
10 duplicate records (same name + email, different customer_id)
10 duplicate customer_id values
phone_number initially lost leading zeros due to pandas auto-inferring it as a numeric column on read
Cleaning Performed
Issue	Action	Reasoning
Duplicate name+email	Dropped	Same person registered twice under different IDs
Duplicate customer_id	Dropped	IDs must be unique by design
Missing state	Filled with "unknown"	Preserves the row rather than discarding a full customer record over one field
Missing age	Filled with median age per gender group	Avoids injecting one identical global value across all rows; more realistic than a flat mean/median
phone_number leading zeros	Fixed via dtype=str on read_csv	Root cause was pandas reading the column as numeric, not a formatting error in the source data

Before/after row and null counts are printed at runtime in cleaning.py.

## Enrichment Performed
age_bracket — derived field, bins age into ranges (<18, 18-25, 26-35, 36-45, 46-60, 60+) for segmentation.
signup_cohort — derived field, extracts year-month of signup (e.g. 2024-05) for cohort grouping.
phone_valid — API-based validity flag using NumVerify's free tier. Applied to a random sample of 20 records (random_state=42 for reproducibility) due to free-tier rate limits. Values: True/False (validated), "Not Checked" (outside sample), "Check Failed" (sampled but API call failed after retries).
## Tools Used
Python, pandas
NumVerify free API (phone validation)
Google Sheets / Supabase (final storage — see below)
Final Storage

Cleaned + enriched dataset uploaded to https://docs.google.com/spreadsheets/d/1jiQe-APbTghiLXNo94f-2mFkIB4y5hZ2H7vAcs0cGK4/edit?usp=sharing.

# Limitations
Phone validation covers only a 20-record sample, not the full dataset, due to NumVerify's free-tier request limit (100/month).
Some sampled phone numbers failed validation due to API timeouts; these are marked "Check Failed" rather than silently dropped or left blank.
