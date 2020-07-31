from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import pyjq
#All functions associated with IBM Tone analyzer api.



"""Takes a string of raw text and feeds it into the IBM api to recieve tones associated with text.

    Sends request to IBM Tone analyzer api, and grabs responses.

    Args:
        text: A string of text to be sent to the tone analyzer
    Returns:
         list of scores and tones associated with text that was fed in"""

def IBMtone(text):
    apikey='d3ShrpYAkR36xgoeTDGnKULO7V_1Hcs82Qy0hFmGwrFZ'
    authenticator = IAMAuthenticator(apikey)
    tone_analyzer = ToneAnalyzerV3(
        version='2017-09-21',
        authenticator=authenticator
    )

    tone_analyzer.set_service_url('https://api.au-syd.tone-analyzer.watson.cloud.ibm.com/instances/8f3da9cc-3ff9-491e-8749-fd22c2b25ace')
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

"""
This is how I used the Assign tone function and the IBMtone function.

count=0
#Loop through article texts

for text in texts:
    #Iterate through each article class, each 'text', corresponds to a single article

    article=articles[count]
    #Get tone scores and tones from IBM

    tscores,tones=IBMtone(text)
    #AssignTone scores takes the scores from IBM and adds them to that specific article object.

    AssignTone(tscores,tones,article)
    count+=1
"""
