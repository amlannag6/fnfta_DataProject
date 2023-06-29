import requests
from PyPDF2 import PdfReader
import pytesseract
from PIL import Image

def extract_text_from_pdf(pdf_path):
    pdf_file = open(pdf_path, 'rb')
    pdf_reader = PdfReader(pdf_file)

    num_pages = len(pdf_reader.pages)

    text_data = []
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        page_image = page.extract_text()
        text_data.append(page_image)

    pdf_file.close()
    return '\n'.join(text_data)

def extract_financial_data(text):
    data = {}
    # Define the keywords to search for
    keywords = {
        'Cash and Equivalents': None,
        'Restricted Cash': None,
        'Accounts Receivables (AR)': None,
        'Inventory': None,
        'Long-term Investments': None,
        'Investment in GBEs': None,
        'Related Party Loans': None,
        'Investment in Trust Funds': None,
        'Other Assets': None,
        'Total Financial Assets': None
    }

    # Extract data using OCR
    for keyword in keywords:
        index = text.find(keyword)
        if index != -1:
            start_index = index + len(keyword) + 1
            end_index = text.find('\n', start_index)
            value = text[start_index:end_index].strip()
            keywords[keyword] = value

    return keywords

def get_pdf_url(band_number, fiscal_year):
    base_url = "https://fnp-ppn.aadnc-aandc.gc.ca/fnp/Main/Search/DisplayBinaryData.aspx"
    query_params = {
        "BAND_NUMBER_FF": str(band_number),
        "FY": fiscal_year,
        "DOC": "Audited consolidated financial statements",
        "lang": "eng"
    }

    response = requests.get(base_url, params=query_params)
    if response.status_code == 200:
        return response.url
    else:
        return None

def fetch_financial_data(band_number, fiscal_year):
    pdf_url = get_pdf_url(band_number, fiscal_year)
    if pdf_url is None:
        print("Error: Unable to retrieve the PDF URL.")
        return

    response = requests.get(pdf_url)
    if response.status_code == 200:
        pdf_path = "financial_statements.pdf"
        with open(pdf_path, 'wb') as file:
            file.write(response.content)

        extracted_text = extract_text_from_pdf(pdf_path)
        financial_data = extract_financial_data(extracted_text)

        return financial_data
    else:
        print("Error: Unable to download the PDF.")
        return None

# Example usage
band_number = input("Enter Band Number: ")
fiscal_year = input("Enter Fiscal Year (yyyy-yyyy): ")

financial_data = fetch_financial_data(band_number, fiscal_year)

if financial_data is not None:
    print("Financial Data for 2014:")
    for key, value in financial_data.items():
        print(f"{key}: {value}")