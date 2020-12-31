import csv
from datetime import date

import pyjq
import requests
from bs4 import BeautifulSoup

from GetDate import get_date_nyt_format
from ToneAnalyzer import tone_analyze
from entity.Article import Article


def fetch_from_nyt(que, file_name):
    urls, articles, amt = pull(que)
    print(amt)
    print("hit \n")
    if amt < 1:
        # If there are no articles returned skip to the next week.
        return
    texts, token_texts = get_text(urls)
    articles = create_arts(articles, texts)
    create_csv(articles, file_name)


# Pull basic info from NYT API, return url and list of article class OBJS


"""Api request, pulls important metadata.

    Pull() grabs the source, publication date and url of the articles returned.

    Args:
        que: An api query

    Returns:
         A list of urls, and a list of article class objects, the number of responses(articles in json) is also returned 
         to check for 0 results"""


def pull(que):
    response = requests.get(que)
    data = response.json()
    num_docs = pyjq.all('.response | .docs', data)[0]
    resp = len(num_docs)
    query = f'.response .docs [] | {{web_url: .web_url, source: .source, pub_date: .pub_date}}'

    output = pyjq.all(query, data)

    arts = list()
    urls = []
    for i in range(len(output)):
        my_dict = output[i]
        source = my_dict["source"]
        date = my_dict["pub_date"]
        url = my_dict["web_url"]
        urls.append(url)
        arts.append(Article(source, date, url))

    return urls, arts, resp


"""Grabs text from websites, specifically NYT

    Args:
        urls: urls is a url or list of urls.

    Returns:
        One array of plain text from each url."""


def get_text(urls):
    session = requests.Session()
    blob = []
    for url in urls:
        text = ""
        req = session.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            words = p.get_text()
            text = text + " " + words
        if len(text) > 131070:
            continue
        blob.append(text)
    return blob


"""Creates complete article class objects with tone scores

    Args:
        articles: article class objs each of which associates to a blob of text
        texts: A list of text blobs for the Tone Analyzer

    Returns:
         A list of article objects which also have tone scores."""


def create_arts(articles, texts):
    count = 0
    for text in texts:
        article = articles[count]
        tone_analyze(article, text)
        count += 1
    return articles


"""
Reads through article class objs and creates CSV for that week.

Args:
    articles: List of articles from the same week.
    file_name: desired name of CSV.
    scores: Scores from lexicon.

Returns:
    Nothing, creates file in directory"""


def create_csv(articles, file_name):
    with open(file_name, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(
            ["Source", "Date", "URL", "Score", "   ", "Anger", "Fear", "Joy", "Sad", "Analy", "Confi", "Tenta"])
        for a in articles:
            writer.writerow(
                [a.source, a.published, a.url, 0, " ", a.anger, a.fear, a.joy, a.sadness, a.analytical,
                 a.confidence, a.tentative])


def demo():
    s_dates = get_date_nyt_format(0, date(2020, 3, 1), date(2020, 12, 26))
    e_dates = get_date_nyt_format(6, date(2020, 3, 1), date(2020, 12, 26))
    for i in range(0, len(s_dates)):
        file_name = s_dates[i][:2] + "." + s_dates[i][2:] + "-" + e_dates[i][:2] + "." + e_dates[i][2:] + ".csv"
        que = """https://api.nytimes.com/svc/search/v2/articlesearch.json?q=coronavirus&page=0&fq=news_desk:(
        "Health")&source:("The New York Times")&facet=true&sort=relevance&begin_date=2020""" + \
              s_dates[i] + "&end_date=2020" + e_dates[i] + "&api-key=aiPyJZEGATr7l0XfQGsBpQ3loDqzteIC"
        fetch_from_nyt(que, file_name)


demo()
