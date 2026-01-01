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


def find_section_node(soup, title):
    """
    Find the HTML node that visually represents a section title
    """
    return soup.find(
        lambda tag:
        tag.name in ["div", "span", "td"]
        and title.lower() in tag.get_text(strip=True).lower()
    )


def collect_tables_until_next_section(start_node, soup):
    """
    Collect all tables after a section title
    until the next section title appears
    """
    tables = []
    for elem in start_node.find_all_next():
        # Stop if next section title is reached
        if elem.name in ["div", "span", "td"]:
            text = elem.get_text(strip=True).lower()
            if any(t.lower() in text for t in SECTION_TITLES):
                break

        if elem.name == "table":
            tables.append(elem)

    return tables


def main():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "lxml")

    with pd.ExcelWriter(OUTPUT_EXCEL, engine="xlsxwriter") as writer:
        for section in SECTION_TITLES:
            start_node = find_section_node(soup, section)

            if not start_node:
                print(f"❌ Section title not found: {section}")
                continue

            tables = collect_tables_until_next_section(start_node, soup)

            if not tables:
                print(f"⚠ No tables for section: {section}")
                continue

            dfs = []
            for table in tables:
                try:
                    dfs.append(pd.read_html(str(table))[0])
                except Exception:
                    continue

            if not dfs:
                print(f"⚠ No readable data in section: {section}")
                continue

            final_df = pd.concat(dfs, ignore_index=True)
            sheet_name = section[:31]
            final_df.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"✔ Extracted section: {section}")

    print(f"\n✅ Excel created: {OUTPUT_EXCEL}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Try again with the program code.)
