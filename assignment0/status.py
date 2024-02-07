import sqlite3

# function to print the nature and count of nature    
def status(db_name, table_name):
    
    # create connection and connect cur
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    
    query = """
        SELECT Nature, COUNT(*) AS IncidentCount
        FROM {}
        GROUP BY Nature
        ORDER BY 
            CASE WHEN Nature = '' THEN 1 ELSE 0 END, 
            IncidentCount DESC,
            Nature
    """.format(table_name)
    
    cur.execute(query)
    
    rows = cur.fetchall()
    
    con.close()
    
    for row in rows:
        print("{}|{}".format(row[0], row[1]))