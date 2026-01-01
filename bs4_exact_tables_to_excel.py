import pandas as pd
from bs4 import BeautifulSoup

HTML_FILE = "test_scrap.html"
OUTPUT_EXCEL = "Tender_Details_Exact.xlsx"


SECTION_TITLES = [
    "Basic Details",
    "Payment Instruments",
    "Covers Information",
    "Tender Fee Details",
    "EMD Fee Details",
    "Work Item Details",
    "Critical Dates",
    "Tenders Documents",
    "Tender Inviting Authority"
]

def find_table_afte_title(soup, title_text):
    title_elem = soup.find(lambda tag: tag.name in ["div", "span", "td"]
                          and tag.get_text(strip = True).startswith(title_text))
    
    if not title_elem:
        return None
    
    return title_elem.find_next("table")

def main():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "lxml")

    with pd.ExcelWriter(OUTPUT_EXCEL, engine= "xlsxwriter") as writer:
        for section in SECTION_TITLES:
            table = find_table_afte_title(soup, section)

            if table is None:
                print(f"Section not found: {section}")
                continue

            try:
                df = pd.read_html(str(table))[0]
                sheet_name = section[:31]
                df.to_excel(writer, sheet_name= sheet_name, index= False)
                print(f"Extracted: {section}")
            except Exception as e:
                print(f"Failed {section}: {e}")

    print(f"Excel created: {OUTPUT_EXCEL}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Try again with the file execution.")
