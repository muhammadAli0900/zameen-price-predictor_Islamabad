import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

# Setup Chrome options
options = Options()
options.add_argument("--start-maximized")

# Initialize WebDriver
driver = webdriver.Chrome(
    service=Service(r"C:\Users\Owii\OneDrive\Desktop\Real State Price prediction\chromedriver.exe"),
    options=options
)

# Open Zameen URL
url = 'https://www.zameen.com/Homes/Islamabad-3-1.html'
driver.get(url)

input("🌐 Zameen page loaded.\n👋 Please close any popups/ads manually, then press ENTER to continue...")

# Create CSV file
csv_file = open('zameen_islamabad.csv', 'a', newline='', encoding='utf-8')
writer = csv.writer(csv_file)
writer.writerow(['Title', 'Price', 'Location', 'Beds', 'Baths', 'Area'])

# Start scraping
page = 1
while page > 5:  # Limit to 5 pages for testing
    print(f"\n🔁 Scraping Page {page}...")
    time.sleep(5)  # Give time for listings to load

    # Scroll to bottom to trigger lazy loading
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    listings = driver.find_elements(By.CSS_SELECTOR, 'li[aria-label="Listing"]')
    print(f"📦 Found {len(listings)} listings on this page.")

    if not listings:
        print("⚠️ No listings found. Ending script.")
        break

    for index, listing in enumerate(listings, start=1):
        try:
            # Title
            try:
                title = listing.find_element(By.CSS_SELECTOR, 'a.d870ae17').get_attribute("title")
            except:
                title = "N/A"

            # Price
            try:
                price = listing.find_element(By.CSS_SELECTOR, 'span.dc381b54').text
            except:
                price = "N/A"

            # Location
            try:
                location = listing.find_element(By.CSS_SELECTOR, 'div.db1aca2f').text
            except:
                location = "N/A"

            # Beds
            try:
                beds = listing.find_element(By.CSS_SELECTOR, 'span._6d9b9b83[aria-label="Beds"]').text
            except:
                beds = "N/A"

            # Baths
            try:
                baths = listing.find_element(By.CSS_SELECTOR, 'span._6d9b9b83[aria-label="Baths"]').text
            except:
                baths = "N/A"

            # Area
            try:
                area = listing.find_element(By.CSS_SELECTOR, 'span._6d9b9b83[aria-label="Area"] span').text
            except:
                area = "N/A"

            # Save to CSV
            writer.writerow([title, price, location, beds, baths, area])
            print(f"✅ Saved listing {index}: {title}")

        except Exception as e:
            print(f"⚠️ Skipped listing {index} due to error: {e}")
            continue

    # Click "Next" button to go to the next page
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, 'a[title="Next"]')
        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        time.sleep(1)
        try:
            next_button.click()
        except ElementClickInterceptedException:
            print("🚧 Click blocked. Retrying with JS click...")
            driver.execute_script("arguments[0].click();", next_button)
        page += 1
        time.sleep(5)
    except NoSuchElementException:
        print("⛔ No 'Next' button found. Scraping complete.")
        break

# Close everything
csv_file.close()
driver.quit()
print("✅ All data saved to zameen_islamabad.csv")
