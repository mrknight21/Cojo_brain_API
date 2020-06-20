# Cojo_brain_API
Cojo is a intelligent news feeder, that aims to improve reader's reading habit and visions. C stands for either "civil" or 
"compound", and "Ojo" means "eyes" in Spanish. This project aims to help people broaden their vision beyond their own social bubble,
by allowing fast vision exchanging between individuals.

For more information about the Cojo project please read the medium article:

https://medium.com/@fadingcicadaz/cojo-the-concept-of-digital-diet-and-the-smart-digital-feeder-1aeee156fa0

## Data Model

** Due to the fact that firestore is currently the primary database, the primary data structure whill based on Firestores's primary data strcutures

### 1. Article object (Path: news_articles)

Description: object that store the information for a news article.

** The 'label' is to be used for fornt end display.

```
{
  '_id': 'xxxxxxxxxxxxxx' (12 cahracters, String) (Required)
  'url': 'https://www.xxxx.com' (String) (Required),
  'downloadedAt': (Timestamp)(2020, 4, 12, 1, 27, 14, 210148, tzinfo=<UTC>)(Required),
  'country': 'us' (String) (Required),
  'source_domain': 'www.inquirer.com',
  'urlToImage': 'https://www.xxxx.com' (String) (Optional),
  'bag': {},
  'main_category': 'business' (String) (Required),
  'tag': {'reading_time': 6 (Int),
  'words_count': 29 (Int),
  'polarity': 0.5 (Int),
  'subjectivity': 0.5 (Int)},
  'author': 'Jacob Bogage' (String) (Optional),
  'language': 'en' (String) (Required),
  'description': 'xxxxxxxxxxxxxx' (String) (Required),
  'source': {'id': None, 'name': 'Inquirer.com'} (To be updated),
  'categories': [] (Arrat:String) (Optional),
  'publishedAt': (Timestamp)(2020, 4, 12, 1, 27, 14, 210148, tzinfo=<UTC>)(Required),
  'title': 'xxxxxxxxxxxxxx' (String) (Required)
 }

```

### 2. Sources object (Path: source_domains/..domain['article_sources'])

Description: object that store the link information that are essential for scraping and subscription, nesting inside domain object.

```
{
  '_id': 'xxxxxxxxxxxxxx' (16 cahracters, String) (Required) **the _id is usually source domain + 4 digits
  "url": 'https://www.xxxx.com' (String) (Required),
  "crawler": "RssCrawler" (String) (Optional) Default:"RssCrawler",
  "meta_data": {
  "main_category": "sport", (String) (Required)
  "headline": True (Boolean) (Optional) Default: false,
  "categories":["government"] (Array:String) (Optional) Default: []
  },
  "label":"Sport" (String) (Required)
},
```


### 3. Domain object (Path: source_domains)

Description: object that store the domain information that are essential for scraping and subscription.

```
{
  "domain_name" : "xxxxxxxxxxxx", (12 cahracters, String) (Required)
  "description" : "xxxxxxxxxxxx", (String) (Optional)
  "domain_url" : 'https://www.xxxx.com' (String)(Required),
  "icon_image_link" : 'https://www.xxxx.com' (String) (Optional),
  "language" : "en" (String)(Required),
  "country" : "nz" (String)(Required),
  "tags" : {},
  "media_type":"newspaper"  (String) (Optional),
  "interaction": {}, (To be updated)
  "analysis":{}, (To be updated)
  "article_sources":[source_obj] (Array: Source)
```


## API Calls

### 1. ping

Description:a simple API call that check if the server is alive.

Consumption Detail:

```

End point: http://cojo.co.nz/news_api/ping
Method:POST,GET

Body:
None

Output:

STATUS 200:
"Ping!" (String)
```


### 2. user news cache update

Description: reset or increment more recent news article into user's cach in the firebase.

Consumption Detail:

```

End point: http://cojo.co.nz/news_api/update
Method:POST
Body:
{
  "user_id": "xxxxxxx" (String) (Required),
  "auth_token": "xxxxxxx" (Sring) (Required), *To be updated,
  "reset": "True/False" (Boolean/String) Default value: False *To be updated,
  "return_cache": "True/False" (Boolean/String) Default value: False *To be updated
}

Output:

STATUS 200:
{
"user_id": "IMUJzv9y06SPDsIVLNRsjKaKUGi1",
"complete": true,
"total_news": 40,
"message": ""

If "return_cache" was true in request:
"ranked_news": [
    news_article_json(refer to Data Model news_article),
    ...,
    ...
]
}

```


