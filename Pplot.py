import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
import re
import glob
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
from BigCSV import *
from Funcs import *
from math import log


#NYT primary tentative




months=["March","April","May","June","July"]
sdates=StartDates("G")
Sad_mean,Fear_mean,Anger_mean,Tenta_mean,Joy_mean,Confi_mean,Analy_mean=GetToneAvgs("GuardianSci")
xaxe=[]
for num in range(0,len(Sad_mean)):
    xaxe.append(num)
fig, ax1 = plt.subplots()
plt.plot(Sad_mean,'ro',label="sad")
plt.yticks(np.arange(.5, 1))  # Set Ticks to go from .5 to 1
plt.ylim(.5, 1) #Set limits of y axis
ax1.yaxis.set_major_locator(MultipleLocator(.1)) #Set spacing of y axis
ax1.set_xticklabels(months,rotation=45)
ax1.xaxis.set_major_locator(MultipleLocator(10))
#plt.xticks(np.arange(2,5))
#plt.xlim(2,5)
#ax1.xaxis.set_major_locator(MultipleLocator(1))
ax1.legend(loc="upper left")
fig.tight_layout()
plt.show()
