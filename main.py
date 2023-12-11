from pprint import pprint
from modules import targetScraper, productCrawler, util
import openpyxl
import requests
import config
import json

TERMS_OF_SERVICE_PATH = "legal/TOS.txt"

# Force open the TOS.txt file so that the user sees it
util.open_file(TERMS_OF_SERVICE_PATH)

# Use of while loop to lock the user in this dialog until they respond appropriately.
while True:
    # build a prettyfied string to display a dialog choice for the user to accept TOS agreement
    dialog_message = util.build_dialog_choice_str("\nAccept License Agreement: ", ["Yes", "No", "Print License Agreement"])
    result = input(dialog_message)
    # handle responses
    if result == "1":
        print("\nResult: Welcome!")
        break
    elif result == "2":
        print("\nResult: Program exited because the license was denied.")
        exit()
    elif result == "3":
        with open(TERMS_OF_SERVICE_PATH, "r") as f:
            print(f"\nResult: {f.read()}")
            f.close()
    else:
        print("\nResult: Incorrect response type!")
    print("\n")

# scrape the site for relevent data needed to execute the main functionality of the application
target_url = targetScraper.get_initial_url()
page = requests.get(target_url)
productUrls = targetScraper.get_product_urls(page.content)
auction_dates = targetScraper.get_auction_dates()
num_active_listings = targetScraper.get_num_active_listings()

# main dialog
while True:
    # get user choice
    dialog_message = util.build_dialog_choice_str("\nWhat would you like to do:", ["Get Auction Details", "Get Number Active Listings", "Get Spreadsheet Report"])
    result = input(dialog_message)
    if result == "1":
        print("Result: \n")
        pprint(auction_dates, depth=3)
    elif result == "2":
        print(f"Result: {num_active_listings}")
    elif result == "3": 
        print("\n[YIELD] Result: Fetching products, this may take a moment... ")
        wb = openpyxl.Workbook()
        ws = wb.active

        headers = ["Product URL", "Product Title", "Current Bid"]
        ws.append(headers)

        for productUrl in productUrls:
            print("\nAnalyzing URL: " + productUrl)
            # gather summary
            scraped_summary = targetScraper.get_product_summary(productUrl)
            crawled_summary = productCrawler.get_product_summary(productUrl)

            productTitle = scraped_summary.get("title") or "NO TITLE PROVIDED"
            currentBid = crawled_summary.get("current-bid") or "NIL"

            # check for bidding matches
            currentBidPrice = int(currentBid[1:])
            if currentBidPrice <= config.PRICE_THRESHOLD:

                match = True

                # check for title matches
                if len(config.TITLE_FILTERS) >  0:
                    # using * to pass all the title filters in the list as kwarguments
                    if util.find_matches_in_text(productTitle.lower(), *config.TITLE_FILTERS):
                        match = True
                    else:
                        match = False


                if match:
                    # shorten the hyperlink for productUrl
                    short_url = f'=HYPERLINK("{productUrl}","Link")'

                    # append data to the sheet
                    ws.append([short_url, productTitle, currentBid])

        # save the workbook to a file
        wb.save("output/products.xlsx")
    elif result == "3":
        print("\nResult: Program exited")
        exit()
    else:
        print("\nResult: Incorrect response type!")