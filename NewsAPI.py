import pyjq
import json
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, RegexpTokenizer
# Basic functions for querying NYT API, parsing json, insantiating article class objs, and returning texts for Tone Analyzer


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
