# cis6930sp24 -- Assignment0 -- Template

Name: Yasir Khan

# Assignment Description (in your own words)
This project extract incidents data from Norman, Oklahoma Police department and save that in a sql database and print the nature of incidents and number of times they have occured.

# How to install
pipenv install

## How to run
For running the project you can either run through 1 or 2
1) pipenv run python assignment0/main.py --incidents <url>
2) python assignment0/main.py --incidents <url>

For running the testcase use either of the following command
1) pipenv run python -m pytest
2) pipenv run python -m unittest tests/test_download.py
3) python -m unittest .\tests\test_download.py
The test case can also be run using pipenv

I have attached the video recording in the docs folder. But below is a gif attached
![](docs/Recording%202024-02-08%20235815.mp4.gif)


## Functions
1)  main.py - This is the main function of the project which invokes all other function

2) fetchIncidents(url) - This function takes URL as parameter and fetch the data from the URL. I am storing the data in the local directory and not saving at some file location. The reason is that my main objective is not to just only retreive data but to make a sql database which i can do by only storing in the local variable.

3) extractincidents(incident_data) - This Python function, extractIncidents, takes a PDF file's binary data (incident_data) as input and uses pypdf to read the PDF. It iterates through each page, extracts text using layout mode, and concatenates the extracted text into a single string, which is then returned.

4) createdb(db_name, table_name) - This Python function, createdb, creates a SQLite database (db_name) and a table (table_name). It establishes a connection, drops the table if it exists, and then creates a new table with specific column names. The function finally commits the changes and closes the connection. The header name of the table is hard coded as we already know all the column header values

5) populatedb(db_name, table_name, table_data) - This Python function, populatedb, inserts parsed data (data_lines) into a specified SQLite table (table_name) within a database (db_name). It connects to the database, prepares an SQL INSERT query with placeholders, and iteratively executes the query for each line of data, handling cases where the data lines have empty nature columns. Finally, it commits the changes and closes the connection.

6) status(db_name, table_name) - This Python function, status, retrieves and prints the count of each unique value in the 'Nature' column from a specified SQLite table (table_name) within a database (db_name). It utilizes a SQL query to group and count incidents by nature, and then prints the nature and its corresponding count for each category. The output is formatted as "Nature|IncidentCount".

## Testings
I am performing the unit testing using Mocking. The purpose of this mocking is to validate individual functions of code working as expected.

1) test_fetch_incidents - The fetchIncidents function involves fetching data from a URL using urllib.request.urlopen. I have created a mock version of these functions using unitest.mock. The mock versions simulate the behavior of the real functions without performing actual network requests. Instead of fetching real data from the specified URL, I provided static mock data using the following line: mock_urlopen.return_value.read.return_value = b'Some mock data'. This static mock data represents what I expect the response content to be. The url variable in the test function can be any URL since the actual HTTP request is not made. It is used as input to the fetchIncidents function for testing.

2) test_extract_incidents - This unit test mocks the PDF library to control page content. It creates mock pages with pre-defined text and feeds them to the function. Finally, it checks if the extracted text matches the expected output, ensuring correct text extraction without needing real PDFs.

3) test_create_db - The unit test test_create_db uses mocking to verify that the createdb function successfully creates a database and table. It then checks if the sqlite3.connect method is called with the correct arguments and if the expected SQL queries are executed on the mock cursor, and if the commit and close methods are called on the mock connection.

4) test_populate_db - This test mocks sqlite3.connect. It verifies data insertion calls matches with the expected queries and checks if commit and close occur on the mock connection. This also validate if the insertion follows table format. This ensures function behaves correctly without needing a real database for testing.

5) test_status - The test mocks the database connection and returns desired data. It captures the printed output of the status function and compares it to the expected string. This verifies that the function generates the correct output using mocked data 

## Database Development
1) Create database using function createdb() 
    - Establish a connection to an SQLite database named "normanpd.db" using the `sqlite3` module.
    - Create a cursor to interact with the database.
    - Define the name of the coulmns of the table and then execute sql statement to create table with that column name

2) Insert elements in the database using function populatedb()
    - Construct an SQL `INSERT` statement to insert the data into the incidents table.
    - Execute the `INSERT` statement using the cursor and then commit the changes to the database.

3) Print nature of incidents and counts using status()
    - Execute an SQL query to get the count of incidents grouped by nature from the table
    - Sort the results first by count (in descending order) and then alphabetically by nature.

## Bugs and Assumptions
The assumptions is that not all column value for a particular row is empty. There is atleast one non-empty column value present for each row.
