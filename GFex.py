from Funcs import *
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
import re
import glob
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
# These are the start and end dates we want to pull articles from.
s_dates=["0522","0601","0608","0615","0622","0701","0708","0715","0722"]
e_dates=["0531","0607","0614","0621","0630","0707","0714","0721","0729"]
bob=False
# This is just here so I could put Pulling data code and plotting data code in the same file to show the whole process.
# Typically these tasks are seperated into different files.
if bob==True:

    newdict=DictCSV("wkwlex.tab",0,2) #Reading dict, this requires a file in the same directory as this code

    # Since we want articles from each week, we loop through the dates, using them as start and end dates in the API query.
    for i in range(0,len(s_dates)):

        fname="week"+str(i)+".csv"

        # In this example we are looking at articles with the keyword George Floyd, in the OpEd section.
        que="""https://api.nytimes.com/svc/search/v2/articlesearch.json?q=George%20Floyd&page=0&fq=news_desk:("OpEd")&source:("The New York Times")&facet=true&sort=relevance&begin_date=2020"""+s_dates[i]+"&end_date=2020"+e_dates[i]+"&api-key=d6ZZ3CclPNtLfkZid9iUvs6HpYLEbehl"

        # We feed the query into the pull function.
        urls,articles,amt=Pull(que)
        print(amt)
        print("hit \n")
        if amt<1:
            # If there are no articles returned skip to the next week.
            continue

        print("made it past")
        texts,token_texts=GetText(urls) #This function takes the urls, visits them and takes the article text from the site.
        # texts for the IBM tone analyzer, token_texts for the lexicon score.

        scores=GetScore(token_texts,newdict)
        # Get scores from the lexicon, this may or may not be removed, just because we aren't really using it.
        count=0
        # Loop through article texts
        for text in texts:
            article=articles[count]
            # Iterate through each article class, each 'text', corresponds to a single article
            tscores,tones=IBMtone(text)
            # Get tone scores and tones from IBM

            AssignTone(tscores,tones,article)
            #AssignTone scores takes the scores from IBM and adds them to that specific article object.
            count+=1
        CreateCSV(articles,fname,scores)

# Plotting

# Since we typically plot using week averages, the first thing we want to do is create week class objects
# This is done by reading the csv files we created above
# The function for this is the ReadSection function
#    weeks=ReadSection()
# This function accepts a path as its param. So in order to use this function I have to put all the csvs I want into a folder.
# Then I take the folders pathname and pass it as a string to ReadSection(path)
path='/Users/nathaniel/Desktop/Research/George'
weeks=ReadSection(path)
# Once we have the weeks we decide what we want to plot.
# For this example I will plot the average tone scores per week, over time
# To get the averages by week, I call the GetAvgs function which takes a list of 'week' class objs.

Sad_mean,Fear_mean,Anger_mean,Tenta_mean,Joy_mean,Confi_mean,Analy_mean=GetAvgs(weeks)

# Here I create the title, and labels for our plot
plt.title('Average Tone Score Per Week ("George Floyd")')
plt.xlabel('Week')
plt.ylabel('IBM Tone Score')
new=[]

# This section of code is to loop through the number of expected weeks and check if any are missing.
missing_weeks=[]
for i in range(0,9):
    missing_weeks.append(i)

# Here we loop through each week we have data for.
for i in range(len(weeks)):
    week=weeks[i]
    name=week.weekname
    # Num represents which week we are on, num=1 for week 1.
    num=int(name[4:])
    # If we have data for a certain week, remove that week number from the missing weeks list.
    if num in missing_weeks:

        missing_weeks.remove(num)

# Now that missing_weeks only holds weeks we dont have data for, we can go through and populate those weeks with
# place holder data so the plotting still works.
for i in range(0,9):
    # If the i is still in missing weeks, we know there is no csv associated with that week.
    if i in missing_weeks:
        # if a week doesnt have a csv (i.e got no data), we have to inseret a default of .5 to ensure smooth plotting.
        Sad_mean.insert(i,.5)
        Fear_mean.insert(i,.5)
        Anger_mean.insert(i,.5)
        Tenta_mean.insert(i,.5)
        Joy_mean.insert(i,.5)
        Confi_mean.insert(i,.5)
        Analy_mean.insert(i,.5)
    tick="Week"
    tick=tick+str(i+1)
    # Here we also create the labels for the x axis.
    new.append(tick)


plt.locs, labels = plt.yticks()  # Get the current locations and labels.
plt.yticks(np.arange(.5, 1))  # Set Ticks to go from .5 to 1
plt.ylim(.5, 1) #Set limits of y axis
ax=plt.axes()
ax.yaxis.set_major_locator(MultipleLocator(.1)) # Space out y axis ticks by .1
plt.tick_params(axis='x', which='major', labelsize=7, rotation=90) # Rotate tick labels by 90 degrees to fit them.
#plt.tick_params(axis='y', which='major', labelsize=4)
#plt.legend()
#plt.ax.set_xticklabels(rotation = (45), fontsize = 10, va='bottom', ha='left')

# (x,y,label='*name associated with line shows up on the legend').
plt.scatter(new,Tenta_mean, label='Tentative')
plt.plot(new,Tenta_mean,linestyle='--')
plt.scatter(new,Anger_mean,label='Anger')
plt.plot(new,Anger_mean,linestyle='--')
plt.scatter(new,Sad_mean,label='Sad',linewidths=1)
plt.plot(new,Sad_mean,linestyle='--')
plt.scatter(new,Fear_mean,label='Fear')
plt.plot(new,Fear_mean,linestyle='--')
#plt.scatter(new,Joy_mean,label='Joy')
#plt.plot(new,Joy_mean,linestyle='--')
plt.scatter(new,Confi_mean,label='Confident')
plt.plot(new,Confi_mean,linestyle='--')
plt.scatter(new,Analy_mean,label='Analytical')
plt.plot(new,Analy_mean,linestyle='--')

ax.legend()

#plt.scatter()

plt.show()
# The plot is shown in the GFex.png file 
