# Limitation Notice:
For your sake, I removed the part of the code that would scrape EVERY page resulted by the search query. This is because,
when running this application with the ability to scrape each page, the program will take very long to gather it's data from the site. Therefor, I've limited this program to only parse the first page of results.

If you are looking at the auction site, please note that there may be significantly less items on the page at the time of you testing. You may need to ease up on the filter restrictions of your query for this matter. At the time of development, there were around 14000 listings and 792 pages. At the time of writing the auction has just completed and there are not many listings. If you can not get ANY results, please contact me.

# Problem: 

Auction website has limited search features. Product analysts and shoppers will have a difficult time filtering for specific products on the page. Need a way to obtain data from products automatically given a more advanced search query.

# Solution: 

A python web scraper that can pull data from the target auction website, search for products using the various filters, and create a report of the found products in a spreadsheet with links to the auction page.

# How to use:

This config.py file will contain the various constants you can edit to alter the search pattern for the application.

After personalizing the config file, run the main.py file. 

You may be prompted to install various packages. See requirements.txt for list of packages included. 

The application should ask for your consent, and then scrape the website for data and return results.