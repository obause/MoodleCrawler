# import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

from .CrawledCourse import CrawledCourse


class ArticleFetcher:
    def fetch(self):
        url = "http://python.beispiel.programmierenlernen.io/index.php"

        while url != "":
            print(url)
            # time.sleep(1)
            r = requests.get(url)
            doc = BeautifulSoup(r.text, "html.parser")

            for card in doc.select(".card"):
                emoji = card.select_one(".emoji").text
                content = card.select_one(".card-text").text
                title = card.select(".card-title span")[1].text
                image = urljoin(url, card.select_one("img").attrs["src"])

                yield CrawledCourse(title, emoji, content, image)

            next_button = doc.select_one(".navigation .btn")
            if next_button:
                next_href = next_button.attrs["href"]
                next_href = urljoin(url, next_href)
                url = next_href
            else:
                url = ""

    def print_articles(self, count):
        articles = self.fetch()
        if count == -1:
            count = 999999999
        counter = 0
        for article in articles:
            if counter >= count:
                break
            print("")
            print(article.emoji + ": " + article.title)
            print(article.content)
            counter += 1

    def export_csv(self):
        with open('articles.csv', 'w', newline='', encoding='utf-8') as csvfile:
            articlewriter = csv.writer(csvfile, delimiter=";", quotechar='"')
            for article in self.fetch():
                articlewriter.writerow([article.emoji, article.title, article.image, article.content])
