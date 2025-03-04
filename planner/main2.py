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

service = Service()
driver = webdriver.Chrome(service=service, options=options)

# Open the target webpage
url = "https://rtp.pixika.ai/v2/pdf/index.php?tt=1740653192&product=DIYCALENDAR&source=cam&objectKey=671ee828b56bc0323&preview=stitch-done"
driver.get(url)

regional_calendar_data = {
    "te": {
        "months": {"జనవరి": 1, "ఫిబ్రవరి": 2, "మార్చి": 3, "ఏప్రిల్": 4, "మే": 5, "జూన్": 6,
                    "జూలై": 7, "ఆగస్టు": 8, "సెప్టెంబర్": 9, "అక్టోబర్": 10, "నవంబర్": 11, "డిసెంబర్": 12},
        "weekdays": ["ఆది", "సోమ", "మంగళ", "బుధ", "గురు", "శుక్ర", "శని"],
        "dates": ["౧", "౨", "౩", "౪", "౫", "౬", "౭", "౮", "౯", "౧౦", "౧౧", "౧౨", "౧౩", "౧౪", "౧౫", "౧౬", "౧౭", "౧౮", "౧౯", "౨౦", "౨౧", "౨౨", "౨౩", "౨౪", "౨౫", "౨౬", "౨౭", "౨౮", "౨౯", "౩౦", "౩౧"]
    },
    "en": {
        "months": {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
                    "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12},
        "weekdays": ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
        "dates": [str(i) for i in range(1, 32)]
    }
}

def detect_language(class_list):
    for cls in class_list:
        if cls.startswith("lang-"):
            return cls.split("-")[-1]  # Extract language code
    return None

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
        extracted_data = {}
        
        # Extract month name
        month_element = calendar.find("div", class_="month-name")
        month_text = month_element.get_text(strip=True) if month_element else "Month Not Found"
        
        # Extract language from class attributes
        year_element = calendar.find("div", class_="year-num")
        language = detect_language(year_element.get("class", [])) if year_element else None
        
        if not language or language not in regional_calendar_data:
            print("Language not detected or unsupported.")
            continue
        
        # Extract weekdays
        weekdays = [day.get_text(strip=True) for day in calendar.find_all("div", class_="day-head")]
        
        # Extract dates
        dates = [date.get_text(strip=True) for date in calendar.find_all("div", class_="cell-date") if date.get_text(strip=True)]
        
        extracted_data["month"] = month_text
        extracted_data["weekdays"] = weekdays
        extracted_data["dates"] = dates
        
        # Compare extracted data with dictionary
        expected_data = regional_calendar_data[language]
        
        errors = []
        
        # Validate month
        if month_text not in expected_data["months"]:
            errors.append(f"Mismatched month: {month_text}")
        
        # Validate weekdays
        if weekdays != expected_data["weekdays"]:
            errors.append(f"Mismatched weekdays: {weekdays}")
        
        # Validate dates
        if dates != expected_data["dates"]:
            errors.append(f"Mismatched dates: {dates}")
        
        # Print validation results
        if errors:
            print("\nValidation Errors:")
            for error in errors:
                print("-", error)
        else:
            print("\nCalendar data matches expected values ✅")
    
except Exception as e:
    print("Error:", e)

finally:
    driver.quit()
