from Funcs import *

import pandas as pd

the_paths = ['/Users/ff/Desktop/nyt/business', '/Users/ff/Desktop/nyt/opinion']


def bigCSV(paths):
    for path in paths:
        section = path[path.rfind('/') + 1:]
        weeks = ReadSection(path)
        weekwrite(weeks, section)


def GetToneAvgs(filename):
    fields = ["Anger_avg", "Sad_avg", "Fear_avg", "Joy_avg", "Analy_avg", "Confi_avg", "Tenta_avg"]
    filename = filename + ".csv"
    df = pd.read_csv(filename, usecols=fields)
    Sad_mean = df["Sad_avg"]
    Fear_mean = df["Fear_avg"]
    Anger_mean = df["Anger_avg"]
    Tenta_mean = df["Tenta_avg"]
    Joy_mean = df["Joy_avg"]
    Confi_mean = df["Confi_avg"]
    Analy_mean = df["Analy_avg"]
    return Sad_mean, Fear_mean, Anger_mean, Tenta_mean, Joy_mean, Confi_mean, Analy_mean


bigCSV(the_paths)
