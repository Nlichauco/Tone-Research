import json
import requests
import pyjq
from bs4 import BeautifulSoup
import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, RegexpTokenizer
import csv
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
import re
import glob
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
import os
import pandas as pd
import statistics as stat
from natsort import natsorted, ns






"""
Gets averages of given list of week class objects.

Args:
    Weeks: A list of week class objects.

Returns:
    full list of average score per week, one per tone (7 in total)"""

def GetAvgs(weeks):
    Sad_mean=[]
    Fear_mean=[]
    Anger_mean=[]
    Tenta_mean=[]
    Joy_mean=[]
    Confi_mean=[]
    Analy_mean=[]
    for week in weeks:
        Sad_mean.append(week.Sadness.get_mean())
        Confi_mean.append(week.Confi.get_mean())
        Anger_mean.append(week.Anger.get_mean())
        Fear_mean.append(week.Fear.get_mean())
        Joy_mean.append(week.Joy.get_mean())
        Analy_mean.append(week.Analy.get_mean())
        Tenta_mean.append(week.Tenta.get_mean())
    return Sad_mean,Fear_mean,Anger_mean,Tenta_mean,Joy_mean,Confi_mean,Analy_mean



"""
Reads through article class objs and creates CSV for that week.

Args:
    articles: List of articles from the same week.
    fname: desired name of CSV.
    scores: Scores from lexicon.

Returns:
    Nothing, creates file in directory"""

def CreateCSV(articles,fname,scores):
    with open(fname, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Source", "Date", "URL","Score","   ","Anger","Fear","Joy","Sad","Analy","Confi","Tenta"])
        rcount=0
        for a in articles:
            #writer.writerow([a.source, a.published,a.url,scores[count]," ",%.2f,a.fear,a.joy,a.sadness,a.analytical,a.confidence,a.tentative])
            writer.writerow([a.source, a.published,a.url,scores[rcount]," ",a.anger,a.fear,a.joy,a.sadness,a.analytical,a.confidence,a.tentative])
            rcount+=1


"""
Reads all of the CSVS and returns a list of week class objs.

Reads one CSV per iteration of the given "section" pathname, puts each CSV into an article class.

Args:
    Path: The path to a section file, section file contains all CSVS pertaining to that section (each CSV represents a week).


Returns:
    A list of week class objs, One for each CSV"""

def ReadSection(path):
    missing_values=["NaN","0"]
    #print(os.listdir(path))
    list_weeks=list()
    for filename in natsorted(os.listdir(path), key=lambda y:y.lower()):


        if not filename.startswith('.'):
            #print(filename,"\n")
            week=Week(str(filename[0:-4]))
            with open(os.path.join(path, filename)) as f:


                data=pd.read_csv(f, header=0,sep=r'\s*,\s*',na_values=missing_values,engine='python',usecols=[0,1,2,5,6,7,8,9,10,11])
                for ind in data.index:
                    article=Article(data['Source'][ind],data['Date'][ind], data['URL'][ind])


                    article.analytical=data['Analy'][ind]
                    article.sadness=data['Sad'][ind]
                    article.confidence=data['Confi'][ind]
                    article.anger=data['Anger'][ind]
                    article.tentative=data['Tenta'][ind]
                    article.fear=data['Fear'][ind]
                    article.joy=data['Joy'][ind]


                    #print(article.sadness,"    ", article.url)
                    week.add_Art(article)
                list_weeks.append(week)
    return list_weeks



class toneStat:
    """toneStat class which can grab median, max and avg from a weeks dataset.

    The toneStat class is inside the weeks class, it is used to get stats about the week.

    Attributes:
        Tone: Each toneStat class obj is responsible for one tone, the 'Tone' attribute holds the label to keep track of tones.
        Tone_Scores: the array which holds all scores associated with the Tone.
    """
    def __init__(self,tonename):
        self.Tone=tonename
        self.Tone_scores=[]
    def add_score(self,score):
        #add a tone score to the array
        self.Tone_scores.append(score)
    def get_mean(self):
        sum=0
        count=0
        for score in self.Tone_scores:
            if score>.5:
                sum+=score
                count+=1
        if sum!=0:
            return (sum/count)
        else:
            return .5
    def get_median(self):
        return stat.median(self.Tone_scores)
    def get_max(self):
        return max(self.Tone_scores)
    def get_perc(self):
        total=len(self.Tone_scores)
        if total==0:
            return 0
        else:
            sum=0
            for num in self.Tone_scores:
                if num > .5:
                    sum+=1
            return (sum/total)





    """
    Writes data from Weeks class to CSV.

    Creates CSV with week by week data of a the current "section" (i.e. ('sports','science','buisness'))

    Args:
        Weeks: A list of week class objects.
        Section: The new desk where the data was taken from, this will be the label of the csv.

    Returns:
        Nothing. Writes a 'section'.csv file in the current directory."""

def weekwrite(weeks,section):
    fname=section+".csv"
    with open(fname, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Week","Anger_max", "Anger_med","Anger_avg","Sad_max","Sad_median","Sad_avg","Fear_max","Fear_med","Fear_avg","Joy_max","Joy_med","Joy_avg","Analy_max","Analy_med","Analy_avg","Confi_max","Confi_med","Confi_avg","Tenta_max","Tenta_med","Tenta_avg"])
        rcount=0
        for week in weeks:
            Anger_median=week.Anger.get_median()
            Anger_max=week.Anger.get_max()
            Anger_mean=week.Anger.get_mean()
            Sad_median=week.Sadness.get_median()
            Sad_max=week.Sadness.get_max()
            Sad_mean=week.Sadness.get_mean()
            Fear_median=week.Fear.get_median()
            Fear_max=week.Fear.get_max()
            Fear_mean=week.Fear.get_mean()
            Joy_median=week.Joy.get_median()
            Joy_max=week.Joy.get_max()
            Joy_mean=week.Joy.get_mean()
            Analy_median=week.Analy.get_median()
            Analy_max=week.Analy.get_max()
            Analy_mean=week.Analy.get_mean()
            Confi_median=week.Confi.get_median()
            Confi_max=week.Confi.get_max()
            Confi_mean=week.Confi.get_mean()
            Tenta_median=week.Tenta.get_median()
            Tenta_max=week.Tenta.get_max()
            Tenta_mean=week.Tenta.get_mean()
            writer.writerow([week.weekname, Anger_max,Anger_median,Anger_mean,Sad_max,Sad_median,Sad_mean,Fear_max,Fear_median,Fear_mean,Joy_max,Joy_median,Joy_mean,Analy_max,Analy_median,Analy_mean,Confi_max,Confi_median,Confi_mean,Tenta_max,Tenta_median,Tenta_mean])


class Week:
    """Week class which holds all tone data from a singular week.

    Week class has all tone data for that week.

  Attributes:
      weekname: weekname is there to be able to identiy different weeks.
      List_Arts: A list of article class objects.
     """

    def __init__(self, week_name):
        self.weekname=week_name
        self.List_Arts=list()
        self.Sadness=toneStat("Sadness")
        self.Anger=toneStat("Anger")
        self.Tenta=toneStat("Tenta")
        self.Joy=toneStat("Joy")
        self.Analy=toneStat("Analy")
        self.Confi=toneStat("Confi")
        self.Fear=toneStat("Fear")

    def add_Art(self, art):
        #Add an article to the week, this function updates all scores for the week with the incoming articles data.
        self.List_Arts.append(art)
        self.Analy.add_score(art.analytical)
        self.Sadness.add_score(art.sadness)
        self.Confi.add_score(art.confidence)
        self.Anger.add_score(art.anger)
        self.Tenta.add_score(art.tentative)
        self.Fear.add_score(art.fear)
        self.Joy.add_score(art.joy)







"""
Class Article
-Scores set to .5 by default
"""
class Article:
    def __init__(self, source, date,url):
        self.source=source
        self.published=date
        self.url=url
        self.analytical=.5
        self.sadness=.5
        self.confidence=.5
        self.anger=.5
        self.tentative=.5
        self.fear=.5
        self.joy=.5








"""Tokenizes string of text.

    Tokenizes a given block of text, converts to lower and removes stop words.

    Args:
        text: a long string of text, typically an article.

    Returns:
        Returns a tokenized version of the text in the form of an array"""

def tokenize(text):
    words = nltk.word_tokenize(text.lower())
    new_words= [word for word in words if word.isalnum()]
    tokens_without_sw = [word for word in new_words if not word in stopwords.words()]
    return tokens_without_sw


"""Reads a csv lexicon and returns a dictionary.

    Args:
        Wrow: the number associated with the column that contains words in the csv.
        Prow: the number associated with the column that contains the polarity score in the csv.

    Returns:
        Returns a dictionary of words with associated scores."""

def DictCSV(filename,Wrow,Prow):
    newdict={}
    with open (filename) as tsv:
        lines=tsv.readline()
        for line in csv.reader(tsv, delimiter="\t"):
            word=line[Wrow]
            score=float(line[Prow])
            newdict[word]=score

    return newdict



"""Grabs text from websites, specifically NYT

    Args:
        urls: urls is a url or list of urls.

    Returns:
        One array of plain text from each url, and one array of tokenized text from each article."""



def GetText(urls):
    session = requests.Session()
    blob=[]
    tokenized_text=[]
    for url in urls:
        text=""
        req = session.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            words=p.get_text()
            text=text+" "+words
        Sentex=tokenize(text)
        tokenized_text.append(Sentex)
        #print(text, "\n")
        #blob.append(text[200:len(text)-360])
        blob.append(text)
        #print(text[200:len(text)-360],"/n")
    return blob, tokenized_text




"""Creates basic word usage graph

    Creates 3 graphs, histogram of words in the lexicon, not in the lexicon, and in the lexicon.

    Args:
        texts: An array of tokenized texts (typically from get text func).
        newdict: A lexicon to compare against.

    Returns:
        Prints graphs in order: Not in lexicon, both in lexicon and not, and one for in lexicon."""

def MakeGraphs(texts,newdict):
    both=[]
    indict=[]
    not_in_dict=[]
    for text in texts:
        for word in text:
            if word in newdict:
                both.append(word)
                indict.append(word)
            else:
                not_in_dict.append(word)
                both.append(word)

    dist1=FreqDist(not_in_dict)
    dist1.plot(15)
    dist2=FreqDist(both)
    dist2.plot(15)
    dist3=FreqDist(indict)
    dist3.plot(15)


"""Creates a list of scores associated with the texts fed in

    Args:
        texts: An array of tokenized texts (typically from get text func).
        newdict: A lexicon to score with.

    Returns:
         A list of scores associated with each text in the list of texts."""

def GetScore(texts,newdict):
    scores=[]
    for blob in texts:
        sum=0
        for word in blob:
            if word in newdict:
                sum+=newdict[word]
        scores.append(sum)
    return scores

#Pull basic info from NYT API, return url and list of article class OBJS



"""Api request, pulls important metadata.

    Pull() grabs the source, publication date and url of the articles returned.

    Args:
        que: An api query

    Returns:
         A list of urls, and a list of article class objects, the number of responses(articles in json) is also returned to check for 0 results"""

def Pull(que):

    response = requests.get(que)
    data = response.json()
    #hits=pyjq.all('.hits',data)

    copyright=pyjq.all('.copyright',data)
    dict={}
    num_docs=pyjq.all('.response | .docs',data)[0]
    resp=len(num_docs)


    #print(hits)
    query=f'.response .docs [] | {{web_url: .web_url, source: .source, pub_date: .pub_date}}'

    output=pyjq.all(query,data)

    arts=list()
    urls=[]
    for i in range(len(output)):
        dict=output[i]
        source=dict["source"]
        date=dict["pub_date"]
        url=dict["web_url"]
        urls.append(url)
        arts.append(Article(source,date,url))

    return urls,arts,resp
#Function name, #What it does, #input/output


"""Use with the IBM tone api, updates article class objs

    Args:
        scores: an array of scores for an article
        tones: the tones associated with the array of scores (parallel arrays)
        article: The specific article class obj that the scores are associated with
    Returns:
         Nothing, updates class obj"""


def AssignTone(scores,tones,article):
        for i in range(len(scores)):
            if tones[i]=="Analytical":
                article.analytical=scores[i]
            elif tones[i]=="Confidence":
                article.confidence=scores[i]
            elif tones[i]=="Sadness":
                article.sadness=scores[i]
            elif tones[i]=="Anger":
                article.anger=scores[i]
            elif tones[i]=="Tentative":
                article.tentative=scores[i]
            elif tones[i]=="Fear":
                article.fear=scores[i]
            elif tones[i]=="Joy":
                article.joy=scores[i]


#Takes body of texts, returns tone names[], and tone scores[]
"""
This is how I used the Assign tone function and the IBMtone function.
count=0
for text in texts:
    article=articles[count]
    tscores,tones=IBMtone(text)
    AssignTone(tscores,tones,article)
    count+=1
"""

"""Takes a string of raw text and feeds it into the IBM api to recieve tones associated with text.

    Sends request to IBM Tone analyzer api, and grabs responses.

    Args:
        text: A string of text to be sent to the tone analyzer
    Returns:
         list of scores and tones associated with text that was fed in"""

def IBMtone(text):
    apikey='mA_4uqt2kbCe0ulfIL_-w-s6d9QF1-tsC0ZB0_tWmDZu'
    authenticator = IAMAuthenticator(apikey)
    tone_analyzer = ToneAnalyzerV3(
        version='2017-09-21',
        authenticator=authenticator
    )

    tone_analyzer.set_service_url('https://api.au-syd.tone-analyzer.watson.cloud.ibm.com/instances/a4959905-de76-443d-9f76-3da83ecaa3cf')
    text = text
    tone_analysis = tone_analyzer.tone(
        {'text': text},
        content_type='application/json'
    ).get_result()
    query=f'.document_tone .tones[] | {{score: .score, tone_name: .tone_name}}'
    output=pyjq.all(query,tone_analysis)
    scores=[]
    tones=[]
    for i in range(len(output)):
        dict=output[i]
        score=dict["score"]
        tone=dict["tone_name"]
        scores.append(score)
        tones.append(tone)
    return scores,tones
