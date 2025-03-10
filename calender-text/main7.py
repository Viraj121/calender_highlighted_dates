from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time


# WebDriver setup
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

service = Service()
driver = webdriver.Chrome(service=service, options=options)

# Open the webpage

# Open the target webpage
# url = "https://rtp.pixika.ai/v2/pdf/index.php?tt=1740653374&product=DIYCALENDAR&source=cam&objectKey=670e28a995f222490&preview=stitch-done" # working with code te
# url = "https://rtp.pixika.ai/v2/pdf/index.php?tt=1740653192&product=DIYCALENDAR&source=cam&objectKey=671ee828b56bc0323&preview=stitch-done" # working with code te
# url="https://rtp.pixika.ai/v2/pdf/index.php?tt=1740657059&product=DIYCALENDAR&source=cam&objectKey=677bb68e161186718&preview=stitch-done" # working with code en
# url="https://rtp.pixika.ai/v2/pdf/index.php?tt=1740651498&product=DIYCALENDAR&source=cam&objectKey=672a23bd9ccf97cd4&preview=stitch-done" # working with code mr
# url="https://rtp.pixika.ai/v2/pdf/index.php?tt=1740651460&product=DIYCALENDAR&source=cam&objectKey=67171b2dabeed5808&preview=stitch-done" # working with code gu
# url="https://rtp.pixika.ai/v2/pdf/index.php?tt=1741248710&product=DIYCALENDAR&source=cam&objectKey=67752ee3a411ceb5d&preview=stitch-done" # palson-2,kid theme, working
# url="https://rtp.pixika.ai/v2/pdf/index.php?tt=1741249400&product=DIYCALENDAR&source=cam&objectKey=67c95b5d9ecdaaaac&preview=collection-init" # working, kid theme en
url="https://rtp.pixika.ai/v2/pdf/index.php?tt=1741249485&product=DIYCALENDAR&source=cam&objectKey=67c95bc5a098461bf&preview=collection-init" # kid theme, working mr



driver.get(url)
time.sleep(5)


regional_calendar_data = {
    "te": {  # Telugu
        "months": {"జనవరి", "ఫిబ్రవరి", "మార్చి", "ఏప్రిల్‌", "మే", "జూన్‌",
                   "జులై", "ఆగస్టు", "సెప్టెంబరు", "అక్టోబరు", "నవంబరు", "డిసెంబరు"},
        "weekdays": ["ఆది", "సోమ", "మంగళ", "బుధ", "గురు", "శుక్ర", "శని"],
        "dates": {"౧", "౨", "౩", "౪", "౫", "౬", "౭", "౮", "౯", "౧౦", "౧౧", "౧౨", "౧౩", "౧౪", "౧౫",
                  "౧౬", "౧౭", "౧౮", "౧౯", "౨౦", "౨౧", "౨౨", "౨౩", "౨౪", "౨౫", "౨౬", "౨౭", "౨౮", "౨౯", "౩౦", "౩౧"}
    },
    "en": {  # English
        "months": {"January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"},
        "weekdays": ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
        "dates": {str(i) for i in range(1, 32)}
    },
    "mr": {  # Marathi
        "months": {"जानेवारी", "फेब्रुवारी", "मार्च", "एप्रिल", "मे", "जून","जुलै", "ऑगस्ट", "सप्टेंबर", "ऑक्टोबर", "नोव्हेंबर", "डिसेंबर"},
        "weekdays": ["रवि", "सोम", "मंगळ", "बुध", "गुरु", "शुक्र", "शनि"],
        "dates": {"१", "२", "३", "४", "५", "६", "७", "८", "९", "१०", "११", "१२", "१३", "१४", "१५",
                   "१६", "१७", "१८", "१९", "२०", "२१", "२२", "२३", "२४", "२५", "२६", "२७", "२८", "२९", "३०", "३१"}
    },
    "gu": {  # Gujarati
        "months": {"જાન્યુઆરી", "ફેબ્રુઆરી", "માર્ચ", "એપ્રિલ", "મે", "જૂન",
                   "જુલાઈ", "ઓગસ્ટ", "સપ્ટેમ્બર", "ઓક્ટોબર", "નવેમ્બર", "ડિસેમ્બર"},
        "weekdays": ["રવિ", "સોમ", "મંગળ", "બુધ", "ગુરુ", "શુક્ર", "શનિ"],
        "dates": {"૧", "૨", "૩", "૪", "૫", "૬", "૭", "૮", "૯", "૧૦", "૧૧", "૧૨", "૧૩", "૧૪", "૧૫",
                  "૧૬", "૧૭", "૧૮", "૧૯", "૨૦", "૨૧", "૨૨", "૨૩", "૨૪", "૨૫", "૨૬", "૨૭", "૨૮", "૨૯", "૩૦", "૩૧"}
    }
}

kids_calendar_data = {
    "te": {  # Telugu
        "months": {"జనవరి", "ఫిబ్రవరి", "మార్చి", "ఏప్రిల్‌", "మే", "జూన్‌",
                   "జులై", "ఆగస్టు", "సెప్టెంబరు", "అక్టోబరు", "నవంబరు", "డిసెంబరు"},
        "weekdays": {"ఆది", "సోమ", "మంగళ", "బుధ", "గురు", "శుక్ర", "శని"},
        "dates": {"౧", "౨", "౩", "౪", "౫", "౬", "౭", "౮", "౯", "౧౦", "౧౧", "౧౨", "౧౩", "౧౪", "౧౫","౧౬", "౧౭", "౧౮", "౧౯", "౨౦", "౨౧", "౨౨", "౨౩", "౨౪", "౨౫", "౨౬", "౨౭", "౨౮", "౨౯", "౩౦", "౩౧"}
    },
    "en": {  # English
        "months": {"Jan", "Feb", "March", "Apr", "May", "Jun","Jul", "Aug", "Sept", "Oct", "Nov", "Dec"},
        "weekdays": ['S', 'M', 'T', 'W', 'T', 'F', 'S'],
        "dates": {str(i) for i in range(1, 32)}
    },
    "mr": {  # Marathi
    "months": {"जानेवारी", "फेब्रुवारी", "मार्च", "एप्रिल", "मे", "जून", "जुलै", "ऑगस्ट", "सप्टेंबर", "ऑक्टोबर", "नोव्हेंबर", "डिसेंबर"},
    "weekdays": ["रवि", "सोम", "मंगळ", "बुध", "गुरु", "शुक्र", "शनि"],
    "dates": {"१", "२", "३", "४", "५", "६", "७", "८", "९", "१०", "११", "१२", "१३", "१४", "१५",
              "१६", "१७", "१८", "१९", "२०", "२१", "२२", "२३", "२४", "२५", "२६", "२७", "२८", "२९", "३०", "३१"}
    },
    "gu": {  # Gujarati
        "months": {"જાન્યુઆરી", "ફેબ્રુઆરી", "માર્ચ", "એપ્રિલ", "મે", "જૂન",
                   "જુલાઈ", "ઓગસ્ટ", "સપ્ટેમ્બર", "ઓક્ટોબર", "નવેમ્બર", "ડિસેમ્બર"},
        "weekdays": {"રવિ", "સોમ", "મંગળ", "બુધ", "ગુરુ", "શુક્ર", "શનિ"},
        "dates": {"૧", "૨", "૩", "૪", "૫", "૬", "૭", "૮", "૯", "૧૦", "૧૧", "૧૨", "૧૩", "૧૪", "૧૫",
                  "૧૬", "૧૭", "૧૮", "૧૯", "૨૦", "૨૧", "૨૨", "૨૩", "૨૪", "૨૫", "૨૬", "૨૭", "૨૮", "૨૯", "૩૦", "૩૧"}
    }
}


try:
    # Get page source and parse it
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    # Wait for the calendar content to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "calendar-content"))
    )

    print("step 1")

    # Find the div with id "hub_1" (outer container)
    hub_div = soup.find("div", id="hub_1")

    if hub_div:
        # Search for class names that contain "collection-pan-" or "collection-kids"
        if hub_div.find("div", class_=lambda x: x and ("collection-pan-" in x or "mankind_vet" in x)):
            print("slot-1 theme")
            selected_calendar_data = regional_calendar_data
        elif hub_div.find("div", class_=lambda x: x and ("collection-kids" in x)):
            print("slot-2 theme")
            selected_calendar_data = kids_calendar_data
        else:
            print("no theme detected")
            selected_calendar_data = None
    else:
        print("hub_1 div not found")
        selected_calendar_data = None

except Exception as e:
    print("Error:", e)
    selected_calendar_data = None

# print([div.get("class") for div in hub_div.find_all("div")])



if selected_calendar_data:
    try:
        # Wait for the month name to appear and match one of the valid months
        WebDriverWait(driver, 10).until(
            lambda d: (
                (month_text := d.find_element(By.CLASS_NAME, "month-name").text.strip())
                and any(month_text in data["months"] for data in selected_calendar_data.values())
            ) if any(d.find_element(By.CLASS_NAME, "month-name").text.strip() in data["months"]
                     for data in selected_calendar_data.values()) else True
        )

        print("starting....")

        # Now proceed with extracting months, weekdays, and dates using the selected dictionary
        calendars = soup.find_all("div", class_="calendar-content")

        for calendar in calendars:
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

            weekdays = [day.get_text(strip=True) for day in calendar.find_all("div", class_="day-head")]

            dates = {date.get_text(strip=True) for date in calendar.find_all("div", class_="cell-date") if date.get_text(strip=True)}

            # Verify extracted data using set operations
            valid_data = selected_calendar_data.get(language, {})
            valid_months = valid_data.get("months", set())
            valid_weekdays = valid_data.get("weekdays", [])
            valid_dates = valid_data.get("dates", set())

            month_valid = month_text in valid_months
            weekdays_valid = weekdays==valid_weekdays
            dates_valid = dates.issubset(valid_dates)

            # Print validation results
            print(f"\n📅 Calendar - {month_text} (Language: {language})")
            print("-" * 50)
            print(f"Month Valid: {month_valid}")
            # print(month_text)
            print(f"Weekdays Valid: {weekdays_valid}")
            # print(f"Extracted Weekdays: {weekdays}")
            # print(f"Expected Weekdays: {valid_weekdays}")
            print(f"Dates Valid: {dates_valid}")
            print("-" * 50)
          
    except Exception as e:
        print("Error:", e)

# Close the browser
driver.quit()
