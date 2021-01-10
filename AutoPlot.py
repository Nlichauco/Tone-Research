import plotly.graph_objects as go
import pandas as pd
from plotly.validators.scatter.marker import SymbolValidator

symbols = []
raw_symbols = SymbolValidator().values
for i in range(0, len(raw_symbols), 12):
    symbols.append(raw_symbols[i])


def GetCols(filename, col):
    df = pd.read_csv(filename, usecols=[col])
    list = df.keys()
    ToneScores = df[list[0]].tolist()
    return ToneScores


def makePlot(filenames, country, tone):
    fig = go.Figure()
    weeks = GetCols(filenames[0], 0)
    fig.update_layout(title=dict(text="", ))
    for i in range(0, len(filenames)):
        fname = filenames[i]
        data = GetCols(filenames[i], 19)
        traceName = fname[:fname[i].find(".")]
        fig.add_trace(
            go.Scatter(x=weeks, y=data, name=traceName, yaxis="y", mode='lines+markers', marker_symbol=symbols[i]))

    fig.update_xaxes(title_text="Weeks", title_font_size=18, tickangle=90)
    fig.update_yaxes(title_text=tone + " Tone Scores", title_font_size=18, range=[.5, 1])
    # fig = make_subplots(specs=[[{"secondary_y": True}]])
    Covid_Data = GetCols("UKcovidAVG.csv", 0)

    fig.update_layout(yaxis2=dict(
        title="Weekly Average Covid Cases in the " + country,
        titlefont=dict(
            color="#d62728"
        ),
        range=[0, 50000],
        anchor="x",
        overlaying="y",
        side="right"
    ))

    fig.add_trace(go.Scatter(x=weeks, y=Covid_Data, name='<b>Covid cases</b>', yaxis='y2', fill='tozeroy'))

    fig.update_layout(title_text="Weekly Average Analytical Tone Score per Primary Desk")
    fig.update_layout(title_x=.1)
    fig.update_layout(title_font_size=20)
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
        margin=dict(
            l=0,
            r=50,

        ))

    fig.show()


def main():
    filenames = ['/Users/nathaniel/Desktop/Tone-Research/res/GuardianCSVs/Business/BIGCSV/Guardian-Business.csv','/Users/nathaniel/Desktop/Tone-Research/res/GuardianCSVs/Opinion/BigCSV/Guardian-Opinion.csv']
    makePlot(filenames)


main()
