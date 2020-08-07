import pyjq
import json
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, RegexpTokenizer
from datetime import timedelta, date
# Basic functions for querying NYT API, parsing json, insantiating article class objs, and returning texts for Tone Analyzer



"""Get dates to iterate through for API query.

   endDates gets all of the end dates for weeks from the 1st of Jan to the 29 of July.
   StartDates does the same thing except, the date of the beginning of the week.

    Args:
        None

    Returns:
         A list of dates that can be used as variables in the query"""
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




"""Grabs text from websites, specifically NYT

    Args:
        urls: urls is a url or list of urls.

    Returns:
        One array of plain text from each url, and one array of tokenized text from each article."""

def GetText(urls):
    # Arg is urls from Pull function
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


"""Tokenizes string of text.

    Tokenizes a given block of text, converts to lower and removes stop words.

    Args:
        text: a long string of text, typically an article.

    Returns:
        Returns a tokenized version of the text in the form of an array"""
def tokenize(text):
    # Used in GetText function
    words = nltk.word_tokenize(text.lower())
    new_words= [word for word in words if word.isalnum()]
    tokens_without_sw = [word for word in new_words if not word in stopwords.words()]
    return tokens_without_sw
