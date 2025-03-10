from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# WebDriver setup with Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode
options.add_argument('--disable-gpu')  # Disable GPU for better performance in headless mode

service = Service()  # Automatically finds the correct chromedriver
driver = webdriver.Chrome(service=service, options=options)

# Open the target webpage
url = "https://rtp.pixika.ai/v2/pdf/index.php?tt=1740653192&product=DIYCALENDAR&source=cam&objectKey=671ee828b56bc0323&preview=stitch-done"
driver.get(url)


regional_calendar_data = {
    "te": {  # Telugu
        "months": {
            "జనవరి": 1, "ఫిబ్రవరి": 2, "మార్చి": 3, "ఏప్రిల్": 4, "మే": 5, "జూన్": 6,
            "జూలై": 7, "ఆగస్టు": 8, "సెప్టెంబర్": 9, "అక్టోబర్": 10, "నవంబర్": 11, "డిసెంబర్": 12
        },
        "weekdays": ["ఆది", "సోమ", "మంగళ", "బుధ", "గురు", "శుక్ర", "శని"],
        "dates": ["౧", "౨", "౩", "౪", "౫", "౬", "౭", 
                  "౮", "౯", "౧౦", "౧౧", "౧౨", "౧౩", "౧౪", 
                  "౧౫", "౧౬", "౧౭", "౧౮", "౧౯", "౨౦", "౨౧", 
                  "౨౨", "౨౩", "౨౪", "౨౫", "౨౬", "౨౭", "౨౮", 
                  "౨౯", "౩౦", "౩౧"]
    },
    "en": {  # English
    "months": {
        "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
        "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
    },
    "weekdays": ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
    "dates": ["1", "2", "3", "4", "5", "6", "7", 
              "8", "9", "10", "11", "12", "13", "14", 
              "15", "16", "17", "18", "19", "20", "21", 
              "22", "23", "24", "25", "26", "27", "28", 
              "29", "30", "31"]
}
}

try:
    # Wait for the calendar content to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "calendar-content"))
    )

    # Parse page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Find all calendar-content divs (each contains months and days)
    calendars = soup.find_all("div", class_="calendar-content")

    for calendar in calendars:
        # Extract month and year
        month = calendar.find("div", class_="month-name")
        year = calendar.find("div", class_="year-num")

        # year_text = year.get_text(strip=True) if year else "Year Not Found"

        # Extract language information
        language_class = year.get("class", []) if year else []
        language = None
        for cls in language_class:
            if cls.startswith("lang-"):
                language = cls.split("-")[-1]
                break

        # print(language)
        # break
        
        month_text = month.get_text(strip=True) if month else "Month Not Found"
        # year_text = year.get_text(strip=True) if year else "Year Not Found"

        # Extract weekday names
        weekdays = [day.get_text(strip=True) for day in calendar.find_all("div", class_="day-head")]

        # Extract all dates
        dates = [date.get_text(strip=True) for date in calendar.find_all("div", class_="cell-date") if date.get_text(strip=True)]

        # Print calendar output in proper formatting
        print(f"\n📅 Calendar - {month_text}")
        print("-" * 50)
        print(" | ".join(weekdays))
        print("-" * 50)

        row = ["   "] * 7  # Initialize a row with empty spaces
        for index, date in enumerate(dates):
            row[index % 7] = date
            if (index + 1) % 7 == 0 or index == len(dates) - 1:
                print(" | ".join(row))
                row = ["   "] * 7  # Reset the row

        print("-" * 50)

except Exception as e:
    print("Error:", e)

finally:
    driver.quit()  # Close the browser
