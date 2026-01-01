import pandas as pd
import os
from bs4 import BeautifulSoup

# CONFIG
INPUT_PATH =  "test_scrap.html"
OUTPUT_FILE = "table_extracted.xlsx"

# HELPER
def get_html_files(input_path):
    if os.path.isfile(input_path):
        return [input_path]
    
    if os.path.isdir(input_path):
        return [os.path.join(input_path, 'f')
                for f in os.listdir(input_path)
                if f.lower().endswith(".html")
                ]
    raise ValueError("INPUT_PATH is neither a file nor a directory.")

# CORE LOGIC
def extract_tables_from_html(html_file, writer):
    with open(html_file, "r", encoding = "utf-8") as f:
        soup = BeautifulSoup(f.read(), "lxml")
    
    # records = []
    tables = soup.find_all("table")
    base_name = os.path.splitext(os.path.basename(html_file))[0]

    print(f"{base_name}: {len(tables)} tables found.")

    for idx, table in enumerate(tables, start = 1):
        try:
            df = pd.read_html(str(table))[0]
            sheet_name = f"{base_name}_T{idx}"
            sheet_name = sheet_name[:31]
            df.to_excel(writer, sheet_name =sheet_name, index = False)
        except Exception:
            continue

def main():
    html_files = get_html_files(INPUT_PATH)

    with pd.ExcelWriter(OUTPUT_FILE, engine= "xlsxwriter") as writer:
        for html_file in html_files:
            print(f"Processing : {html_file}")
            extract_tables_from_html(html_file, writer)

if __name__ == "__main__":
    main()
