from playwright.sync_api import sync_playwright
import pandas as pd

HTML_FILE = "test_scrap.html"

def extract_tables_playwright():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load local HTML file
        page.goto(f"file:///{HTML_FILE}", timeout=60000)
        page.wait_for_load_state("load")

        tables = page.query_selector_all("table")
        print(f"✅ Total tables found: {len(tables)}")

        for idx, table in enumerate(tables, start=1):
            html = table.inner_html()
            try:
                df = pd.read_html(f"<table>{html}</table>")[0]
                df.to_csv(f"playwright_folder/playwright_table_{idx}.csv", index=False)
                print(f"✔ Saved playwright_table_{idx}.csv")
            except Exception as e:
                print(f"⚠ Failed table {idx}: {e}")

        browser.close()


if __name__ == "__main__":
    extract_tables_playwright()
