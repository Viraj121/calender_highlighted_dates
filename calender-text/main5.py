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
# url = "https://rtp.pixika.ai/v2/pdf/index.php?tt=1740651460&product=DIYCALENDAR&source=cam&objectKey=67171b2dabeed5808&preview=stitch-done" # working with code gu
# url="https://rtp.pixika.ai/v2/pdf/index.php?tt=1740657059&product=DIYCALENDAR&source=cam&objectKey=677bb68e161186718&preview=stitch-done" # working with code en
url="https://rtp.pixika.ai/v2/pdf/index.php?tt=1740651460&product=DIYCALENDAR&source=cam&objectKey=67171b2dabeed5808&preview=stitch-done"
driver.get(url)

regional_calendar_data = {
    "en": {  # English
        "months": {"January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"},
        "weekdays": {"Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"},
        "dates": {str(i) for i in range(1, 32)}
    }
}

kids_calendar_data = {
    "en": {  # English
        "months": {"Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"},
        "weekdays": {"S", "M", "T", "W", "T", "F", "S"},
        "dates": {str(i) for i in range(1, 32)}
    }
}



try:
    # # Wait for the calendar content to load
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, "calendar-content"))
    # )

    # Parse page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    for div in soup.find_all("div"):
      class_value = div.get("class")
    if class_value:
        print("Class found:", class_value)


    print("step 1:")

    # Determine which dictionary to use based on the presence of specific classes
    if soup.find("div", class_=lambda x: x and "collection-pan-" in str(x)):
     calendar_data = regional_calendar_data
    elif soup.find("div", class_=lambda x: x and "collection-kids" in str(x)):
     calendar_data = kids_calendar_data
    else:
     raise ValueError("Unknown calendar type")

  

    # Wait for all month names to change from English to the target language
    WebDriverWait(driver, 10).until(
        lambda d: (
            # Extract the month name text
            (month_text := d.find_element(By.CLASS_NAME, "month-name").text.strip())
            and
            # Check if month exists in any supported language
            any(month_text in data["months"] for data in calendar_data.values())
        ) if any(d.find_element(By.CLASS_NAME, "month-name").text.strip() in data["months"] 
                 for data in calendar_data.values()) else True
    )

    # Find all calendar-content divs (each contains months and days)
    calendars = soup.find_all("div", class_="calendar-content")

    for calendar in calendars:
        # Extract month and year
        month = calendar.find("div", class_="month-name")
        # print(month)
        # break

        # Find the "days" div inside this same calendar-content
        days_div = calendar.find("div", class_="days")

        # Detect language from class attribute
        language_class = days_div.get("class", []) if days_div else []
        language = None
        for cls in language_class:
            if cls.startswith("lang-"):
                language = cls.split("-")[-1]
                break

        month_text = month.get_text(strip=True) if month else "Month Not Found"

        weekdays = {day.get_text(strip=True) for day in calendar.find_all("div", class_="day-head")}
        dates = {date.get_text(strip=True) for date in calendar.find_all("div", class_="cell-date") if date.get_text(strip=True)}

        # Verify extracted data using set operations
        valid_data = calendar_data.get(language, {})
        valid_months, valid_weekdays, valid_dates = valid_data.get("months", set()), valid_data.get("weekdays", set()), valid_data.get("dates", set())

        month_valid = month_text in valid_months
        weekdays_valid = weekdays.issubset(valid_weekdays)
        dates_valid = dates.issubset(valid_dates)

        # Print validation results
        print(f"\n📅 Calendar - {month_text} (Language: {language})")
        print("-" * 50)
        print(f"Month Valid: {month_valid}")
        print(f"Weekdays Valid: {weekdays_valid}")
        print(f"Dates Valid: {dates_valid}")
        print("-" * 50)

except Exception as e:
    print("Error:", e)

finally:
    driver.quit()  # Close the browser