# Cojo_brain_API
Cojo is a intelligent news feeder, that aims to improve reader's reading habit and visions. C stands for either "civil" or 
"compound", and "Ojo" means "eyes" in Spanish. This project aims to help people broaden their vision beyond their own social bubble,
by allowing fast vision exchanging between individuals.

For more information about the Cojo project please read the medium article:

https://medium.com/@fadingcicadaz/cojo-the-concept-of-digital-diet-and-the-smart-digital-feeder-1aeee156fa0

## Data Model

```
## To be updated...

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


