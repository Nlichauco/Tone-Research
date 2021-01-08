import chart_studio
import chart_studio.plotly as py
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd


def GetCols(filename, col):
    ToneScores = []
    df = pd.read_csv(filename, usecols=[col])
    list = df.keys()
    ToneScores = df[list[0]].tolist()
    return ToneScores


def makePlot(filenames):
    fig = go.Figure()
    weeks = GetCols(filenames[0], 0)
    for i in range(0, len(filenames)):
        fname = filenames[i]
        data = GetCols(filenames[i], 19)
        traceName = fname[:fname[i].find(".")]
        fig.add_trace(go.Scatter(x=weeks, y=data, name=traceName))
    fig.update_xaxes(title_text="Weeks", title_font_size=18)
    fig.update_yaxes(title_text="Analytical Tone Scores", title_font_size=18, range=[.48, 1])
    fig.show()


def main():
    filenames = ["GuardianSci.csv", "GuardianOped.csv"]
    makePlot(filenames)


main()
#
#
# trace0 = go.Scatter(x=[1, 2, 3, 4],y=[10, 15, 13, 17])
# trace1 = go.Scatter(x=[1, 2, 3, 4], y=[16, 5, 11, 9])
# data = [trace0, trace1]
#
# py.plot(data, filename = 'basic-line', auto_open=True)
