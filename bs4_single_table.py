import pandas as pd
from bs4 import BeautifulSoup

HTML_FILE = "test_scrap.html"
OUTPUT_EXCEL = "Basic_Details.xlsx"

def extract_basic_details():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "lxml")

    # 1️⃣ Find the "Basic Details" section title (robust match)
    title_node = soup.find(
        lambda tag:
        tag.name in ["div", "span", "td"]
        and "basic details" in tag.get_text(strip=True).lower()
    )

    if not title_node:
        raise Exception("❌ 'Basic Details' title not found in HTML")

    # 2️⃣ Find the FIRST table after this title
    table = title_node.find_next("table")

    if not table:
        raise Exception("❌ No table found after 'Basic Details'")

    # 3️⃣ Read table exactly as-is
    df = pd.read_html(str(table))[0]

    # 4️⃣ Save to Excel
    df.to_excel(OUTPUT_EXCEL, index=False)

    print("✅ Basic Details table extracted successfully")
    print(f"📄 Output file: {OUTPUT_EXCEL}")


if __name__ == "__main__":
    extract_basic_details()
