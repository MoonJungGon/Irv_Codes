import csv
import requests
from bs4 import BeautifulSoup
import re

filename = "presents.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="")
writer = csv.writer(f)

# Define attributes for the CSV file
attributes = ["title", "price", "reviews"]
writer.writerow(attributes)

count = 0

# Loop through pages
for page_number in range(1, 250):
    url = f"https://www.etsy.com/search?q=valentine+gift&anchor_listing_id=780107583&ref=pagination&mosv=sese&moci=1226894514292&mosi=1231873457722&is_merch_library=true&page={page_number}"

    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "lxml")

    season_header = soup.find("div", class_="v2-listing-card__info")

    if season_header:
        episodes = soup.find_all("div", class_="v2-listing-card__info")

        # Loop through episodes on the page
        for episode in episodes:
            # Extract title information
            title = episode.find("h3", attrs={"class": "wt-text-caption v2-listing-card__title wt-text-truncate"}).get_text()
            count += 1
            print('Count')
            print(count)
            print(title)

            # Extract cost information
            cost = episode.find("span", class_="currency-value").get_text()
            print(cost)

            # Extract review information
            review_element = episode.find("p", class_="wt-text-body-smaller")
            review = review_element.get_text() if review_element else "N/A"

            # Check if the review contains numbers
            if any(char.isdigit() for char in review):
                match = re.search(r'\((.*?)\)', review)

                if match:
                    review = match.group(1)
                else:
                    print("No review count found.")

                print(review)

                # Write data to CSV file
                data_rows = [title, cost, review]
                writer.writerow(data_rows)
            else:
                print("No numeric review count found. Skipping to the next episode.")

    else:
        print(f"No information on page {page_number}.")

f.close()
