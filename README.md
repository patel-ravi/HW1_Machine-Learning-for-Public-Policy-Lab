# MLPP_HW1_rjpatel

I collected data for the parameters race, nativity and citizenship status, median income in the past 12 months, housing units, household type and bachelor's degrees for Alabama to analyze how parameters like race, citizenship, income and education are associated with the proportion of housing units across household types. I used the API of api.census.gov to fetch the data and created csv file of the data using json and pandas.
Next, I created connection with the database using psycopg2.connect and created an empty datatable rjpatel_acs_data using .cursor() and .execute() methods on the connection.
For inserting data into this empty datatable, I used the previously created csv file with the fetched  data by iterating over the rows of the csv file using csv.reader() and inserted one row at a time from the csv file into the datatable.
After completing inserting the data into the datatable, I used the .commit() and .close() methods on the connection with the database to save the changes and close the connection.
