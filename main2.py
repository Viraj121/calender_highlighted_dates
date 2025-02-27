from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time


public_events = {
    "January": ["1 - New Year", "13 - Lohri", "14 - Makar Sankranti", "26 - Republic Day"],
    "February": ["26 - Maha Shivaratri", "28 - Ramzan Eid"],
    "March": ["30 - Ugadi", "31 - Eid al-Fitr", "14 - Holi"],
    "April": ["6 - Ram Navami", "18 - Good Friday", "20 - Easter"],
    "May": ["1 - Labour Day"],
    "June": ["6 - Bakri Eid"],
    "July": [],
    "August": ["9 - Raksha Bandhan", "15 - Independence Day", "16 - Janmashtami", "26 - Onam", "27 - Ganesh Chaturthi"],
    "September": [],
    "October": ["2 - Dussehra", "20 - Lakshmi Pujan", "21 - Diwali"],
    "November": [],
    "December": ["25 - Merry Christmas"]
}


# Setup WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode
driver = webdriver.Chrome(options=options)

# Open the calendar page
driver.get("https://rtp.pixika.ai/v2/pdf/index.php?tt=1740653192&product=DIYCALENDAR&source=cam&objectKey=671ee828b56bc0323&preview=stitch-done")
# driver.get("https://rtp.pixika.ai/v2/pdf/index.php?tt=1740651498&product=DIYCALENDAR&source=cam&objectKey=672a23bd9ccf97cd4&preview=stitch-done")
# driver.get("https://rtp.pixika.ai/v2/pdf/index.php?tt=1740653374&product=DIYCALENDAR&source=cam&objectKey=670e28a995f222490&preview=stitch-done")
# driver.get("https://rtp.pixika.ai/v2/pdf/index.php?tt=1740653374&product=DIYCALENDAR&source=cam&objectKey=670e28a995f222490&preview=stitch-done")
# driver.get("https://rtp.pixika.ai/v2/pdf/index.php?tt=1740047884&product=DIYCALENDAR&source=cam&objectKey=676ba70b32618e0b2&preview=ready")

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

""" def process_days_div(days_div, month_name):
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
                    print("{event_date} - {event_name}")
                elif event_date:
                    print(f" Highlighted Day: {event_date} (No Event Name) in {month_name}")
    else:
        print(f" No 'days' section found in this calendar-content for {month_name}.")"""

def process_days_div(days_div, month_name):
    if days_div:
        grid_cells = days_div.find_all("div", class_=lambda x: x and "grid-cell" in x)
        for cell in grid_cells:
            classes = cell.get("class", [])

            if "public-event" in classes:
                event_date = None
                for class_name in classes:
                    if class_name.startswith("cell-day-"):
                        event_date = class_name.split("-")[-1]  # Extract day number

                event_name = None
                for class_name in classes[::-1]:  
                    if class_name not in ["grid-cell", "no-overflow", "day-cell", "weekend-cell", "public-event"]:
                        event_name = class_name.replace("-", " ").capitalize()
                        break

                if event_date and event_name:
                    extracted_event = f"{event_date} - {event_name}"
                    if month_name in public_events and extracted_event in public_events[month_name]:
                        print(f"✅ Matched Event: {extracted_event} in {month_name}")
                    else:
                        print(f"❌ Unmatched Event: {extracted_event} in {month_name}")
    else:
        print(f"⚠ No 'days' section found for {month_name}.")



# Iterate through each calendar-content div
for calendar in calendars:

    # Find all "month-box" divs inside this calendar-content
    month_boxes = calendar.find_all("div", class_=lambda x: x and x.startswith("year-num no-overflow"))

    if not month_boxes:
        month_boxes = calendar.find_all("div", class_=lambda x: x and x.startswith("year-month"))
        # print(month_boxes,"debugging")

    for month_box in month_boxes:
        # Find the div with class "month-name" and attribute "data-i18n"
        month_name_div = month_box.find("div", class_="month-name", attrs={"data-i18n": True})

        if month_name_div:
            # Extract the month name from the "data-i18n" attribute
            # month_name = month_name_div["data-i18n"].capitalize()
            month_name = month_name_div["data-i18n"].split("-", 1)[-1].capitalize()
            # print(month_name,'debugging...')
        else:
            # print("parsing through else ")
            # Handle the exceptional case
            classes = month_box.get("class", [])
            # print(f"Classes found: {classes}")  # Debugging print
            
            
            nested_month_box = month_box.find("div", class_="month-box")
            if nested_month_box:
                    nested_classes = nested_month_box.get("class", [])
                    # print(f"Nested classes found: {nested_classes}")  # Debugging print
                    if "month-box" in nested_classes and "no-overflow" in nested_classes:
                        month_box_index = nested_classes.index("month-box")
                        if month_box_index + 1 < len(nested_classes):
                            month_name = nested_classes[month_box_index + 1].capitalize()
                    else:
                      month_name = None

        print(f"\n Month: {month_name}")  # Print the month name

        # Find the "days" div inside this same calendar-content
        days_div = calendar.find("div", class_=lambda x: x and x.startswith("days"))

        # Process the days div with the month name
        process_days_div(days_div, month_name)
