# Tone-Research
This repo contains functions and files which all work together to request data from an API, use that data to grab text from articles. Score the articles with IBM Tone Analyzer, and then store them into CSV's and class objs where we can analyze and plot the data. The tasks listed are delegated througout the .py files included in the repo. 


# Getting Started
The necessary libraries in total are
********************************************************
* $ git clone https://github.com/Nlichauco/Tone-Research.git


# Data Collection


![image](https://user-images.githubusercontent.com/48927902/102701691-91ab1c00-4227-11eb-9346-720782ba4069.png)


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
__Compiling__
  * This is what all of the above files look like in action working together. 
  * This file effectively calls the API through a give range of dates, and creates CSVs for each response. 
  * Plotting and Week class objects are not currently used here. 
************************************  

All you actually need for data collection is the GitDemo file and Funcs.py, Funcs.py includes all of the necesary functions for GitDemo, and GitDemo is how I have been grabbing and saving data.






