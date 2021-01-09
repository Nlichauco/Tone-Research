from Funcs import*

def getDate(q):
    def daterange(date1, date2):
        add = 1 if q == 6 else 0
        for n in range(q, int((date2 - date1).days) + add, 7):
            yield date1 + timedelta(n)

    end_date = []
    start_dt = date(2020, 3, 1)
    end_dt = date(2020, 12, 26)
    for dt in daterange(start_dt, end_dt):
        end_date.append(dt.strftime("%m%d"))
    return end_date


# newdict=DictCSV("wkwlex.tab",0,2)
s_dates = getDate(0)
e_dates = getDate(6)
scores = []
for i in range(32,len(s_dates)):
    fname = s_dates[i][:2] + "." + s_dates[i][2:] + "-" + e_dates[i][:2] + "." + e_dates[i][2:] + ".csv"
    que = """https://api.nytimes.com/svc/search/v2/articlesearch.json?q=coronavirus&page=0&fq=news_desk:(
    "business")&source:("The New York Times")&facet=true&sort=relevance&begin_date=2020""" + \
          s_dates[i] + "&end_date=2020" + e_dates[i] + "&api-key=aiPyJZEGATr7l0XfQGsBpQ3loDqzteIC"
    #que="""https://api.nytimes.com/svc/search/v2/articlesearch.json?q=coronavirus&page=0&fq=news_desk:("Politics")&source:("The New York Times")&facet=true&sort=relevance&begin_date=2020"""+s_dates[i]+"&end_date=2020"+e_dates[i]+"&api-key=d6ZZ3CclPNtLfkZid9iUvs6HpYLEbehl"
    urls,articles,amt=Pull(que)
    print(amt)
    print("hit \n")
    if amt<1:

        #If there are no articles returned skip to the next week.
        continue
    print("made it past")
    texts,token_texts=GetText(urls)
    scores.append(1)
    #texts for the IBM tone analyzer, token_texts for the lexicon score.
    # scores=GetScore(token_texts,newdict)
    #Get scores from the lexicon, this may or may not be removed, just because we aren't really using it.
    articles=createArts(articles,texts)
    CreateCSV(articles,fname,scores)
