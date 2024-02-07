# cis6930sp24 -- Assignment0 -- Template

Name: Yasir Khan

# Assignment Description (in your own words)
This project extract incidents data from Norman, Oklahoma Police department and print the nature of incidents and number of times they have occured.

# How to install
pipenv install

## How to run
For running the project you can either run through 1 or 2
1) pipenv run python assignment0/main.py --incidents <url>
2) python assignment0/main.py --incidents <url>

For running the testcase run using following command
1) python -m unittest .\tests\test_download.py
One can also run test case using pipenv

I have attached the video is the docs folder

## Functions
#### main.py \
1) fetchIncidents(url) - This function takes URL as parameter and fetch the data from the URL. I am storing the data in the local directory and not saving at some file location. The reason is that my main objective is not to just only retreive data but to make a sql database which i can do by only storing in the local variable.

2) extractincidents(incident_data) - This function takes fetched data as paramter and parse the table data from the pdf.

3) createdb(db_name, table_name) - This function takes the name of database, the name of table as parameter and craete a database with these values. The header name of the table is hard coded as we already know all the column header values

4) populatedb(db_name, table_name, table_data) - This function takes the name of database, the name of table and the rows values and populate the table.

5) status(db_name, table_name) - This function takes database name, and the table name as parameter and print the nature of incidents and number of occurence of the incidents.

## Testings
I am performing the unit testing using Mocking. The purpose of this mocking is to validate individual functions of code working as expected.

1) test_fetch_incidents - The fetchIncidents function involves fetching data from a URL using urllib.request.urlopen. I have created a mock version of these functions using unitest.mock. The mock versions simulate the behavior of the real functions without performing actual network requests. Instead of fetching real data from the specified URL, I provided static mock data using the following line: mock_urlopen.return_value.read.return_value = b'Some mock data'. This static mock data represents what I expect the response content to be. The url variable in the test function can be any URL since the actual HTTP request is not made. It is used as input to the fetchIncidents function for testing.

2) test_extract_incidents - This unit test mocks the PDF library to control page content. It creates mock pages with pre-defined text and feeds them to the function. Finally, it checks if the extracted text matches the expected output, ensuring correct text extraction without needing real PDFs.

3) test_create_db - The unit test test_create_db uses mocking to verify that the createdb function successfully creates a database and table. It then checks if the sqlite3.connect method is called with the correct arguments and if the expected SQL queries are executed on the mock cursor, and if the commit and close methods are called on the mock connection.

4) test_populate_db - This test mocks sqlite3.connect. It verifies data insertion calls matches with the expected queries and checks if commit and close occur on the mock connection. This also validate if the insertion follows table format. This ensures function behaves correctly without needing a real database for testing.

5) test_status - The test mocks the database connection and returns desired data. It captures the printed output of the status function and compares it to the expected string. This verifies that the function generates the correct output using mocked data 

## Database Development


## Bugs and Assumptions
The assumptions is that not all column value for a particular row is empty. There is atleast one non-empty column value present for each row.
