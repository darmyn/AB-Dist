from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import TimeoutException

# this code handles all processes which require a webdriver in order to crawl on the page
# webdriver crawlers are often useful for accessing information that is not part of the initial HTML snapshot that you can parse with requests
# by simulating a user on a webdriver, it allows for JS to run as well as things like PHP includes, offering a bigger picture of the DOM.

# in order to apply some additional specifications to our selenium firefox driver
firefox_options = webdriver.FirefoxOptions() # we must create the firefox options object
firefox_options.headless = True # setting headless to true is what allows firefox to run silently in the background. 
                                                    # Otherwise the firefox GUI would be present as if you were using the FireFox app.
                                                    # This is said to reduce significant overhead of the GUI when scraping for data.
firefox_service = Service("bin/windows/geckodriver.exe")
driver = webdriver.Firefox(service=firefox_service, options=firefox_options)

# returns a summary of the given product_url
# scrapes the product_page
# analyzes the expected HTML
# retrieves important data
# summarizes important data in a dictionary
def get_product_summary(product_url):
    summary = {}
    driver.get(product_url)

    # for now we will just fetch the current bid of the target product.
    # in practice, more data could be scraped here, such as the product warenty etc. etc.
    try:
        # using webdriverwait allows us to offer a bit of leeway for the site to load all it's HTML content
        current_bid_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="listing-page"]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[2]'))
        )

        summary["current-bid"] = current_bid_element.text
    except TimeoutException:
        print("Timed out waiting for the element to be present")

    return summary