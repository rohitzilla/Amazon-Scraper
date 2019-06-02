from AmazonScraper import scrape, scrape_multiple
from bs4 import BeautifulSoup

page = BeautifulSoup(open("/Users/rohitneppalli/Library/Mobile Documents/com~apple~CloudDocs/Documents/workspace/Python/Python/src/text.txt", "r"), "html.parser")

books = [span.text for span in page.find_all("span", attrs={"class": "text-info"})][:10]

scrape_multiple(books, delay=1)

#scrape_multiple(["The Boys in the Boat"], delay=0, url_version=1)