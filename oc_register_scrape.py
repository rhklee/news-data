from bs4 import BeautifulSoup
import requests


OC_REGISTER_BASE_ENDPOINT = "https://www.ocregister.com/{}/page/{}/"

def create_page_endpoint(year, pageNum):
    return OC_REGISTER_BASE_ENDPOINT.format(year, pageNum)

def get_titles_only(soup, titles, f):
    divTitles = soup.find_all("span", class_="dfm-title")
    for divTitle in divTitles:
        title = divTitle.getText().replace('\n', '').strip()
        print(title)
        if title in titles:
            continue

        titles.add(title)
        f.write(title)

def cleanText(t):
    return t.replace('\n', '').strip()

def get_article_info(soup, titles, file):
    articleDivs = soup.find_all("div", class_="article-info")

    for ad in articleDivs:
        title = cleanText(ad.find("a", class_="article-title").get("title"))
        url = cleanText(ad.find("a", class_="article-title").get("href"))
        meta = ad.find("div", class_="entry-meta")
        author = cleanText(meta.find("div", class_="byline").find("a").getText())
        date = cleanText(ad.find("time").get("datetime"))
        line = "\"{}\",\"{}\",\"{}\",\"{}\"\n".format(date, title, author, url)
        print(line)
        file.write(line)


def doSomething():
    titles = set()

    with open('oc_reg_titles.csv', 'w') as f:
        for year in range(2005, 2019):
            pageNum = 1

            while(True):
                pageOfContent = requests.get(create_page_endpoint(year, pageNum)).text
                soup = BeautifulSoup(pageOfContent, 'html.parser')

                get_article_info(soup, titles, f)

                nextPage = soup.find_all("a", class_="load-more")
                if len(nextPage) == 0:
                    break

                pageNum += 1




if __name__ == '__main__':
    doSomething()

    

