import urllib.parse
import webbrowser

def redirect_to_financial_statements(band_number, fiscal_year):
    base_url = "https://fnp-ppn.aadnc-aandc.gc.ca/fnp/Main/Search/DisplayBinaryData.aspx"
    query_params = {
        "BAND_NUMBER_FF": str(band_number),
        "FY": fiscal_year,
        "DOC": "Audited consolidated financial statements",
        "lang": "eng"
    }

    url = base_url + '?' + urllib.parse.urlencode(query_params)
    webbrowser.open(url)

# Example usage
band_number = input("Enter Band Number: ")
fiscal_year = input("Enter Fiscal Year (yyyy-yyyy): ")
redirect_to_financial_statements(band_number, fiscal_year)