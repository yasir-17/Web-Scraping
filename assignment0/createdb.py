import sqlite3

# Create a sqlite database and a table
def createdb(db_name, table_name):
    
    # create connection to the database and create a cursor
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    # Drop the existing table if it already exists
    cur.execute("DROP TABLE IF EXISTS {};".format(table_name))

    # Create the table
    create_table_query = "CREATE TABLE {} (incident_time TEXT, incident_number TEXT, incident_location TEXT, nature TEXT, incident_ori TEXT);".format(table_name)
    cur.execute(create_table_query)
    
    # Commit changes
    con.commit()
    con.close()