

import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
import re
import glob
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)

# This section still needs a lot of work, automated plotting is something im still working on.
# However this will code create a plot.
# Also by far the most confusing section





missing_values=["NaN","0"]
paths=["/Users/nathaniel/Desktop/Research/All_Weeks/Jan","/Users/nathaniel/Desktop/Research/All_Weeks/Feb","/Users/nathaniel/Desktop/Research/All_Weeks/March","/Users/nathaniel/Desktop/Research/All_Weeks/April","/Users/nathaniel/Desktop/Research/All_Weeks/May","/Users/nathaniel/Desktop/Research/All_Weeks/June"]


tru=0

col_names=['Anger','Fear','Joy','Sad','Analy','Confi','Tenta']
M_Anger,M_Fear,M_Joy,M_Sad,M_Analy,M_Confi,M_Tenta=([] for i in range(7))
for path in paths:
    for filename in sorted(os.listdir(path)):

        if not filename.startswith('.'):
            #print(filename)

            with open(os.path.join(path, filename)) as f:


                data=pd.read_csv(f, header=0,sep=r'\s*,\s*',na_values=missing_values,engine='python')
                for emo in col_names:
                    values=data[emo]
                    sum=0
                    count=0
                    for num in values:
                        if num > .5:
                            sum+=num
                            count+=1

                    if count!=0 and sum!=0:
                        mean=sum/count
                        if emo=='Anger':
                            M_Anger.append(mean)

                        elif emo=='Fear':
                            M_Fear.append(mean)

                        elif emo=='Joy':
                            M_Joy.append(mean)

                        elif emo=='Sad':
                            M_Sad.append(mean)

                        elif emo=='Analy':
                            M_Analy.append(mean)

                        elif emo=='Confi':
                            M_Confi.append(mean)

                        elif emo=='Tenta':
                            M_Tenta.append(mean)

new=[]
List_of_tones=[M_Anger,M_Fear,M_Joy,M_Sad,M_Analy,M_Confi,M_Tenta]

for i in range(1,len(M_Joy)+1):
    tick="Week"
    tick=tick+str(i)
    new.append(tick)


#print((tru/count)*100,"\n")
plt.title('Average Tone Score Per Week ("Op-Eds")')
plt.xlabel('Week')
plt.ylabel('IBM Tone Score')

#plt.yticks([])
plt.locs, labels = plt.yticks()  # Get the current locations and labels.
plt.yticks(np.arange(.5, 1))  # Set Ticks to go from .5 to 1
plt.ylim(.5, 1) #Set limits of y axis


ax=plt.axes()
ax.yaxis.set_major_locator(MultipleLocator(.1)) #Space out y axis ticks by .1


plt.tick_params(axis='x', which='major', labelsize=7, rotation=90) #Rotate tick labels by 90 degrees to fit them.
#plt.tick_params(axis='y', which='major', labelsize=4)

#plt.legend()
#plt.ax.set_xticklabels(rotation = (45), fontsize = 10, va='bottom', ha='left')

confi=[] #Create axis that fit lists who dont have as much data.
fear=[]
sad=[]


for i in range(0,len(M_Confi)):
    confi.append(i)
for i in range(0,len(M_Fear)):
    fear.append(i)
for i in range(0,len(M_Sad)):
    sad.append(i)

plt.scatter(new,M_Tenta, label='Tentative')
plt.plot(new,M_Tenta,linestyle='--')

plt.scatter(sad,M_Sad,label='Sad',linewidths=1)
plt.plot(sad,M_Sad,linestyle='--')
plt.scatter(fear,M_Fear,label='Fear')
plt.plot(fear,M_Fear,linestyle='--')
plt.scatter(new,M_Joy,label='Joy')
plt.plot(new,M_Joy,linestyle='--')
plt.scatter(confi,M_Confi,label='Confident')
plt.plot(confi,M_Confi,linestyle='--')
plt.scatter(new,M_Analy,label='Analytical')
plt.plot(new,M_Analy,linestyle='--')

ax.legend()

#plt.scatter()

#plt.show()

plt.savefig('Ftest3.png',bbox_inches='tight')





rootdir = '/Users/nathaniel/Desktop/Research/All_Weeks'
