import csv
from datetime import date

import pyjq
import requests

# from GetDate import get_date_guardian_format
from GetDate import get_date_guardian_format
from ToneAnalyzer import tone_analyze
from entity.Article import Article

"""Creates complete article class objects with tone scores
    Args:
        articles: article class objs each of which associates to a blob of text
        texts: A list of text blobs for the Tone Analyzer
    Returns:
         A list of article objects which also have tone scores.
         """


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
    Nothing, creates file in directory
    """


def create_csv(articles, file_name):
    with open(file_name, 'a') as file:
        writer = csv.writer(file)
        for a in articles:
            writer.writerow(
                [a.source, a.published, a.url, 0, " ", a.anger, a.fear, a.joy, a.sadness, a.analytical,
                 a.confidence, a.tentative])


"""Api request, pulls important metadata.
    Pull() grabs the source, publication date and url of the articles returned.
    Args:
        que: An api query
    Returns:
         A list of urls, and a list of article class objects, the number of responses(articles in json) is also returned
         to check for 0 results"""


def Gpull(que):
    response = requests.get(que)
    data = response.json()
    num_docs = pyjq.all('.response | .total', data)[0]
    num_pages = pyjq.all('.response | .pages', data)[0]

    pquery = '.response .results[].fields |  {stuff: .bodyText}'
    query = f'.response .results [] | {{web_url: .webUrl, pub_date: .webPublicationDate}}'
    output = pyjq.all(query, data)
    another = pyjq.all(pquery, data)
    print(another)
    arts = list()
    body = []
    for i in range(len(another)):
        dict = output[i]
        texts = another[i]
        source = "Guardian"
        date = dict["pub_date"]
        url = dict["web_url"]
        text = texts["stuff"]
        if text != '':
            body.append(text)
            arts.append(Article(source, date, url))
    return body, arts, num_docs, num_pages


def create_template(file_name):
    with open(file_name, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(
            ["Source", "Date", "URL", "Score", "   ", "Anger", "Fear", "Joy", "Sad", "Analy", "Confi", "Tenta"])


def fetch_from_guardian(que, filename):
    texts, articles, amt, pages = Gpull(que)
    if amt < 1:
        # If there are no articles returned skip to the next week.
        return 0
    # Get scores from the lexicon, this may or may not be removed, just because we aren't really using it.
    articles = create_arts(articles, texts)
    create_csv(articles, filename)
    return pages


def Guardpull(s_dates, e_dates, keyword, APIkey, sectionName):
    for i in range(0, len(s_dates)):
        fname = "2020-"+s_dates[i][:2] + "-" + s_dates[i][3:]+ ".csv"
        create_template(fname)
        page = 2
        que = """https://content.guardianapis.com/search?section=""" + sectionName + """&q=""" + keyword + """&type=article&edition=uk&from-date=2020-""" + \
              s_dates[i] + "&to-date=2020-" + e_dates[i] + "&show-fields=bodyText&api-key=""" + APIkey
        pages = fetch_from_guardian(que, fname)

        while page <= pages:
            que = """https://content.guardianapis.com/search?section=""" + sectionName + """&q=""" + keyword + """&type=article&edition=uk&from-date=2020-""" + \
                  s_dates[i] + "&to-date=2020-" + e_dates[i] + "&show-fields=bodyText&page=""" + str(
                page) + """&api-key=""" + APIkey
            fetch_from_guardian(que, fname)
            page += 1


def main():
    # Assuming desired start date is March 1st 2020, and end date is December 26th
    s_dates = get_date_guardian_format(0, date(2020, 3, 1), date(2020, 12, 26))
    e_dates = get_date_guardian_format(6, date(2020, 3, 1), date(2020, 12, 26))

    # Now we have all the info we need to grab articles.
    keyword = "coronavirus"
    APIkey = "7735070e-6108-49c2-80bc-a6a7898d725b"
    sectionName = "society"

    Guardpull(s_dates, e_dates, keyword, APIkey, sectionName)


main()
