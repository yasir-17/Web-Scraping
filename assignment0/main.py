# -*- coding: utf-8 -*-
# Example main.py
import argparse
import re
from fetchIncidents import fetchIncidents
from extractIncidents import extractIncidents
from createdb import createdb
from populatedb import populatedb
from status import status

 
# Processing of table   
def modify_table_data(table_data):
    
    # To store table entry
    final_table_data = []
        
    for table_row in table_data:
        
        if len(table_row) > 1:
            final_table_data.append(table_row)
            
    return final_table_data
    

def main(url):
    
    db_name = "resources/normanpd.db"
    table_name = "incident_table"
    
    # Download data
    incident_data = fetchIncidents(url)

    # Extract data
    incidents = extractIncidents(incident_data)
    
    # Extracting header and rows values
    new_lines = incidents.strip().split('\n')
    table_header = re.split(r'\s{2,}', new_lines[2].strip())
    table_data = [re.split(r'\s{2,}', line.strip()) for line in new_lines[3:-1]]
    final_table_data = modify_table_data(table_data)
    
    # create new database
    createdb(db_name, table_name)

    # insert data
    populatedb(db_name, table_name, final_table_data)
    
    # Print nature of incident and count of incident
    status(db_name, table_name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, help="Incident summary url.")
    args = parser.parse_args()

    if args.incidents:
        main(args.incidents)

