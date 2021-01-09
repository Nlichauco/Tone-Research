import pyjq
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import ToneAnalyzerV3


def tone_analyze(article, text):
    # Iterate through each article class, each 'text', corresponds to a single article
    t_scores, tones = ibm_tone(text)
    # Get tone scores and tones from IBM
    assign_tone(t_scores, tones, article)
    # AssignTone scores takes the scores from IBM and adds them to that specific article object.


# Takes body of texts, returns tone names[], and tone scores[]
"""
This is how I used the Assign tone function and the IBMtone function.
count=0
for text in texts:
    article=articles[count]
    t_scores,tones=ibm_tone(text)
    AssignTone(t_scores,tones,article)
    count+=1
"""

"""Takes a string of raw text and feeds it into the IBM api to receive tones associated with text.

    Sends request to IBM Tone analyzer api, and grabs responses.

    Args:
        text: A string of text to be sent to the tone analyzer
    Returns:
         list of scores and tones associated with text that was fed in"""


def ibm_tone(text):
    apikey = ''
    # apikey='mA_4uqt2kbCe0ulfIL_-w-s6d9QF1-tsC0ZB0_tWmDZu'
    authenticator = IAMAuthenticator(apikey)
    tone_analyzer = ToneAnalyzerV3(
        version='2017-09-21',
        authenticator=authenticator
    )

    tone_analyzer.set_service_url(
        '')
    text = text
    tone_analysis = tone_analyzer.tone(
        {'text': text},
        content_type='application/json'
    ).get_result()
    query = f'.document_tone .tones[] | {{score: .score, tone_name: .tone_name}}'
    output = pyjq.all(query, tone_analysis)
    scores = []
    tones = []
    for i in range(len(output)):
        my_dict = output[i]
        score = my_dict["score"]
        tone = my_dict["tone_name"]
        scores.append(score)
        tones.append(tone)
    return scores, tones


"""Use with the IBM tone api, updates article class objs

    Args:
        scores: an array of scores for an article
        tones: the tones associated with the array of scores (parallel arrays)
        article: The specific article class obj that the scores are associated with
    Returns:
         Nothing, updates class obj"""


def assign_tone(scores, tones, article):
    for i in range(len(scores)):
        if tones[i] == "Analytical":
            article.analytical = scores[i]
        elif tones[i] == "Confidence":
            article.confidence = scores[i]
        elif tones[i] == "Sadness":
            article.sadness = scores[i]
        elif tones[i] == "Anger":
            article.anger = scores[i]
        elif tones[i] == "Tentative":
            article.tentative = scores[i]
        elif tones[i] == "Fear":
            article.fear = scores[i]
        elif tones[i] == "Joy":
            article.joy = scores[i]
