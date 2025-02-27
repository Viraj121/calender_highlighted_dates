import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (no UI)
driver = webdriver.Chrome(options=options)  # Use Chrome WebDriver

url = "https://rtp.pixika.ai/v2/pdf/index.php?tt=1740651498&product=DIYCALENDAR&source=cam&objectKey=672a23bd9ccf97cd4&preview=stitch-done"

# Open the URL
driver.get(url)

# Wait for 5 seconds to allow the page to load fully
time.sleep(5)

# Get the page source after JavaScript execution
html = driver.page_source

# Close the browser
driver.quit()

# Parse the updated HTML with BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

years = ["2024","2025","2026"]
for year in years:
    for month in range(1, 13):

        # Find the div with class "month-1"
        month_div = soup.find(
            "div",
            class_=f"koye-s001-container-planner planner month-{month} year-{year} slot-id-undefined lang-en",
        )
        if month_div:
            month_name_div = month_div.find("div", class_="month-name")
        else:
            continue
        try:
            if month_name_div:
                month_name = month_name_div.text
        except:
            print(month)
        if month_div:
            # Find all divs with class "grid-cell" inside "month-1"
            grid_cells = month_div.find_all("div", class_="grid-cell")

            for cell in grid_cells:
                # Check if "grid-cell" contains a "cell-public-event"
                public_events = cell.find_all("div", class_="cell-public-event")
                cell_date = cell.find("div", class_="cell-date")
                if public_events and cell_date:
                    print("---- Grid Cell Found ----")
                    print("Cell Date:")
                    print(month_name, cell_date.get_text(strip=True), year)  # Extract date text
                    print("\nPublic Event:")
                    for public_event in public_events:
                        print(public_event.text)  # Pretty print event HTML
                    print("------------------------\n")
        else:
            print("No div with class 'month-1' found.")