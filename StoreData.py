
import csv
# These functions are used to create CSV files and store the data in them.
"""
Reads through article class objs and creates CSV for that week.

Args:
    articles: List of articles from the same week.
    fname: desired name of CSV.
    scores: Scores from lexicon.

Returns:
    Nothing, creates file in directory"""

def CreateCSV(articles,fname,scores):
    with open(fname, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Source", "Date", "URL","Score","   ","Anger","Fear","Joy","Sad","Analy","Confi","Tenta"])
        rcount=0
        for a in articles:
            #writer.writerow([a.source, a.published,a.url,scores[count]," ",%.2f,a.fear,a.joy,a.sadness,a.analytical,a.confidence,a.tentative])
            writer.writerow([a.source, a.published,a.url,scores[rcount]," ",a.anger,a.fear,a.joy,a.sadness,a.analytical,a.confidence,a.tentative])
            rcount+=1


    """
    Writes data from Weeks class to CSV.

    Creates CSV with week by week data of a the current "section" (i.e. ('sports','science','buisness'))

    Args:
        Weeks: A list of week class objects.
        Section: The new desk where the data was taken from, this will be the label of the csv.

    Returns:
        Nothing. Writes a 'section'.csv file in the current directory."""

def weekwrite(weeks,section):
    fname=section+".csv"
    with open(fname, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Week","Anger_max", "Anger_med","Anger_avg","Sad_max","Sad_median","Sad_avg","Fear_max","Fear_med","Fear_avg","Joy_max","Joy_med","Joy_avg","Analy_max","Analy_med","Analy_avg","Confi_max","Confi_med","Confi_avg","Tenta_max","Tenta_med","Tenta_avg"])
        rcount=0
        for week in weeks:
            Anger_median=week.Anger.get_median()
            Anger_max=week.Anger.get_max()
            Anger_mean=week.Anger.get_mean()
            Sad_median=week.Sadness.get_median()
            Sad_max=week.Sadness.get_max()
            Sad_mean=week.Sadness.get_mean()
            Fear_median=week.Fear.get_median()
            Fear_max=week.Fear.get_max()
            Fear_mean=week.Fear.get_mean()
            Joy_median=week.Joy.get_median()
            Joy_max=week.Joy.get_max()
            Joy_mean=week.Joy.get_mean()
            Analy_median=week.Analy.get_median()
            Analy_max=week.Analy.get_max()
            Analy_mean=week.Analy.get_mean()
            Confi_median=week.Confi.get_median()
            Confi_max=week.Confi.get_max()
            Confi_mean=week.Confi.get_mean()
            Tenta_median=week.Tenta.get_median()
            Tenta_max=week.Tenta.get_max()
            Tenta_mean=week.Tenta.get_mean()
            writer.writerow([week.weekname, Anger_max,Anger_median,Anger_mean,Sad_max,Sad_median,Sad_mean,Fear_max,Fear_median,Fear_mean,Joy_max,Joy_median,Joy_mean,Analy_max,Analy_median,Analy_mean,Confi_max,Confi_median,Confi_mean,Tenta_max,Tenta_median,Tenta_mean])
