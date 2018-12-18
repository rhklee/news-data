import requests
from urllib.parse import urlparse
from collections import namedtuple
from bs4 import BeautifulSoup
import re

NYTIMES_BASE_URL = "https://spiderbites.nytimes.com"
TIME_PERIOD = range(1994, 2018 + 1)
MONTHS = range(1, 13)
CSV_FILENAME = "nytimes_headlines.csv"

Headline = namedtuple('Headline', ['title', 'date', 'url'])

def create_articles_path(base_url: str, 
                         year: int, 
                         month: int, 
                         part: int) -> str:
    return "{}/{}/articles_{}_{}_{}.html".format(base_url, 
        str(year), str(year), str(month).zfill(2), str(part).zfill(5))


def get_articles(url: str) -> []:
    response = requests.get(url)

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = soup.find("ul", id="headlines").find_all("a")

    return [ Headline(h.getText(), get_date_from_url(h.get("href")), h.get("href")) 
                for h in headlines ]


def get_date_from_url(url: str) -> str:
    pattern = re.compile('\d{4,4}/(1[0-2]|0\d)/\d{2,2}')

    str_date = urlparse(url).path[1:11]

    if pattern.match(str_date) is None:
        return None
    return str_date

def format_csv_row(headline: Headline) -> str:
    return "\"{}\",\"{}\",\"{}\"\n".format(headline.title, 
        headline.date, headline.url)

def write_data(articles: []) -> None:
    with open(CSV_FILENAME, "a") as file:
        for article in articles:
            file.write(format_csv_row(article))

def scrape_nytimes():
    for year in TIME_PERIOD:
        for month in MONTHS:
            part = 0
            while True:
                print("Year: {} - Month: {} - Part: {}".format(year, month, part))
                articles_path = create_articles_path(NYTIMES_BASE_URL, 
                                                    year,
                                                    month,
                                                    part)
                articles = get_articles(articles_path)
                # print(articles)
                if not articles:
                    break
                write_data(articles)
                part+=1

if __name__ == "__main__":
    scrape_nytimes()