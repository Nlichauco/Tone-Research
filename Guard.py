from Funcs import *

import pandas as pd


s_dates=StartDates("G")
e_dates=endDates("G")
scores = [1]
for i in range(0,len(s_dates)):
    fname=s_dates[i][:2] + "." + s_dates[i][2:] + "-" + e_dates[i][:2] + "." + e_dates[i][2:] + ".csv"
    que="""https://content.guardianapis.com/search?section=business&q=coronavirus&type=article&edition=uk&from-date=2020-"""+s_dates[i]+"&to-date=2020-"+e_dates[i]+"&show-fields=bodyText&api-key=7735070e-6108-49c2-80bc-a6a7898d725b"""
    texts,articles,amt=Gpull(que)
    print(amt)
    print("hit \n")
    if amt<1:
        arts=list()
        arts.append(Article("source","date","url"))
        CreateCSV(arts,fname,scores)
        #If there are no articles returned skip to the next week.
        continue
    print("made it past")
    #texts,token_texts=GetText(urls)
    scores.append(1)
    # scores=GetScore(token_texts,newdict)
    #Get scores from the lexicon, this may or may not be removed, just because we aren't really using it.
    articles=createArts(articles,texts)
    CreateCSV(articles,fname,scores)
    print(i,"/n")

def get_avg_daily_cases(file_name):
    avg = []
    count = 0
    my_sum = 0
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        is_first = 1
        for row in csv_reader:
            if is_first:
                is_first ^= 1
            else:
                count += 1
                if not row[4].isnumeric():
                    break
                my_sum += int(row[4])
                if count == 7:
                    avg.append(my_sum / 7)
                    count = 0
                    my_sum = 0
