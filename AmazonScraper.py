from googlesearch import search
import csv
import requests
from lxml import html
import time
import random

def scrape_multiple(search_terms, delay=1):
    for index, search_term in enumerate(search_terms):
        scrape(search_term, delay=delay, suppress_labels=(index!=0))

def scrape(search_term, delay=0, suppress_labels=False):
    start_time = time.time()
    url = get_url_v2(search_term)
    print("Url time: {}".format(time.time() - start_time))
    headers = {'User-Agent': 'Mozilla/{}.0 (Windows NT 6.1) {} Chrome/{}.0.2228.0 Safari/537.36'.format(
        random.randint(1, 6), random.choice(["", "AppleWebKit/537.36 (KHTML, like Gecko)"]), random.randint(1, 41))}
    request = requests.get(url, headers=headers)
    doc = html.fromstring(request.content)
    try:
        title = doc.xpath("//h1[@id='title']//text()")[1].replace("\n", "").strip()
        author = doc.xpath("//a[@class='a-link-normal contributorNameID']//text()")[0]
        reviews = doc.xpath("//span[@id='acrCustomerReviewText']//text()")[0]
        reviews = reviews[:reviews.find(" ")].replace(",", "")
        rating = doc.xpath("//span[@class='arp-rating-out-of-text a-color-base']//text()")[0]
        rating = rating[:rating.find(" ")]
        category = doc.xpath("//span[@class='cat-link']//text()")

        # stuff = doc.xpath("//td[@class='bucket']//div[@class='content']//li//text()")
        # stuff = [elem.replace("\n", "").strip() for elem in stuff if elem.replace("\n", "").strip() != "" and "{" not in elem and len(elem) > 3]

        #summary = doc.xpath("//div[@id='iframeContent']")

        if not suppress_labels:
            print(["Url", "Title", "Author", "Reviews", "Rating", "Category"])
        print([url, title, author, reviews, rating, category])

    except:
        print("Error")
    print("Total time: {}".format(time.time() - start_time))
    time.sleep(delay)

def get_url(search_term):
    results = search(search_term + " amazon", stop=1)
    for result in results:
        if "amazon.com" in result:
            return result

def get_url_v2(search_term):
    amazon_url = "https://www.amazon.com/s?k={}&ref=nb_sb_noss_2".format(search_term.replace(" ", "+"))
    headers = {'User-Agent': 'Mozilla/6.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0'}
    request = requests.get(amazon_url, headers=headers)
    doc = html.fromstring(request.content)

    url = "https://www.amazon.com" + doc.xpath("//a[@class='a-link-normal']")[0].attrib['href']
    return url
