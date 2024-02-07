import sqlite3

# Insert parsed data into the SQLite table
def populatedb(db_name, table_name, data_lines):
    
    # Open connection and create cur
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    # Insert parsed data into the SQLite table
    insert_query = "INSERT INTO {} VALUES ({});".format(table_name, ', '.join(['?']*len(data_lines[0])))

    for data_line in data_lines:
        
        if len(data_line) < 5 :
            temp_line = [''] * 5
            cur.execute(insert_query, temp_line)
        else :
            cur.execute(insert_query, data_line)

    # Commit changes
    cur.connection.commit()

    # Commit changes and close connection
    con.commit()
    con.close()