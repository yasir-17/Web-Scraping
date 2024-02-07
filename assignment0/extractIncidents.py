import io
import pypdf

# Function to parse table from PDF
def extractIncidents(incident_data):
    
    # Create a PDF file reader object
    reader = pypdf.PdfReader(io.BytesIO(incident_data))

    # Initialize an empty string to store extracted text
    extracted_text = ""

    # Iterate through each page in the PDF
    for page_number in range(len(reader.pages)):
    
        extracted_text += "\n"
        page = reader.pages[page_number]

        # Extract text from the page
        page_text = page.extract_text(extraction_mode="layout")

        # Append the extracted text to the result
        extracted_text += page_text

    return extracted_text