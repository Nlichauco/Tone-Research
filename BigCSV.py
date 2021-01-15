import csv
import os
import pandas as pd
from natsort import natsorted
from entity.Article import Article
from entity.Week import Week

the_paths = ['res/NYT/Business', 'res/NYT/Science', 'res/NYT/Opinion', 'res/NYT/Politics']


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
            ["Week", "Anger_max", "Anger_med", "Anger_avg", "Anger_total", "Anger_ratio", "Sad_max", "Sad_median",
             "Sad_avg",
             "Sad_total", "Sad_ratio", "Fear_max", "Fear_med",
             "Fear_avg", "Fear_total", "Fear_ratio", "Joy_max", "Joy_med", "Joy_avg", "Joy_total", "Joy_ratio",
             "Analy_max", "Analy_med",
             "Analy_avg", "Analy_total", "Analy_ratio", "Confi_max",
             "Confi_med", "Confi_avg", "Confi_total", "Confi_ratio", "Tenta_max", "Tenta_med", "Tenta_avg",
             "Tenta_total", "Tenta_ratio"])
        for week in weeks:
            writer.writerow(
                [week.weekname, week.Anger.get_max(), week.Anger.get_median(), week.Anger.get_mean(),
                 week.Anger.get_total(), week.Anger.get_perc(),
                 week.Sadness.get_max(), week.Sadness.get_median(), week.Sadness.get_mean(), week.Sadness.get_total(),
                 week.Sadness.get_perc(),
                 week.Fear.get_max(),
                 week.Fear.get_median(), week.Fear.get_mean(), week.Fear.get_total(), week.Fear.get_perc(),
                 week.Joy.get_max(),
                 week.Joy.get_median(),
                 week.Joy.get_mean(), week.Joy.get_total(), week.Joy.get_perc(), week.Analy.get_max(),
                 week.Analy.get_median(),
                 week.Analy.get_mean(), week.Analy.get_total(), week.Analy.get_perc(),
                 week.Confi.get_max(),
                 week.Confi.get_median(), week.Confi.get_mean(), week.Confi.get_total(), week.Confi.get_perc(),
                 week.Tenta.get_max(),
                 week.Tenta.get_median(),
                 week.Tenta.get_mean(), week.Tenta.get_total(), week.Tenta.get_perc()])


def sum_total(path):
    missing_values = ["NaN", "0"]
    # print(os.listdir(path))
    sums = list()
    for i in range(0, 7):
        sums.append(0)
    for filename in natsorted(os.listdir(path), key=lambda y: y.lower()):
        if not filename.startswith('.'):
            with open(os.path.join(path, filename)) as f:

                data = pd.read_csv(f, header=0, sep=r'\s*,\s*', na_values=missing_values, engine='python',
                                   usecols=[5, 6, 7, 8, 9, 10, 11])

                for ind in data.index:
                    if data['Analy'][ind] > 0.5:
                        sums[0] += data['Analy'][ind]
                    if data['Sad'][ind] > 0.5:
                        sums[1] += data['Sad'][ind]
                    if data['Confi'][ind] > 0.5:
                        sums[2] += data['Confi'][ind]
                    if data['Anger'][ind] > 0.5:
                        sums[3] += data['Anger'][ind]
                    if data['Tenta'][ind] > 0.5:
                        sums[4] += data['Tenta'][ind]
                    if data['Fear'][ind] > 0.5:
                        sums[5] += data['Fear'][ind]
                    if data['Joy'][ind] > 0.5:
                        sums[6] += data['Joy'][ind]
    return sums


def write_overall(path, source, desk):
    sums = sum_total(path)
    file_name = source + "_" + desk + ".csv"
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            ["Anger", "Sad", "Fear", "Joy", "Analy", "Confi", "Tenta"])
        writer.writerow([sums[0], sums[1], sums[2], sums[3], sums[4], sums[5], sums[6]])


def main():
    for p in the_paths:
        # write_overall(p, "NYT", p[p.rfind("/") + 1:])
        write_overall(p, "Guardian", p[p.rfind("/") + 1:])


main()
