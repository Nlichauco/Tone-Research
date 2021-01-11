import plotly.graph_objects as go
import pandas as pd
from plotly.validators.scatter.marker import SymbolValidator
from IPython.display import Image

symbols = []
raw_symbols = SymbolValidator().values
for i in range(0, len(raw_symbols), 12):
    symbols.append(raw_symbols[i])


def GetCols(filename, col):
    df = pd.read_csv(filename, usecols=[col])
    list = df.keys()
    ToneScores = df[list[0]].tolist()
    return ToneScores


def makePlot(filenames, country, tone,tone_col):
    fig = go.Figure()
    weeks = GetCols(filenames[0], 0)
    # fig.update_layout(title=dict(bgcolor="#FFF" ))
    for i in range(0, len(filenames)):
        fname = filenames[i]
        start = fname.rfind("/")
        end = fname.rfind(".")
        fname = fname[start + 1:end + 1]
        data = GetCols(filenames[i], tone_col)
        traceName = fname[:fname[i].find(".")]
        fig.add_trace(
            go.Scatter(x=weeks, y=data, name=traceName, yaxis="y", mode='lines+markers', marker_symbol=symbols[i]))
    fig.update_xaxes(title_text="Weeks", title_font_size=18, tickangle=90,range=[-.25, 42.15])
    fig.update_yaxes(title_text=tone + " Tone Scores", title_font_size=18, range=[.5, 1])
    Covid_Data = GetCols("res/CovidData/UKcovidAVG.csv", 0)
    fig.update_layout(yaxis2=dict(
        title="Weekly Average Covid Cases in the " + country,
        titlefont=dict(
            size=17
        ),
        range=[0, 50000],
        anchor="x",
        overlaying="y",
        side="right"
    ))
    fig.add_trace(go.Scatter(x=weeks, y=Covid_Data, name='Covid cases', yaxis='y2', fill='tozeroy'))
    fig.update_layout(title_text="<b>(The Guardian) Weekly Average Analytical Tone Score per Primary Desk</b>")
    fig.update_layout(title_x=.01,paper_bgcolor="#FFF",
    plot_bgcolor='rgba(0,0,0,0)')
    fig.update_layout(title_font_size=20,width=900,height=520, autosize=True,margin=dict(
        l=100,
        r=10,
        b=100,
        t=100,
        pad=5
    ))
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

    # fig.write_image("fig1.png", width=1200, height=600, scale=1)
    fig.write_image("fig1.png")

#cross country comparison of tone (need tone name and source name )
#

def crossPlot(filenames, source_1,source_2, tone,tone_col):
    fig = go.Figure()
    weeks = GetCols(filenames[0], 0)
    # fig.update_layout(title=dict(bgcolor="#FFF" ))
    for i in range(0, len(filenames)):
        fname = filenames[i]
        start = fname.rfind("/")
        end = fname.rfind(".")
        if fname.find("Guardian")!=-1:
            fname=fname[start+1:end+1]
            traceName = "GRD "+fname[:fname[i].find(".")]
        else:
            fname=fname[start+1:end+1]
            traceName = "NYT "+fname[:fname[i].find(".")]
        data = GetCols(filenames[i], tone_col)
        fig.add_trace(
            go.Scatter(x=weeks, y=data, name=traceName, yaxis="y", mode='lines+markers', marker_symbol=symbols[i]))

    fig.update_xaxes(title_text="Weeks", title_font_size=18, tickangle=90,range=[-.25, 42.15])
    fig.update_yaxes(title_text=tone + " Tone Scores", title_font_size=18, range=[.5, 1])
    fig.update_layout(title_text="<b>Weekly Average " + tone + " Tone Score (" +source_1+ " Vs " + source_2+ ")</b>")
    fig.update_layout(title_x=.01,paper_bgcolor="#FFF",
    plot_bgcolor='rgba(0,0,0,0)')
    fig.update_layout(title_font_size=20,width=900,height=520, autosize=True,margin=dict(
        l=100,
        r=10,
        b=100,
        t=100,
        pad=5
    ))
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

    # fig.write_image("fig1.png", width=1200, height=600, scale=1)
    fig.show()


def PercPlot(filenames,country,tone,tone_col,CovidData):
    fig = go.Figure()
    weeks = GetCols(filenames[0], 0)
    # fig.update_layout(title=dict(bgcolor="#FFF" ))
    for i in range(0, len(filenames)):
        fname = filenames[i]
        start = fname.rfind("/")
        end = fname.rfind(".")
        if fname.find("Guardian")!=-1:
            fname=fname[start+1:end+1]
            traceName = "GRD "+fname[:fname[i].find(".")]
        else:
            fname=fname[start+1:end+1]
            traceName = "NYT "+fname[:fname[i].find(".")]
        data = GetCols(filenames[i], tone_col)
        fig.add_trace(
            go.Scatter(x=weeks, y=data, name=traceName, yaxis="y", mode='lines+markers', marker_symbol=symbols[i]))

    fig.update_xaxes(title_text="Weeks", title_font_size=18, tickangle=90,range=[-.25, 42.15])
    fig.update_yaxes(title_text=tone + " Tone Scores", title_font_size=18, range=[0, 1])
    fig.update_layout(title_text="<b>Ratio of Articles Possesing " + tone + " per Week</b>")
    fig.update_layout(title_x=.01,paper_bgcolor="#FFF",
    plot_bgcolor='rgba(0,0,0,0)')


    if CovidData==True:
        if country=="US":
            Covid_Data = GetCols('res/CovidData/UScovidAVG.csv', 0)
            high=250000
        else:
            Covid_Data = GetCols("res/CovidData/UKcovidAVG.csv", 0)
            high=50000
        fig.update_layout(yaxis2=dict(
            title="Weekly Average Covid Cases in the " + country,
            titlefont=dict(
                size=17
            ),
            range=[0, high],
            anchor="x",
            overlaying="y",
            side="right"
        ))
        fig.add_trace(go.Scatter(x=weeks, y=Covid_Data, name='Covid cases', yaxis='y2', fill='tozeroy'))

    fig.update_layout(title_font_size=20,width=900,height=520, autosize=True,margin=dict(
        l=100,
        r=10,
        b=100,
        t=100,
        pad=5
    ))
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

    # fig.write_image("fig1.png", width=1200, height=600, scale=1)
    fig.show()





def main():
    filenames = ['res/NYT/Opinion.csv','res/GuardianCSVs/BigCSV/Opinion.csv']
    #makePlot(filenames, "UK", "Analytical")
    #crossPlot(filenames,"NYT","GRD","Analytical")
    PercPlot(filenames,"UK","Sadness",10,CovidData=True)



main()
