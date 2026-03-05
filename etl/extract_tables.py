import pdfplumber
import pandas as pd

def extract_tables(pdf_path):

    tables = []

    with pdfplumber.open(pdf_path) as pdf:

        for page_num, page in enumerate(pdf.pages):

            page_tables = page.extract_tables()

            for table in page_tables:

                df = pd.DataFrame(table)

                tables.append({
                    "page": page_num + 1,
                    "table": df
                })

    return tables