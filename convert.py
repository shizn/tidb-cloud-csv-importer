import pandas as pd
from sqlalchemy import create_engine
import glob
from dotenv import load_dotenv
import mysql.connector
import os
import csv

load_dotenv()

# Define the database connection parameters
local_config = {
  'user': 'root',
  'password': os.environ['DB_PASSWORD'],
  'host': '127.0.0.1',
  'port': '8083',
}

db_name = os.environ['DB_NAME']
db_password = os.environ['DB_PASSWORD']

# Connect to the MySQL server
print("Connecting to: "+local_config['host'])
cnx = mysql.connector.connect(**local_config)

#
cursor = cnx.cursor()
cursor.execute("DROP DATABASE IF EXISTS "+ db_name)

# Create a new database

print("CREATE DATABASE "+ db_name)
cursor.execute("CREATE DATABASE "+ db_name)

# Close the cursor and database connection
cursor.close()
cnx.close()


# Set the chunk size to 10000 rows
chunk_size = 100000

# Get a list of all the CSV files in a directory
csv_files = glob.glob('./csv/*.csv')

# Loop through each CSV file
for csv_file in csv_files:
    # Create an iterator that reads the file in chunks
    iterator = pd.read_csv(csv_file, chunksize=chunk_size, quotechar='"', quoting=csv.QUOTE_ALL , encoding='utf-8', on_bad_lines='error', engine='python')
    print("Processing file: "+csv_file)
    # Create MySQL database connection
    engine = create_engine('mysql+mysqlconnector://root:'+db_password+'@127.0.0.1:8083/'+db_name)
    table_name = os.path.basename(csv_file).split('.')[0]
    # Loop through the chunks and write them to the database
    for chunk in iterator:
        # Rename columns if necessary
        # chunk = chunk.rename(columns={'old_name': 'new_name'})

        # Write chunk to MySQL database
        
        chunk.to_sql(name=table_name, con=engine, if_exists='append', index=False)
    print("Done processing file: "+csv_file)
# Close the database connection
engine.dispose()