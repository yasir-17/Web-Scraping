# -*- coding: utf-8 -*-
# Example main.py
import argparse
import urllib.request
import pypdf
import io
import sqlite3
import re

import os
print("Current Working Directory:", os.getcwd())

# Function to fetch data from URL
def fetch_incidents(url):
    
    # Set the headers to mimic a user agent
    headers = {
        'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    }
    
    # Create a request with the specified URL and headers
    data = urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read()
    
    return data

# Function to parse table from PDF
def extract_incidents(incident_data):
    
    # Create a PDF file reader object
    pdf_reader = pypdf.PdfReader(io.BytesIO(incident_data))

    # Initialize an empty string to store extracted text
    extracted_text = ""

    # Iterate through each page in the PDF
    for page_number in range(len(pdf_reader.pages)):
    
        extracted_text += "\n"
        page = pdf_reader.pages[page_number]

        # Extract text from the page
        page_text = page.extract_text(extraction_mode="layout")

        # Append the extracted text to the result
        extracted_text += page_text

    return extracted_text

# Function to create a new database
def create_db(db_name, table_name, header):
    
     # create connection to the database and create a cur
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    # Drop the existing table if it already exists
    cur.execute("DROP TABLE IF EXISTS {};".format(table_name))

    # Create the table
    create_table_query = "CREATE TABLE {} ({})".format(table_name, ', '.join('"{}"'.format(col) for col in header))
    cur.execute(create_table_query)
    
    # Commit changes
    con.commit()
    con.close()

# Insert parsed data into the SQLite table
def populate_db(db_name, table_name, data_lines):
    
    # Open connection and create cur
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    # Insert parsed data into the SQLite table
    insert_query = "INSERT INTO {} VALUES ({});".format(table_name, ', '.join(['?']*len(data_lines[0])))

    for data_line in data_lines:
        cur.execute(insert_query, data_line)

    # Commit changes
    cur.connection.commit()

    # Commit changes and close connection
    con.commit()
    con.close()
 
# Processing of table   
def modify_table_data(table_data):
    
    # To store table entry
    final_table_data = []
        
    for table_row in table_data:
        
        if len(table_row) == 5:
            final_table_data.append(table_row)
            
    return final_table_data

def status(db_name, table_name):
    
    # create connection and connect cur
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    
    cur.execute("SELECT Nature, COUNT(*) AS IncidentCount FROM {} GROUP BY Nature ORDER BY IncidentCount DESC, Nature".format(table_name))
    
    rows = cur.fetchall()
    
    con.close()
    
    for row in rows:
        print("{}|{}".format(row[0], row[1]))
        
def display(db_name, table_name):
    # Connect to the database
    con = sqlite3.connect(db_name)

    # Create a cur object to execute SQL queries
    cur = con.cursor()

    # Execute a query to select data from a table
    cur.execute('SELECT * FROM incident_table')

    # Fetch all the rows
    rows = cur.fetchall()

    # Display the fetched data
    for row in rows:
        print(row)

    # Close the cur and connection
    cur.close()
    con.close()

     
def count_entries(db_name, table_name):
    # Connect to the SQLite database
    db_connection = sqlite3.connect(db_name)
    cur = db_connection.cur()

    # Execute the COUNT query
    cur.execute(f"SELECT COUNT(*) FROM {table_name};")

    # Fetch the result
    count = cur.fetchone()[0]

    # Close the connection
    db_connection.close()

    return count       

def main(url):
    
    # Download data
    incident_data = fetch_incidents(url)

    # Extract data
    incidents = extract_incidents(incident_data)
    
    
    new_lines = incidents.strip().split('\n')
    table_header = re.split(r'\s{2,}', new_lines[2].strip())
    table_data = [re.split(r'\s{2,}', line.strip()) for line in new_lines[3:]]
    
    final_table_data = modify_table_data(table_data)
    
    
    db_name = "resources/normanpd.db"
    table_name = "incident_table"
    
    # create new database
    create_db(db_name, table_name, table_header)

    # insert data
    populate_db(db_name, table_name, final_table_data)
    
    status(db_name, table_name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, help="Incident summary url.")
    args = parser.parse_args()

    if args.incidents:
        main(args.incidents)

