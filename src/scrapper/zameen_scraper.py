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

# Use manually downloaded ChromeDriver
driver = webdriver.Chrome(
    service=Service(r"C:\Users\Owii\OneDrive\Desktop\Real State Price prediction\chromedriver.exe"),
    options=options
)

# Open Zameen URL
url = 'https://www.zameen.com/Homes/Islamabad-3-1.html'
driver.get(url)

input("🌐 Opening Zameen...\n👋 Please close the popups/ads manually, then press ENTER to continue...")

# Create CSV file
csv_file = open('zameen_islamabad.csv', 'a', newline='', encoding='utf-8')
writer = csv.writer(csv_file)
writer.writerow(['Title', 'Price', 'Location', 'Beds', 'Baths', 'Area'])

# Scraping loop
page = 1
while True:
    print(f"\n🔁 Scraping Page {page}...")
    time.sleep(5)  # Wait for listings to load

    # Scroll down to ensure listings are loaded
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)  # Wait for lazy-loaded listings

    #listings = driver.find_elements(By.CSS_SELECTOR, 'li._357a9934')
    listings = driver.find_elements(By.CSS_SELECTOR, 'li[aria-label="Listing"]')
    print(f"📦 Found {len(listings)} listings on this page.")

    if not listings:
        print("⚠️ No listings found. Breaking loop.")
        break

for index, listing in enumerate(listings, start=1):
    try:
        # Try to extract title
        try:
            title = listing.find_element(By.CSS_SELECTOR, "h2._64bb5d3b").text
        except:
            title = "N/A"

        # Try to extract price
        try:
            price = listing.find_element(By.CSS_SELECTOR, "span.dc381b54").text
        except:
            price = "N/A"

        # Try to extract location
        try:
            location = listing.find_element(By.CSS_SELECTOR, "span._1f4cefcf").text
        except:
            location = "N/A"

        # Try to extract specs (beds, baths, area)
        try:
            specs = listing.find_elements(By.CSS_SELECTOR, "span._984949fb")
            beds = specs[0].text if len(specs) > 0 else "N/A"
            baths = specs[1].text if len(specs) > 1 else "N/A"
            area = specs[2].text if len(specs) > 2 else "N/A"
        except:
            beds = baths = area = "N/A"

        # Write data to CSV
        writer.writerow([title, price, location, beds, baths, area])
        print(f"✅ Saved listing {index}: {title}")

    except Exception as e:
        print(f"⚠️ Skipped listing {index} due to error: {e}")
        continue


    # Go to next page
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, 'a[title="Next"]')
        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        time.sleep(1)
        try:
            next_button.click()
        except ElementClickInterceptedException:
            print("🚧 Click blocked, trying again after scrolling...")
            time.sleep(2)
            driver.execute_script("arguments[0].click();", next_button)
        page += 1
        time.sleep(5)
    except NoSuchElementException:
        print("⛔ No 'Next' button found. Stopping.")
        break

# Close everything
csv_file.close()
driver.quit()
print("✅ Scraped data saved to zameen_islamabad.csv")
