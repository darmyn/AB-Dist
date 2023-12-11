from modules import targetScraper, productCrawler, util
import openpyxl
from openpyxl.styles import NamedStyle
from urllib.parse import quote
import requests

util.open_file("legal/TOS.txt")

if input("Type `Y` to agree to the terms of service and continue using the application").lower() == "y":
    target_url = targetScraper.get_initial_url()

    page = requests.get(target_url)

    productUrls = targetScraper.get_product_urls(page.content)
    auction_dates = targetScraper.get_auction_dates()
    num_active_listings = targetScraper.get_num_active_listings()

    wb = openpyxl.Workbook()
    ws = wb.active

    # Set the headers in the first row of the sheet
    headers = ["Product URL", "Product Title", "Current Bid"]
    ws.append(headers)

    for productUrl in productUrls:

        scraped_summary = targetScraper.get_product_summary(productUrl)
        crawled_summary = productCrawler.get_product_summary(productUrl)

        productTitle = scraped_summary["title"]
        currentBid = crawled_summary["current-bid"]

        # Only consider products with currentBid == "$0"
        if currentBid == "$5":
            # Shorten the hyperlink for productUrl
            short_url = f'=HYPERLINK("{productUrl}","Link")'

            # Append data to the sheet
            ws.append([short_url, productTitle, currentBid])


    # Save the workbook to a file
    wb.save("output/products.xlsx")

