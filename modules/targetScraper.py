from enums.filters.categoryFilter import CategoryFilter
from enums.filters.orderFilter import OrderFilter
from enums.filters.pageSizeFilter import PageSizeFilter
import config
from bs4 import BeautifulSoup
import requests

URL_SCHEME = "https://"
URL_SUBDOMAIN = "www"
URL_DOMAIN = "kotnauction.com"
BASE_URL = f"{URL_SCHEME}{URL_SUBDOMAIN}.{URL_DOMAIN}"
URL_PATH = "auctions/all"
INITIAL_PAGE_URL = f"{BASE_URL}/{URL_PATH}"
PRODUCT_URL = f"{BASE_URL}/listings"
categoryFilter = config.CATEGORY_FILTER
orderFilter = config.ORDER_FILTER
pageSizeFilter = config.PAGE_SIZE_FILTER

# builds a url string and applies all the queries
def get_initial_url():
    query = "?find="+config.SEARCH_QUERY

    if categoryFilter != CategoryFilter.All:
        query += "&category="

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

# given a page of product listings, this function will parse all the listings and fetch their product URL
# the product URL can be used to further investigate said product
def get_product_urls(html_content: str):
    soup = BeautifulSoup(html_content, 'html.parser')

    # find all divs with the class "listing-tile-wrapper"
    listing_tile_wrappers = soup.find_all('div', class_='listing-tile-wrapper')

    urls = []
    # extract data-id from each listing-tile-wrapper div
    for wrapper in listing_tile_wrappers:
        data_id = wrapper.find('div', class_='listing-tile')['data-id']
        urls.append(PRODUCT_URL + "/" + str(data_id))
        
    return urls

# return all the auction dates for each auction category (scraped from the home page directly)
# result will be a list of dictionary where each dictionary represents a specific category of auction
def get_auction_dates():
    response = requests.get(BASE_URL)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # find all <div> elements with the class "auction-header"
        auction_header_divs = soup.find_all("div", class_="auction-header")

        auction_details_list = []

        for auction_header_div in auction_header_divs:
            # within each "auction-header" div, find the text of the <h2> and <h3> elements
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
        
# returns the active number of listings on the auction site
def get_num_active_listings():
        response = requests.get(BASE_URL)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Use BeautifulSoup to find and extract the text from the first <h3> element
            count_element = soup.find("span", "count")

            if count_element:
                return count_element.text
        return None
    
# gets the title of a product given the soup of that product's specific page
def get_product_title(soup):
    title_element = soup.find("h1")
    if title_element:
        return title_element.text
    else:
        return "No Title Provided"

# gets a summary of the given product url, returning a dictionary of data found
def get_product_summary(product_url):
    summary = {}

    try:
        # Make a request to the website
        response = requests.get(product_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        summary["title"] = get_product_title(soup)

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return summary