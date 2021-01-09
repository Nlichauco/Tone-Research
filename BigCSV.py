<<<<<<< HEAD
import csv
import os
import pandas as pd
from natsort import natsorted
from entity.Article import Article
from entity.Week import Week

the_paths = ['/Users/ff/Desktop/nyt/business', '/Users/ff/Desktop/nyt/opinion']


def big_csv(paths):
    for path in paths:
        section = path[path.rfind('/') + 1:]
        weeks = read_section(path)
        week_write(weeks, section)


"""
Reads all of the CSVS and returns a list of week class objs.

Reads one CSV per iteration of the given "section" pathname, puts each CSV into an article class.

Args:
    Path: The path to a section file, section file contains all CSVS pertaining to that section (each CSV represents a week).


Returns:
    A list of week class objs, One for each CSV"""


def read_section(path):
    missing_values = ["NaN", "0"]
    # print(os.listdir(path))
    list_weeks = list()
    for filename in natsorted(os.listdir(path), key=lambda y: y.lower()):

        if not filename.startswith('.'):
            # print(filename,"\n")
            week = Week(str(filename[0:-4]))
            with open(os.path.join(path, filename)) as f:

                data = pd.read_csv(f, header=0, sep=r'\s*,\s*', na_values=missing_values, engine='python',
                                   usecols=[0, 1, 2, 5, 6, 7, 8, 9, 10, 11])
                for ind in data.index:
                    article = Article(data['Source'][ind], data['Date'][ind], data['URL'][ind])

                    article.analytical = data['Analy'][ind]
                    article.sadness = data['Sad'][ind]
                    article.confidence = data['Confi'][ind]
                    article.anger = data['Anger'][ind]
                    article.tentative = data['Tenta'][ind]
                    article.fear = data['Fear'][ind]
                    article.joy = data['Joy'][ind]

                    # print(article.sadness,"    ", article.url)
                    week.add_Art(article)
                list_weeks.append(week)
    return list_weeks


"""
Writes data from Weeks class to CSV.

Creates CSV with week by week data of a the current "section" (i.e. ('sports','science','buisness'))

Args:
    Weeks: A list of week class objects.
    Section: The new desk where the data was taken from, this will be the label of the csv.

Returns:
    Nothing. Writes a 'section'.csv file in the current directory."""


def week_write(weeks, section):
    file_name = section + ".csv"
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            ["Week", "Anger_max", "Anger_med", "Anger_avg", "Sad_max", "Sad_median", "Sad_avg", "Fear_max", "Fear_med",
             "Fear_avg", "Joy_max", "Joy_med", "Joy_avg", "Analy_max", "Analy_med", "Analy_avg", "Confi_max",
             "Confi_med", "Confi_avg", "Tenta_max", "Tenta_med", "Tenta_avg"])
        for week in weeks:
            writer.writerow(
                [week.weekname, week.Anger.get_max(), week.Anger.get_median(), week.Anger.get_mean(),
                 week.Sadness.get_max(), week.Sadness.get_median(), week.Sadness.get_mean(), week.Fear.get_max(),
                 week.Fear.get_median(), week.Fear.get_mean(), week.Joy.get_max(), week.Joy.get_median(),
                 week.Joy.get_mean(), week.Analy.get_max(), week.Analy.get_median(), week.Analy.get_mean(),
                 week.Confi.get_max(),
                 week.Confi.get_median(), week.Confi.get_mean(), week.Tenta.get_max(), week.Tenta.get_median(),
                 week.Tenta.get_mean()])


big_csv(the_paths)
=======
from Funcs import *

import pandas as pd


paths=['/Users/nathaniel/Desktop/Tone-Research/GuardianOped','/Users/nathaniel/Desktop/Tone-Research/GuardianPol','/Users/nathaniel/Desktop/Tone-Research/GuardianSci']
def bigCSV(paths):
    for path in paths:
        section=""
        for i in range(len(path)-1,0,-1):
            if path[i]=="/":
                break
            section=path[i]+section
        weeks=ReadSection(path)
        weekwrite(weeks,section)


def GetToneAvgs(filename):
    fields=["Anger_avg","Sad_avg","Fear_avg","Joy_avg","Analy_avg","Confi_avg","Tenta_avg"]
    filename=filename+".csv"
    df=pd.read_csv(filename,usecols=fields)
    Sad_mean=df["Sad_avg"]
    Fear_mean=df["Fear_avg"]
    Anger_mean=df["Anger_avg"]
    Tenta_mean=df["Tenta_avg"]
    Joy_mean=df["Joy_avg"]
    Confi_mean=df["Confi_avg"]
    Analy_mean=df["Analy_avg"]
    return Sad_mean,Fear_mean,Anger_mean,Tenta_mean,Joy_mean,Confi_mean,Analy_mean


Sad_mean,Fear_mean,Anger_mean,Tenta_mean,Joy_mean,Confi_mean,Analy_mean=GetToneAvgs("GuardianSci")

print(Sad_mean)

#print(df.keys())
#print(df.Sad_avg)
>>>>>>> 98a1efe04d672969efd89507e3d650932938d054
