from bs4 import BeautifulSoup
import pandas as pd

HTML_FILE = "test_scrap.html"

def extract_tables_bs4():
    with open(HTML_FILE, "r", encoding= "utf-8") as f:
        html = f.read()
    
    soup = BeautifulSoup(html, "lxml")
    tables = soup.find_all("table")

    print(f"Total tables found: {len(tables)}")

    if not tables:
        print("No tables present in HTML.")
        return
    
    for idx, table in enumerate(tables, start = 1):
        try:
            df = pd.read_html(str(table))[0]
            df.to_csv(f"C:\\Users\\Developer\\Shubham_files\\Web-Scrapping\\bs4_data\\bs4_table_{idx}.csv", index= False)
            print(f"Saved bs4_table_{idx}.csv")
        except Exception as e:
            print(f"Faile table {idx}: {e}")

if __name__ == "__main__":
    extract_tables_bs4()
