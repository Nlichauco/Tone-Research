from Funcs import*

# In one iteration of this for loop, the program grabs one weeks worth of articles from the API,
# creates an article class obj for each article with the meta data given from the API response.
# Grabs the text of each article in that week.
# Scores the text of each article, and updates the article obj to hold those scores.
# Finally it creates one CSV pertaining to the given week with the article class objs from that iteration.

s_dates=["0101","0108","0115","0122","0201","0208","0215","0222","0301","0308","0315","0322","0401","0408","0415","0422","0501","0508","0515","0522","0601","0608","0615","0622","0701","0708"]
e_dates=["0107","0114","0121","0131","0207","0214","0221","0229","0307","0314","0321","0331","0407","0414","0421","0430","0507","0514","0521","0531","0607","0614","0621","0630","0707","0714"]

newdict=DictCSV("wkwlex.tab",0,2) #Read a lexicon.

#https://api.nytimes.com/svc/search/v2/articlesearch.json?q=coronavirus&page=0&fq=news_desk:("Sports")&source:("The New York Times")&facet=true&sort=relevance&begin_date=20200101&end_date=20200107&api-key=d6ZZ3CclPNtLfkZid9iUvs6HpYLEbehl
#que="""https://api.nytimes.com/svc/search/v2/articlesearch.json?q=coronavirus&page=0&fq=news_desk:("Sports")&source:("The New York Times")&facet=true&begin_date=20191201&end_date=20200629&api-key=d6ZZ3CclPNtLfkZid9iUvs6HpYLEbehl"""
for i in range(0,len(s_dates)):

    fname="week"+str(i)+".csv"

    #que="""https://api.nytimes.com/svc/search/v2/articlesearch.json?q=coronavirus&page=0&fq=news_desk:("Health")&source:("The New York Times")&facet=true&begin_date=20191201&end_date=20200629&api-key=d6ZZ3CclPNtLfkZid9iUvs6HpYLEbehl"""
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
    count=0
    #Loop through article texts
    for text in texts:
        article=articles[count]
        #Iterate through each article class, each 'text', corresponds to a single article
        tscores,tones=IBMtone(text)
        #Get tone scores and tones from IBM

        AssignTone(tscores,tones,article)
        #AssignTone scores takes the scores from IBM and adds them to that specific article object.
        count+=1

    with open(fname, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Source", "Date", "URL","Score","   ","Anger","Fear","Joy","Sad","Analy","Confi","Tenta"])
        rcount=0
        for a in articles:
            #writer.writerow([a.source, a.published,a.url,scores[count]," ",%.2f,a.fear,a.joy,a.sadness,a.analytical,a.confidence,a.tentative])
            writer.writerow([a.source, a.published,a.url,scores[rcount]," ",a.anger,a.fear,a.joy,a.sadness,a.analytical,a.confidence,a.tentative])
            rcount+=1
    #This section could be replaced by the CreateCSV() function.






#urls,arts=Pull(que)
#GetText(urls)
