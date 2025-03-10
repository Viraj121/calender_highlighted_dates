from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Setup WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode
driver = webdriver.Chrome(options=options)

# Open the calendar page
driver.get("https://rtp.pixika.ai/v2/pdf/index.php?tt=1740653192&product=DIYCALENDAR&source=cam&objectKey=671ee828b56bc0323&preview=stitch-done")

# Wait until at least one calendar-content div loads
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "calendar-content"))
)

time.sleep(3)  # Extra wait to ensure full rendering

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")

driver.quit()  # Close the browser

# Find all calendar-content divs (each contains months and days)
calendars = soup.find_all("div", class_="calendar-content")

# Iterate through each calendar-content div
for calendar in calendars:
    # Find all "month-box" divs inside this calendar-content
    month_boxes = calendar.find_all("div", class_=lambda x: x and x.startswith("month-box"))
    print(month_box)
    # break

    for month_box in month_boxes:
        classes = month_box.get("class", [])

        # Extract the month name dynamically
        month_name = None

        if "month-box" in classes:
            month_box_index = classes.index("month-box")
            if month_box_index + 1 < len(classes):
                month_name = classes[month_box_index + 1].capitalize()

        if not month_name:
            print("textttt")
            # Check for the presence of a div with class "year-box"
            year_box_div = month_box.find("div", class_="year-box")
            if year_box_div:
                # Check for the nested div with data-i18n attribute
                nested_div = year_box_div.find("div", attrs={"data-i18n": True})
                if nested_div:
                    month_name = nested_div["data-i18n"].capitalize()
        print(f"\n Month: {month_name}")  # Print the month name

        # Find the "days" div inside this same calendar-content
        days_div = calendar.find("div", class_=lambda x: x and x.startswith("days"))

        if days_div:
            # Find all "grid-cell" divs inside "days"
            grid_cells = days_div.find_all("div", class_=lambda x: x and "grid-cell" in x)

            # Iterate through grid cells to find public-event days
            for cell in grid_cells:
                classes = cell.get("class", [])

                if "public-event" in classes:
                    # Extract event date from "cell-day-{num}"
                    event_date = None
                    for class_name in classes:
                        if class_name.startswith("cell-day-"):
                            event_date = class_name.split("-")[-1]  # Extract day number

                    # Extract event name (last class, avoiding structural classes)
                    event_name = None
                    for class_name in classes[::-1]:  # Reverse loop for event name
                        if class_name not in ["grid-cell", "no-overflow", "day-cell", "weekend-cell", "public-event"]:
                            event_name = class_name.replace("-", " ").capitalize()
                            break

                    if event_date and event_name:
                        print(f" Highlighted Day: {event_date} - {event_name}")
                    elif event_date:
                        print(f" Highlighted Day: {event_date} (No Event Name)")
        else:
            print(" No 'days' section found in this calendar-content.")