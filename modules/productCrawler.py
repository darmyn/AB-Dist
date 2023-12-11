from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()

def get_product_summary(product_url):
    # Create a new instance of the Firefox driver (you can use other browsers as well)

    summary = {}
    # Open the URL in the browser
    driver.get(product_url)

    try:
        # Wait for a specific element to be present on the page
        current_bid_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="listing-page"]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[2]'))
        )

        summary["current-bid"] = current_bid_element.text
    except:
        print("Timed out waiting for the element to be present")
    return summary
