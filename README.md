# Tone-Research

These functions and files all work together to request data from an API, use that data to grab text from articles. Score the articles with IBM Tone Analyzer, and then store them into CSV's and class objs where we can analyze and plot the data. 

The necessary libraries in total are

********************************************************
import json
import requests
import pyjq
from bs4 import BeautifulSoup
import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, RegexpTokenizer
import csv
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
import re
import glob
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
import os
import pandas as pd
import statistics as stat
from natsort import natsorted, ns
***********************************************************

However these are all used by different files/functions, this is just a master list of all libraries used.

There is also a READCSV function which is not included in any of the files, but it is in Maine.py, I didn't include this function becuase you need to download the WKWSCI lexicon, and store it in the 'current' directory in order to use it. We could also just not use the lexicon anymore as we are primarily using IBM Tone Analyzer for meaningful data. 


