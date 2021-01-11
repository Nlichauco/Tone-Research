# Tone-Research
This repo contains functions and files which all work together to request data from an various APIs, use that data to grab text from articles. Score the articles with IBM Tone Analyzer, and then store them into CSV's and class objs where we can analyze and plot the data. The tasks listed are delegated througout the .py files included in the repo. 


# Getting Started
To get the repo on your computer
********************************************************
* $ git clone https://github.com/Nlichauco/Tone-Research.git


# Data Collection


![image](https://user-images.githubusercontent.com/48927902/102701691-91ab1c00-4227-11eb-9346-720782ba4069.png)


**File Description**
***********************************************************
__Autoplot.py__ 
  * This file contains functions used for plotting data from the big csvs.
  * Includes plotting functions for Avg weekly tone scores, Cross source comparison, weekly ratio per tone score, and Cumulative tone score
************************************  
__ToneAnalyzer.py__
  * This file contains code that will take text gathered by the API and send it to the IBM Tone Analyzer.
  * It is also used to take the output of the IBM API and add the scores to article class objects. 
************************************  
__BigCSV.py__
  * This file contains the code necessary for formatting data to be ready for plotting.
  * Included functions deal with reading all the week by week csvs of a section and generating a big CSV for that section
************************************  
__CovidData.py__
  * Contains Week class obj and the toneStat class which is stored in the Week class object.
  * There is also a function which is used to create Week class objects based on multiple CSVs, given a path to a bunch of CSVs.
************************************  
__GenerateGuard.py and GenerateNYT.py__
  * Contains the necessary code for pulling from either the NYT API or TheGuardian API. 
************************************  
__GetDate.py__
  * This file contains the necessary functions for generating all of the weekly start and end dates
  * These dates are used when making API calls to specify the range you want to look at.
************************************  
__Compiling__
  *  While in terminal, in the correct directory type $ python [filename.py]
************************************  







