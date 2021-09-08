import requests
import csv
import pandas as pd
import json
import psycopg2



url = "https://api.census.gov/data/2019/acs/acs5?get=NAME,B02001_001E,B05001_001E,B06011_001E,B25001_001E,B11016_001E,B15012_001E&for=block%20group:*&in=state:01&in=county:*&in=tract:*&key=78a8d70faaa1ff3a34386ff69e6228d438395130"
response = requests.get(url)
if response.status_code == 200:
    with open("output.txt", mode = 'w') as output_file:
        output_file.write(response.text)
        
    data_list = json.loads(response.content.decode('utf-8'))
    data_df = pd.DataFrame(data_list)
    
    data_df.to_csv('output.csv', index=False)
    
        
    
num_cols = len(data_df.columns)

connection_acs = psycopg2.connect(
    host="acs-db.mlpolicylab.dssg.io",
    port="5432",
    database="acs_data_loading",
    user="mlpp_student",
    password="CARE-horse-most",
    options="-c search_path=dbo,acs")


cursor = connection_acs.cursor()
cursor.execute("DROP TABLE IF EXISTS rjpatel_acs_data;")
sql = '''CREATE TABLE rjpatel_acs_data(
NAME text PRIMARY KEY,
RACE text,
NATIVITY_CITIZENSHIP_STATUS text,
MEDIAN_INCOME text,
HOUSING_UNITS text,
HOUSEHOLD_TYPE text,
BACHELORS_DEGREES text,
STATE text,
COUNTY text,
TRACT text,
BLOCK_GROUP text
);'''

cursor.execute(sql);
print("rjpatel_acs_data table is created successfully")


with open('output.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    next(reader)
    for row in reader:
        cursor.execute("INSERT INTO rjpatel_acs_data VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", row)


connection_acs.commit()

connection_acs.close()


"""
Variables included:
B02001_001E - race
B05001_001E - NATIVITY AND CITIZENSHIP STATUS IN THE UNITED STATES
B06011_001E - MEDIAN INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS) BY PLACE OF BIRTH IN THE UNITED STATES
B25001_001E - HOUSING UNITS
B11016_001E - HOUSEHOLD TYPE BY HOUSEHOLD SIZE
B15012_001E - TOTAL FIELDS OF BACHELOR'S DEGREES REPORTED

"""