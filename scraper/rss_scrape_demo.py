import requests
from bs4 import BeautifulSoup
from newspaper import Article
import newspaper
import json
import csv
import datetime
import feedparser





def create_time_stamp():
    now = datetime.datetime.now()
    return now.strftime("%Y%m%d_%H%M")


def save_news_json(path, news):
    with open(path, 'w') as outfile:
        json.dump(news, outfile)




def save_news_csv(path,news):
    try:
        with open(path, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=news[0].keys())
            writer.writeheader()
            for data in news:
                writer.writerow(data)
    except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
    return





def download_newsite(url):
    newsp = newspaper.build(url)
    print("number of articles: ", len(newsp.articles))
    news = []
    for article in newsp.articles:
        new = get_content(article)
        news.append(new)
    return news

def download_rss(url):
    feed = feedparser.parse(url)
    feed_title = feed['feed']['title']
    feed_entries = feed.entries
    print("number of articles: ", len(feed_entries))
    news = []
    for entry in feed.entries:
        new = get_content(entry.link)
        print(entry.title)
        news.append(new)
    return news




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




def get_content(url):
    new = {}
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()
    print(article.title)
    new['title'] = article.title
    ##https://stackoverflow.com/questions/10624937/convert-datetime-object-to-a-string-of-date-only-in-python
    new['pubdate'] = article.publish_date
    ##new['author'] =article.authors
    new['link'] = article.url
    ##For training convenience I will scrape the content in here, but in production, content will be used to extracting features but will not be stored in database.
    ##new['content'] = article.text
    new['kw'] = article.keywords
    new['sum'] = article.summary
    return new





def main():
    #collection = download_news("https://www.stuff.co.nz/")
    #save_news_csv(collection, "scraper/news_dump.csv")
    collection = download_rss("http://rss.nzherald.co.nz/rss/xml/nzhtsrsscid_000000698.xml")
    print(len(collection))
    save_news_json("heral_news_dump.json", collection)






if __name__ == "__main__":
    main()