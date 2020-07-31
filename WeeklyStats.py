import statistics as stat
from natsort import natsorted, ns
import pandas as pd
import os
import csv


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
            return 0
    def get_median(self):
        return stat.median(self.Tone_scores)
    def get_max(self):
        return max(self.Tone_scores)



"""
Reads all of the CSVS and returns a list of week class objs.

Reads one CSV per iteration of the given "section" pathname, puts each CSV into an article class.

Args:
    Path: The path to a section file, section file contains all CSVS pertaining to that section (each CSV represents a week).

Returns:
    A list of week class objs, One for each CSV"""

# Creates the week class objects based on per week CSVs.
def ReadSection(path):
    missing_values=["NaN","0"]
    print(os.listdir(path))
    #Create a list to return.
    list_weeks=list()
    for filename in natsorted(os.listdir(path), key=lambda y:y.lower()):
        # Files are created in order 'week1','week2'...'weekx',Natsort sorts files in order
        # then iterate through.


        if not filename.startswith('.'):
            #Check for hidden .DS files.
            print(filename,"\n")
            week=Week(str(filename[0:-4]))
            #Slices the .csv off the filenames.
            with open(os.path.join(path, filename)) as f:
                #Read through csv


                data=pd.read_csv(f, header=0,sep=r'\s*,\s*',na_values=missing_values,engine='python',usecols=[0,1,2,5,6,7,8,9,10,11])
                for ind in data.index:
                    #Reading line by line (ind is y coordinate)
                    article=Article(data['Source'][ind],data['Date'][ind], data['URL'][ind])
                    #Create article with all data (based off CSV).

                    article.analytical=data['Analy'][ind]
                    article.sadness=data['Sad'][ind]
                    article.confidence=data['Confi'][ind]
                    article.anger=data['Anger'][ind]
                    article.tentative=data['Tenta'][ind]
                    article.fear=data['Fear'][ind]
                    article.joy=data['Joy'][ind]



                    week.add_Art(article)
                    #Add article to week class obj
                list_weeks.append(week)
                #Finished CSV, append week class obj to list of weeks
                #Repeat until all csvs are represented by week class objs
    return list_weeks
