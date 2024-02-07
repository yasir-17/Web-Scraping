import io
import sys
import unittest
from unittest.mock import patch
from assignment0.fetchIncidents import fetchIncidents
from assignment0.extractIncidents import extractIncidents
from assignment0.createdb import createdb
from assignment0.populatedb import populatedb
from assignment0.status import status

class TestFetchIncidents(unittest.TestCase):

    @patch('urllib.request.urlopen')
    @patch('urllib.request.Request')
    def test_fetch_incidents(self, mock_request, mock_urlopen):
        # Mock the data returned by urllib.request.urlopen
        mock_urlopen.return_value.read.return_value = b'Mocked data'

        # Call the fetchIncidents function
        url = 'https://example.com'
        result = fetchIncidents(url)

        # Check that the urllib.request.Request was called with the correct arguments
        mock_request.assert_called_once_with(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})

        # Check that urllib.request.urlopen was called with the correct arguments
        mock_urlopen.assert_called_once_with(mock_request.return_value)

        # Check that the function returns the expected result
        self.assertEqual(result, b'Mocked data')
        
    @patch('pypdf.PdfReader')
    def test_extract_incidents(self, mock_reader):
        """Tests if text is extracted correctly from PDF pages."""
        incident_data = b'some_pdf_data'  # Sample PDF data
        expected_text = "\nPage 1 text\nPage 2 text"  # Expected extracted text

        # Mock the reader object to return expected page text
        mock_page1 = unittest.mock.MagicMock()
        mock_page1.extract_text.return_value = "Page 1 text"
        mock_page2 = unittest.mock.MagicMock()
        mock_page2.extract_text.return_value = "Page 2 text"
        mock_reader.return_value.pages = [mock_page1, mock_page2]

        # Call the extractIncidents function
        extracted_text = extractIncidents(incident_data)

        # Assert that the extracted text matches the expected text
        self.assertEqual(extracted_text, expected_text)
    
    @patch('sqlite3.connect')
    def test_create_db(self, mock_connect):
        #Tests if the database and table are created successfully using mocking.
        db_name = 'test_database.db'
        table_name = 'test_table'

        # Call the function to create the database and table
        createdb(db_name, table_name)

        # Verify that sqlite3.connect was called with the correct arguments
        mock_connect.assert_called_once_with(db_name)

        # Access the mock connection and cursor objects
        mock_con = mock_connect.return_value
        mock_cur = mock_con.cursor.return_value

        # Check if the expected SQL queries were executed
        mock_cur.execute.assert_has_calls([
            unittest.mock.call("DROP TABLE IF EXISTS {};".format(table_name)),
            unittest.mock.call("CREATE TABLE {} (incident_time TEXT, incident_number TEXT, incident_location TEXT, nature TEXT, incident_ori TEXT);".format(table_name))
        ])

        # Check if commit and close methods were called
        mock_con.commit.assert_called_once()
        mock_con.close.assert_called_once()
        
    @patch('sqlite3.connect')
    def test_populate_db(self, mock_connect):
        #Testing to see if data is inserted correctly
        db_name = 'test_database.db'
        table_name = 'test_table'
        data_lines = [
            ['incident_time1', 'incident_number1', 'incident_location1', 'nature1', 'incident_ori1'],
            ['incident_time2', 'incident_number2', 'incident_location2'],  # Instance with empty nature
            ['incident_time3', 'incident_number3', 'incident_location3', 'nature3', 'incident_ori3']
        ]

        # Call the function to populate the database
        populatedb(db_name, table_name, data_lines)

        # Access the mock connection and cursor objects
        mock_con = mock_connect.return_value
        mock_cur = mock_con.cursor.return_value

        # Check if the expected SQL queries were executed
        expected_calls = [
            unittest.mock.call("INSERT INTO {} VALUES (?, ?, ?, ?, ?);".format(table_name), data_lines[0]),
            unittest.mock.call("INSERT INTO {} VALUES (?, ?, ?, ?, ?);".format(table_name), ['', '', '', '', '']),  # Padding for shorter line
            unittest.mock.call("INSERT INTO {} VALUES (?, ?, ?, ?, ?);".format(table_name), data_lines[2])
        ]
        mock_cur.execute.assert_has_calls(expected_calls)

        # Check if commit and close methods were called
        mock_con.commit.assert_called_once()
        mock_con.close.assert_called_once()
        
    @patch('sqlite3.connect')
    def test_status(self, mock_connect):
        """Tests if the status function prints the correct nature and count."""
        db_name = 'test_database.db'
        table_name = 'test_table'

        # Mock the results to be returned by the cursor
        mock_results = [('nature1', 3), ('', 2), ('nature3', 1)]
        mock_cur = mock_connect.return_value.cursor.return_value
        mock_cur.fetchall.return_value = mock_results

        # Capture the printed output
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Call the status function
        status(db_name, table_name)

        # Restore the standard output
        sys.stdout = sys.__stdout__

        # Assert the printed output
        expected_output = "nature1|3\n|2\nnature3|1\n"
        self.assertEqual(captured_output.getvalue(), expected_output)
        

if __name__ == '__main__':
    unittest.main()
