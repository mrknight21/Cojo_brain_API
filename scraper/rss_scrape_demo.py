import requests
from bs4 import BeautifulSoup
from newspaper import Article
import newspaper
import json








def save_news(news, path):
    with open(path, 'w') as outfile:
        json.dump(news, outfile)

def download_news(url):
    newsp = newspaper.build(url)
    news = []
    for article in newsp.articles:
        new = get_content(article)
        news.append(new)
    return news




def get_content(article):
    new = {}
    article.download()
    article.parse()
    article.nlp()
    new['title'] = article.title
    ##https://stackoverflow.com/questions/10624937/convert-datetime-object-to-a-string-of-date-only-in-python
    new['pubdate'] = article.publish_date
    new['author'] =article.authors
    new['link'] = article.url
    new['content'] = article.text
    new['kw'] = article.keywords
    return new





def main():
    collection = download_news("")



    # url = "https://www.radionz.co.nz/rss/political.xml"
    # resp = requests.get(url)
    # print(resp)
    # soup = BeautifulSoup(resp.content, features="lxml")
    # items = soup.findAll('item')
    # news_items = []
    # for item in items:
    #     news_item = {}
    #     news_item['title'] = item.title.text
    #     news_item['description'] = item.description.text
    #     news_item['link'] = item.link.text
    #     news_item['pubdate'] = item.pubdate.text
    #     article = Article(news_item['link'])
    #     article.download()
    #     print(item)
        # article.parse()
        # content = article.text
        # news_item['content'] = content
        # print(news_item['title'],  news_item['content'])
        # news_items.append(news_item)



if __name__ == "__main__":
    main()