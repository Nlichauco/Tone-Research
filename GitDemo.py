from Funcs import*

def endDates():
    def daterange(date1, date2):
        for n in range(6,int ((date2 - date1).days)+1,7):
            yield date1 + timedelta(n)
    e_dates=[]
    start_dt = date(2020, 1, 1)
    end_dt = date(2020, 7, 29)
    for dt in daterange(start_dt, end_dt):
        e_dates.append(dt.strftime("%m%d"))
    return e_dates

def StartDates():
    def daterange(date1, date2):
        for n in range(0,int ((date2 - date1).days),7):
            yield date1 + timedelta(n)
    s_dates=[]
    start_dt = date(2020, 1, 1)
    end_dt = date(2020, 7, 29)
    for dt in daterange(start_dt, end_dt):
        s_dates.append(dt.strftime("%m%d"))
    return s_dates


newdict=DictCSV("wkwlex.tab",0,2)
s_dates=StartDates()
e_dates=endDates()
for i in range(0,len(s_dates)):
    fname="week"+str(i)+".csv"
    que="""https://api.nytimes.com/svc/search/v2/articlesearch.json?q=coronavirus&page=0&fq=news_desk:("Politics")&source:("The New York Times")&facet=true&sort=relevance&begin_date=2020"""+s_dates[i]+"&end_date=2020"+e_dates[i]+"&api-key=d6ZZ3CclPNtLfkZid9iUvs6HpYLEbehl"
    urls,articles,amt=Pull(que)
    print(amt)
    print("hit \n")
    if amt<1:
        #If there are no articles returned skip to the next week.
        continue
    print("made it past")
    texts,token_texts=GetText(urls)
    #texts for the IBM tone analyzer, token_texts for the lexicon score.
    scores=GetScore(token_texts,newdict)
    #Get scores from the lexicon, this may or may not be removed, just because we aren't really using it.
    articles=createArts(articles,texts)
    CreateCSV(articles,fname,scores)
