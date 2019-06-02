from googlesearch import search
import csv
import requests
from lxml import html
import time
import random
import urllib
from bs4 import BeautifulSoup


def scrape_multiple(search_terms, delay=1, url_version=1):
    csv_writer = csv.writer(open("amazon.csv", mode="w"))
    label_printed = False
    amazon_map = {}
    for index, search_term in enumerate(search_terms):
        product_map = scrape(search_term, delay=delay, suppress_labels=(index != 0), url_version=url_version)
        if len(product_map) == 0:
            continue

        if len(amazon_map) != 0:
            for key in amazon_map.keys():
                if key in product_map.keys():
                    amazon_map[key] = amazon_map[key] + [product_map[key]]
                else:
                    amazon_map[key] = amazon_map[key] + [""]
        else:
            for key in product_map.keys():
                amazon_map[key] = [product_map[key]]

    csv_writer.writerow(list(amazon_map.keys()))

    # number of rows is number of items in list for first key
    key_list = list(amazon_map.keys())
    print(amazon_map)
    for i in range(len(amazon_map[key_list[0]])):
        row = [amazon_map[key][i] for key in amazon_map.keys()] # get ith element in each key's list
        csv_writer.writerow(row)

def scrape(search_term, delay=0, suppress_labels=False, url_version=1):
    url = get_url(search_term) if url_version == 1 else get_url_v2(search_term)
    headers = {'User-Agent': 'Mozilla/{}.0 (Windows NT 6.1) {} Chrome/{}.0.2228.0 Safari/537.36'.format(
        random.randint(1, 6), random.choice(["", "AppleWebKit/537.36 (KHTML, like Gecko)"]), random.randint(1, 41))}
    request = requests.get(url, headers=headers)
    doc = html.fromstring(request.content)
    try:
        title = doc.xpath("//h1[@id='title']//text()")[1].replace("\n", "").strip()
        author = doc.xpath("//a[@class='a-link-normal contributorNameID']//text()")[0]
        reviews = doc.xpath("//span[@id='acrCustomerReviewText']//text()")[0]
        reviews = reviews[:reviews.find(" ")].replace(",", "")
        # rating = doc.xpath("//span[@class='arp-rating-out-of-text a-color-base']//text()")[0]
        # rating = rating[:rating.find(" ")]
        category = doc.xpath("//span[@class='cat-link']//text()")
        first_review = doc.xpath("//div[@class='a-row a-spacing-small review-data']//text()")
        first_review = first_review[: first_review.index("\n  ")]
        first_review = " ".join(first_review)

        stuff = doc.xpath("//td[@class='bucket']//div[@class='content']//li//text()")
        stuff = [elem.replace("\n", "").strip() for elem in stuff if elem.replace("\n", "").strip() != "" and "{" not in elem and len(elem) > 3]

        price = doc.xpath("//span[@class='a-size-medium a-color-price offer-price a-text-normal']//text()")[0]

        description = doc.xpath("//div[@id='bookDescription_feature_div']//text()")
        description = [val for val in description if "\n" not in val and val !=
                   " " and "Read" not in val]
        description = "".join(description)
        # Read to get rid of read more, read less

        new_stuff = []

        for index, value in enumerate(stuff):
            if value[-1] == ":" or stuff[index - 1][-1] == ":":
                new_stuff.append(value)

        labels = ["Title", "Author", "Reviews", "Price"] + [val[:-1] for val in new_stuff[::2]] + ["User Review", "Description"]

        values = [title, author, reviews, price]

        for val in new_stuff[1::2]:
            values.append(val[:-2] if val.endswith(" (") else val)

        values.extend([first_review, description])

        if not suppress_labels:
            print(labels)
        print(values[0])

    except:
        print("Error")
        return {}
    time.sleep(delay)

    return dict(zip(labels, values))

# slower, but always gets correct book
def get_url(search_term):
    results = search(search_term + " amazon", stop=1)
    for result in results:
        if "amazon.com" in result:
            return result

#faster, but is susceptible to more url errors, such as retrieving url of an ad
def get_url_v2(search_term):
    amazon_url = "https://www.amazon.com/s?k={}&ref=nb_sb_noss_2".format(search_term.replace(" ", "+"))
    headers = {'User-Agent': 'Mozilla/6.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0'}
    request = requests.get(amazon_url, headers=headers) # slowest statement
    doc = html.fromstring(request.content)
    url = "https://www.amazon.com" + doc.xpath("//a[@class='a-link-normal']")[0].attrib['href']
    return url
