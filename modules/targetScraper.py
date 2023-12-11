from enums.filters.categoryFilter import CategoryFilter
from enums.filters.orderFilter import OrderFilter
from enums.filters.pageSizeFilter import PageSizeFilter
from enum import Enum
from config import productFilters
from bs4 import BeautifulSoup
import requests

URL_SCHEME = "https://"
URL_SUBDOMAIN = "www"
URL_DOMAIN = "kotnauction.com"
BASE_URL = f"{URL_SCHEME}{URL_SUBDOMAIN}.{URL_DOMAIN}"
URL_PATH = "auctions/all"
INITIAL_PAGE_URL = f"{BASE_URL}/{URL_PATH}"
PRODUCT_URL = f"{BASE_URL}/listings"
categoryFilter = productFilters.CATEGORY_FILTER
orderFilter = productFilters.ORDER_FILTER
pageSizeFilter = productFilters.PAGE_SIZE_FILTER

def get_initial_url():
    query = ""

    if categoryFilter != CategoryFilter.All:
        query = "?category="

    if categoryFilter == CategoryFilter.Not_Yet_Assigned:
        query += "none"
    else:
        query += str(categoryFilter.value)

    if orderFilter != OrderFilter.Undefined:
        query += "&order_by="

    if orderFilter == OrderFilter.Ending_Soon:
        query += "ending_asc"

    if orderFilter == OrderFilter.Newly_Listed:
        query += "posted_desc"

    if pageSizeFilter != PageSizeFilter.TwentyFive:
        query += f"&per_page={str(pageSizeFilter.value)}"

    return f"{INITIAL_PAGE_URL}{query}"

def get_product_urls(html_content: str):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all divs with the class "listing-tile-wrapper"
    listing_tile_wrappers = soup.find_all('div', class_='listing-tile-wrapper')

    urls = []
    # Extract data-id from each listing-tile-wrapper div
    for wrapper in listing_tile_wrappers:
        data_id = wrapper.find('div', class_='listing-tile')['data-id']
        urls.append(PRODUCT_URL + "/" + str(data_id))
        
    return urls

def get_auction_dates():
    response = requests.get(BASE_URL)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all <div> elements with the class "auction-header"
        auction_header_divs = soup.find_all("div", class_="auction-header")

        auction_details_list = []

        for auction_header_div in auction_header_divs:
            # Within each "auction-header" div, find the text of the <h2> and <h3> elements
            h2_element = auction_header_div.find("h2")
            h3_element = auction_header_div.find("h3")

            if h2_element and h3_element:
                auction_details = {
                    "title": h2_element.text.strip(),
                    "date": h3_element.text.strip()
                }
                auction_details_list.append(auction_details)

        return auction_details_list

    return None
        
def get_num_active_listings():
        response = requests.get(BASE_URL)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Use BeautifulSoup to find and extract the text from the first <h3> element
            count_element = soup.find("span", "count")

            if count_element:
                return count_element.text
        return None
    
def get_product_title(soup):
    title_element = soup.find("h1")
    if title_element:
        return title_element.text
    else:
        return "No Title Provided"

def get_product_summary(product_url):
    summary = {}

    try:
        # Make a request to the website
        response = requests.get(product_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        summary["title"] = get_product_summary(soup)

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return summary