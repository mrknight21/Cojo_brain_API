    ## draft datastructure for user preference and news object
    # user_prf =
    # {
    # "read_amount": 40,
    # "size": {"weight":0.9,"s":0.6, "m":0.2,"l":0.2},
    # "categories": {"weight": 0.7, "b":0.05, "e":0.1, "p":0.4, "s":0.15, "t":0.3},
    # ...,
    # ...,
    # ...,
    #     }
    #
    # news = {
    # ...,
    # ...,
    # ...,
    # 'size': 's',
    # 'categories': 'p'
    #     }





##calculate score for each news
def cal_score(news, user_prf):
    score = 1
    for key in user_prf:
        if (key == 'read_amount'):
            continue
        else:
            score = score = score*user_prf[key]["weight"]*user_prf[key][news[key]]
    return score

##rank a list of news
def news_rank(newsl, user_prf):
    newsl.sort(key=lambda k: cal_score(k, user_prf), reverse=True)

