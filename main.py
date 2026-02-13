from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from time import sleep, time

# Variables
url = "https://ozh.github.io/cookieclicker/"
five_minutes = time() + 60 * 5

# Setup Chrome driver
chrome_options = webdriver.ChromeOptions()  # customize how launches chrome
chrome_options.add_experimental_option("detach", True)  # browser stays open
driver = webdriver.Chrome(options=chrome_options)  # start new Chrome browser
driver.get(url)  # open webpage

sleep(3)  # wait

# Language Selection
try:
    language_button = driver.find_element(By.ID, value="langSelect-EN")
    language_button.click()
    # sleep(3)
except NoSuchElementException:
    print("Language not found")

sleep(3)  # wait

# Find the big cookie
cookie = driver.find_element(By.ID, value="bigCookie")

# Get all store items
for i in range(18):
    item_ids = {f"product{i}"}

# set timer
timeout = time() + 5

while True:
    cookie.click()
    # Buy the most expensive item every 5 seconds
    if time() > timeout:
        try:
            cookies_element = driver.find_element(By.ID, value="cookies")
            cookies_text = cookies_element.text
            # find available products
            products = driver.find_elements(By.CSS_SELECTOR, value="div[id^='product']")

            # find the most expensive item
            expensive_item = None
            for product in reversed(products):
                # check if item is available (enabled class)
                if "enabled" in product.get_attribute("class"):
                    expensive_item = product
                    break
            # if found, buy the expensive item
            if expensive_item:
                expensive_item.click()
                print(f"Bought:{expensive_item.get_attribute('id')}")
        except (NoSuchElementException, ValueError):
            print("Could not find items")
        # reset timer
        timeout = time() + 5

    # Stop after 5 minutes
    if time() > five_minutes:
        try:
            cookies_element = driver.find_element(by=By.ID, value="cookies")
            print(f"Final result: {cookies_element.text}")
        except NoSuchElementException:
            print("Couldn't get the final cookie count")
        break

# driver.close()  # closes a tab
driver.quit()  # closes the browser
