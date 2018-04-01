from newspaper import Article
import newspaper
import json
import csv
import datetime
import feedparser
import re
from db_management.config import db_connect
from firebase_admin import db
import csv


class Scraper:

    def __init__(self, load_db = True, load_path = None, save_path= None):
        self.load_path = load_path
        self.save_path = save_path
        self.news = []
        self.source ={}
        if(load_db == True):
            self.ref = db.reference("/sources")
            self.source = self.ref.get()
        else:
            with open(load_path, 'r') as f:
                reader = csv.reader(f)
                for name, link in list(reader):
                    self.source[name]= link



    def create_time_stamp(self):
        now = datetime.datetime.now()
        return now.strftime("%Y%m%d_%H%M")


    def save_news_json(self):
        with open(self.save_path, 'w') as outfile:
            json.dump(self.news, outfile)

    def db_news_push(self):
        ref = db.reference("/news_pool")
        jsform = {}
        for news in self.news:
            id = news['source']+" "+news['pubdate']
            jsform[id] = news
        ref.update(jsform)


    ##using the built() function from the newspaper lib to scrape all news from a given homepage. It is powerful, but the result is not very stable, so will not use it that often.
    # def download_newsite(url):
    #     newsp = newspaper.build(url)
    #     print("number of articles: ", len(newsp.articles))
    #     news = []
    #     for article in newsp.articles:
    #         new = get_content(article)
    #         news.append(new)
    #     return news

    ##use the python feedparser to get basic informations
    def download_rss(self):
        for key, value in self.source.items():
            feed = feedparser.parse(value)
            feed_entries = feed.entries
            print("number of articles: ", len(feed_entries))
            for entry in feed.entries:
                new={}
                new["title"] = entry.title
                new["description"] = re.sub('<.*?>', '', entry.description).strip(' \t\n\r')
                new["source"]= key
                new["link"] = entry.link
                new["pubdate"] = entry.published
                new = {**new, **self.get_content(url=entry.link)}
                print(entry.title)
                self.news.append(new)




        # resp = requests.get(url)
        # print(resp)
        # soup = BeautifulSoup(resp.content, features="lxml")
        # items = soup.findAll('item')
        # news_items = []
        # for item in items:
        #     print(item.link.text)
             # news_item = {}
             # news_item['title'] = item.title.text
             # news_item['description'] = item.description.text
             # news_item['link'] = item.link.text
             # news_item['pubdate'] = item.pubdate.text
             # article = Article(news_item['link'])
             # article.download()
             # print(item)
             # article.parse()
             # content = article.text
             # news_item['content'] = content
             # print(news_item['title'],  news_item['content'])
             # news_items.append(news_item)

    def news_clear(self):
        self.news = []

    ##use newspaper package's Article object to dig into the contents, and do further analysis and tagging
    def get_content(self, url):
        new = {}
        article = Article(url)
        article.download()
        article.parse()
        ##article.nlp()
        content = article.text
        ##new['kw'] = article.keywords
        return new


def main():
    scraper = Scraper(load_db=False, load_path="reuter_news_dump.json")
    scraper.download_rss()


if __name__ == "__main__":
    main()