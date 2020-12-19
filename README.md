# Tone-Research
This repo contains functions and files which all work together to request data from an API, use that data to grab text from articles. Score the articles with IBM Tone Analyzer, and then store them into CSV's and class objs where we can analyze and plot the data. The tasks listed are delegated througout the .py files included in the repo. 


# Getting Started
The necessary libraries in total are
********************************************************
* import json
* import requests
* import pyjq
* from bs4 import BeautifulSoup
* import nltk
* import string
* from nltk.tokenize import word_tokenize
* from nltk.probability import FreqDist
* from nltk.corpus import stopwords
* from nltk.tokenize import word_tokenize, RegexpTokenizer
* import csv
* from ibm_watson import ToneAnalyzerV3
* from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
* import matplotlib.pyplot as plt
* import numpy as np
* import matplotlib.ticker as ticker
* import re
* import glob
* from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
* import os
* import pandas as pd
* import statistics as stat
* from natsort import natsorted, ns
***********************************************************

However these are all used by different files/functions, this is just a master list of all libraries used.


**File Description**
***********************************************************
__NewsAPI.py__ 
  * This file deals with requesting data from an API, parsing that data and returning useful meta data.
  * It also uses the meta data extracted to get the actual text from each article and instantiate article class objects. 
************************************  
__ToneAnalyzer.py__
  * This file contains code that will take text gathered by the API and send it to the IBM Tone Analyzer.
  * It is also used to take the output of the IBM API and add the scores to article class objects. 
************************************  
__StoreData.py__
  * This file has code to createCSV files based on article class objects.
  * Also has a function to create a more comprehenisve week by week CSV, give week class objects.
************************************  
__WeeklyStats.py__
  * Contains Week class obj and the toneStat class which is stored in the Week class object.
  * There is also a function which is used to create Week class objects based on multiple CSVs, given a path to a bunch of CSVs.
************************************  
__RoughPlotting.py__
  * Contains the rough code for plotting the type of graph we want (scatter with dotted connected lines).
  * Still need to make this file more variable as it is not a function currently. 
************************************  
__GitDemo.py__
  * This is what all of the above files look like in action working together. 
  * This file effectively calls the API through a give range of dates, and creates CSVs for each response. 
  * Plotting and Week class objects are not currently used here. 
************************************  

All you actually need for data collection, is the GitDemo file and Funcs.py, Funcs.py includes all of the necesary functions for GitDemo, and GitDemo is the how I have been grabbing and saving data.

![DataCollection.pdf](https://github.com/Nlichauco/Tone-Research/files/5720271/DataCollection.pdf)

