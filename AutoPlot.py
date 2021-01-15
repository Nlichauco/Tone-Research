import csv

import plotly.graph_objects as go
import pandas as pd
from plotly.validators.scatter.marker import SymbolValidator

from BigCSV import sum_total
import statistics as stat

symbols = []
raw_symbols = SymbolValidator().values
for i in range(0, len(raw_symbols), 12):
    symbols.append(raw_symbols[i])


def GetCols(filename, col):
    df = pd.read_csv(filename, usecols=[col])
    list = df.keys()
    ToneScores = df[list[0]].tolist()
    return ToneScores


def GetCovData(country):
    if country=="US":
        Covid_Data = GetCols("res/CovidData/UScovidAVG.csv", 0)
    elif country=="UK":
        Covid_Data = GetCols("res/CovidData/UKcovidAVG.csv", 0)
    return Covid_Data

def FormatFig(Covid_Data,fig,tone,country,weeks):
    fig.update_layout(yaxis2=dict(title="Weekly Avg. Covid Cases in the " + country,titlefont=dict(size=18),range=[0, 50000],anchor="x",overlaying="y",side="right"))
    fig.add_trace(go.Scatter(x=weeks, y=Covid_Data, name='Covid cases', yaxis='y2', fill='tozeroy'))
    fig.update_layout(title_text="<b>(The Guardian) Weekly Avg. " + tone + " Tone Score per Desk</b>")
    fig.update_layout(title_x=.01, paper_bgcolor="#FFF",
                      plot_bgcolor='rgba(0,0,0,0)')
    fig.update_layout(title_font_size=20, width=900, height=520, autosize=True, margin=dict(l=100,r=10,b=100,t=100,pad=5))
    fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),margin=dict(l=0,r=50,))
    fig.update_yaxes(gridcolor='black')
    return fig

# same tone mutliple desks
def makePlot(filenames, country, tone, tone_col):
    fig = go.Figure()
    weeks = GetCols(filenames[0], 0)
    for i in range(0, len(filenames)):
        fname = filenames[i]
        start = fname.rfind("/")
        end = fname.rfind(".")
        fname = fname[start + 1:end + 1]
        data = GetCols(filenames[i], tone_col)
        traceName = fname[:fname[i].find(".")]
        fig.add_trace(
            go.Scatter(x=weeks, y=data, name=traceName, yaxis="y", mode='lines+markers', marker_symbol=symbols[i]))
    fig.update_xaxes(title_text="Weeks", title_font_size=18, tickangle=90, showgrid=False, range=[-.25, 42.15])
    fig.update_yaxes(title_text=tone + " Tone Scores", title_font_size=18, range=[.5, 1], showgrid=False)
    Covid_Data = GetCovData(country)
    FormatFig(Covid_Data,fig,tone,country,weeks)
    # fig.write_image("fig1.png", width=1200, height=600, scale=1)
    fig.write_image("fig1.png")


"""
Used to Plot average of a tone score across multiple desks
Args:
    filenames: List of files you want to plot from
    source_1: News source one
    source_2: Another News source
    tone: String literal of the tone you want to plot, ex. "Analytical"
    tone_col: Singular Index associated with what you want to plot

Returns:
    Nothing, creates a plot.
    """


def crossPlot(filenames, source_1, source_2, tone, tone_col):
    fig = go.Figure()
    weeks = GetCols(filenames[0], 0)
    for i in range(0, len(filenames)):
        fname = filenames[i]
        start = fname.rfind("/")
        end = fname.rfind(".")
        if fname.find("Guardian") != -1:
            fname = fname[start + 1:end + 1]
            traceName = "GRD " + fname[:fname[i].find(".")]
        else:
            fname = fname[start + 1:end + 1]
            traceName = "NYT " + fname[:fname[i].find(".")]
        data = GetCols(filenames[i], tone_col)
        fig.add_trace(
            go.Scatter(x=weeks, y=data, name=traceName, yaxis="y", mode='lines+markers', marker_symbol=symbols[i]))

    fig.update_xaxes(title_text="Weeks", title_font_size=18, tickangle=90, range=[-.25, 42.15])
    fig.update_yaxes(title_text=tone + " Tone Scores", title_font_size=18, range=[.5, 1])
    fig.update_layout(title_text="<b>Weekly Avg. " + tone + " Tone Score (" + source_1 + " Vs " + source_2 + ")</b>")
    fig.update_layout(title_x=.01, paper_bgcolor="#FFF",plot_bgcolor='rgba(0,0,0,0)')
    fig.update_layout(title_font_size=20, width=900, height=520, autosize=True, margin=dict(
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
    saveName = tone + ".png"
    fig.update_yaxes(gridcolor='black')
    fig.write_image(saveName, width=1200, height=600, scale=1)
    # fig.show()


"""
Plots all the ratio tone scores of one tone given multiple sections
Args:
    filenames: List of files you want to plot from
    country: Country of the news source you are plotting from
    tone: String literal of the tone you want to plot, ex. "Analytical"
    tone_col: Singular Index associated with what you want to plot
    CovidData: Can be set to true of false, shows covid cases.

Returns:
    Nothing, creates a plot.
    """


def PercPlot(filenames, country, tone, tone_col, CovidData):
    fig = go.Figure()
    weeks = GetCols(filenames[0], 0)
    for i in range(0, len(filenames)):
        fname = filenames[i]
        start = fname.rfind("/")
        end = fname.rfind(".")
        if fname.find("Guardian") != -1:
            fname = fname[start + 1:end + 1]
            traceName = fname[:fname[i].find(".")]
            source = "GRD"
        else:
            fname = fname[start + 1:end + 1]
            traceName = fname[:fname[i].find(".")]
            source = "NYT"
        data = GetCols(filenames[i], tone_col)
        newdata = []
        for num in data:
            newdata.append(num * 100)
        fig.add_trace(
            go.Scatter(x=weeks, y=newdata, name=traceName, yaxis="y", mode='lines+markers', marker_symbol=symbols[i]))
    fig.update_xaxes(title_text="Weeks", title_font_size=18, tickangle=90, range=[-.25, 42.15])
    fig.update_yaxes(title_text="% Of Articles per Week With " + tone, title_font_size=18, range=[0, 100], ticksuffix="%")
    fig.update_layout(title_text="<b>(" + source + ") Weekly % of Articles With " + tone + "</b>")
    fig.update_layout(title_x=.01, paper_bgcolor="#FFF",plot_bgcolor='rgba(0,0,0,0)')
    if CovidData == True:
        if country == "US":
            Covid_Data = GetCols('res/CovidData/UScovidAVG.csv', 0)
            high = 250000
        else:
            Covid_Data = GetCols("res/CovidData/UKcovidAVG.csv", 0)
            high = 50000
        fig.update_layout(yaxis2=dict(
            title="Weekly Avg. Covid Cases in the " + country,
            titlefont=dict(
                size=17
            ),
            range=[0, high],
            anchor="x",
            overlaying="y",
            side="right"
        ))
        fig.add_trace(go.Scatter(x=weeks, y=Covid_Data, name='Covid cases', yaxis='y2', fill='tozeroy'))
    fig.update_layout(title_font_size=20, width=900, height=520, autosize=True, margin=dict(
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

    saveName = tone + "Ratio.png"
    fig.update_yaxes(gridcolor='black')
    fig.write_image(saveName, width=1200, height=600, scale=1)
    #fig.show()

"""
Plots all the cumulative tone scores of one tone given multiple sections
Args:
    filenames: List of files you want to plot from
    country: Country of the news source you are plotting from
    tone: String literal of the tone you want to plot, ex. "Analytical"
    tone_col: Singular Index associated with what you want to plot
    CovidData: Can be set to true of false, shows covid cases.

Returns:
    Nothing, creates a plot.
    """

def TotalPlot(filenames, country, tone, tone_col, CovidData,source):
    fig = go.Figure()
    big = 0
    weeks = GetCols(filenames[0],0)
    for i in range(0, len(filenames)):
        fname = filenames[i]
        start = fname.rfind("/")
        end = fname.rfind(".")
        fname = fname[start + 1:end + 1]
        traceName =fname[:fname[i].find(".")]

        data = GetCols(filenames[i], tone_col)
        fig.add_trace(
            go.Scatter(x=weeks, y=data, name=traceName, yaxis="y", mode='lines+markers', marker_symbol=symbols[i]))
        if big < max(data):
            big = max(data)
    fig.update_xaxes(title_text="Weeks", title_font_size=18, tickangle=90, range=[-.25, 42.15])
    fig.update_yaxes(title_text="Total "+tone + " Tone Score", title_font_size=18) #, range=[0, big+1]
    fig.update_layout(title_text="<b>Total " + tone + " Tone Score per Week ("+source +")</b>")
    fig.update_layout(title_x=.01, paper_bgcolor="#FFF",plot_bgcolor='rgba(0,0,0,0)')
    if CovidData == True:
        if country == "US":
            Covid_Data = GetCols('res/CovidData/UScovidAVG.csv', 0)
            high = 250000
        else:
            Covid_Data = GetCols("res/CovidData/UKcovidAVG.csv", 0)
            high = 50000
        fig.update_layout(yaxis2=dict(
            title="Weekly Avg. Covid Cases in the " + country,
            titlefont=dict(
                size=17
            ),
            range=[0, high],
            anchor="x",
            overlaying="y",
            side="right"
        ))
        fig.add_trace(go.Scatter(x=weeks, y=Covid_Data, name='Covid cases', yaxis='y2', fill='tozeroy'))
    fig.update_layout(title_font_size=20, width=900, height=520, autosize=True, margin=dict(
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
    #fig.update_yaxes(gridcolor='black')
    fig.write_image("fig1.png", width=1200, height=600, scale=1)
    #fig.show()


"""
Plots multiple tones from one file.
Args:
    file: Singular file you want to plot
    tones: array of indicies specifying which columns you want to plot
    tone_name: Associated names to the above indicies
    country: Country of the news source you are plotting from
Returns:
    Nothing, creates a plot.
    """

def MultiTonePlot(file, tones, tone_name, country):
    fig = go.Figure()
    weeks = GetCols(file, 0)
    fname = file
    for i in range(0, len(tones)):
        tone = tones[i]
        data = GetCols(file, tone)
        start = fname.rfind("/")
        end = fname.rfind(".")
        fname = fname[start + 1:end + 1]
        sectionName = fname[:fname.find(".")]
        fig.add_trace(
            go.Scatter(x=weeks, y=data, name=tone_name[i], yaxis="y", mode='lines+markers', marker_symbol=symbols[i]))

    fig.update_xaxes(title_text="Weeks", title_font_size=18, tickangle=90, range=[-.25, 42.15])
    fig.update_yaxes(title_text=sectionName + " Tone Scores", title_font_size=18, range=[.5, 1], showgrid=True)
    if country == "US":
        Covid_Data = GetCols('res/CovidData/UScovidAVG.csv', 0)
        high = 250000
        source = "NYT"
    else:
        Covid_Data = GetCols("res/CovidData/UKcovidAVG.csv", 0)
        high = 50000
        source = "GRD"
    fig.update_layout(yaxis2=dict(
        title="Weekly Avg. Covid Cases in the " + country,
        titlefont=dict(
            size=17
        ),
        range=[0, high],
        anchor="x",
        overlaying="y",
        side="right"
    ))
    fig.add_trace(go.Scatter(x=weeks, y=Covid_Data, name='Covid cases', yaxis='y2', fill='tozeroy'))
    fig.update_layout(title_text="<b> Weekly Avg. Tone Scores (" + source + " " + sectionName + ") </b>")
    fig.update_layout(title_x=.01, paper_bgcolor="#FFF",plot_bgcolor='rgba(0,0,0,0)')  # 'rgba(0,0,0,0)'229, 236, 246
    fig.update_layout(title_font_size=20, width=900, height=520, autosize=True, margin=dict(
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
    fig.update_yaxes(gridcolor='black')
    saveName = sectionName + ".png"
    fig.write_image(saveName, width=1200, height=600, scale=1)
    #fig.show()


def get_row(filename):
    t = []
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        next(reader)
        body = next(reader)
        for k in range(0, 7):
            t.append(int(float(body[k])))

    return t


def overall_graph_cross_compare(desk):
    source = ['New York Times', 'Guardian']
    nyt = get_row("res/NYT/Overall/NYT_" + desk + ".csv")
    guardian = get_row("res/Guardian/Overall/NYT_" + desk + ".csv")
    fig = go.Figure(data=[
        go.Bar(name='Anger', x=source, y=[nyt[0], guardian[0]]),
        go.Bar(name='Sad', x=source, y=[nyt[1], guardian[1]]),
        go.Bar(name='Fear', x=source, y=[nyt[2], guardian[2]]),
        go.Bar(name='Joy', x=source, y=[nyt[3], guardian[3]]),
        go.Bar(name='Analy', x=source, y=[nyt[4], guardian[4]]),
        go.Bar(name='Confi', x=source, y=[nyt[5], guardian[5]]),
        go.Bar(name='Tenta', x=source, y=[nyt[6], guardian[6]])
    ])
    graph_setup(fig)
    fig.update_xaxes(tickfont=dict(size=18))
    fig.update_layout(barmode='group',
                      title_text=desk + " Cumulative Score Comparison " + ",New York Times VS Guardian",
                      yaxis_title="Cumulative Tone Scores")
    fig.show()


def overall_graph_single_source(source):
    desks = ['Business', 'Science', 'Politics', 'Opinion']
    filenames = ['res/' + source + '/Overall/' + source + '_Business.csv',
                 'res/' + source + '/Overall/' + source + '_Science.csv',
                 'res/' + source + '/Overall/' + source + '_Politics.csv',
                 'res/' + source + '/Overall/' + source + '_Opinion.csv']
    t = [[], [], [], [], [], [], []]
    for filename in filenames:
        row = get_row(filename)
        for k in range(0, 7):
            t[k].append(row[k])

    fig = go.Figure(data=[
        go.Bar(name='Anger', x=desks, y=t[0]),
        go.Bar(name='Sad', x=desks, y=t[1]),
        go.Bar(name='Fear', x=desks, y=t[2]),
        go.Bar(name='Joy', x=desks, y=t[3]),
        go.Bar(name='Analy', x=desks, y=t[4]),
        go.Bar(name='Confi', x=desks, y=t[5]),
        go.Bar(name='Tenta', x=desks, y=t[6])
    ])
    graph_setup(fig)
    fig.update_yaxes(range=[0, 1000])
    fig.update_xaxes(tickfont=dict(size=18))
    fig.update_layout(barmode='group',
                      title_text="Overall Primary Desks Tone Scores For " + source,
                      yaxis_title="Cumulative Tone Scores")
    fig.show()


def graph_setup(fig):
    fig.update_layout(title_x=.1,
                      yaxis_title_font_size=18,
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)', title_font_size=20, width=900, height=520, autosize=True,
                      margin=dict(
                          l=100,
                          r=10,
                          b=100,
                          t=100,
                          pad=5
                      ),
                      legend=dict(
                          orientation="h",
                          yanchor="bottom",
                          y=1.02,
                          xanchor="right",
                          x=1
                      ))


def main():
    # filenames = ['res/NYT/Overall/NYT_Business.csv',
    #              'res/NYT/Overall/NYT_Science.csv',
    #              'res/NYT/Overall/NYT_Politics.csv',
    #              'res/NYT/Overall/NYT_Opinion.csv']
    # overall_graph_single_source(filenames, "New York Times")
    tones = ["Anger", "Sad", "Fear", "Joy", "Analytical", "Confidence", "Tentative"]
    cols = [3, 8, 13, 18, 23, 28, 33]
    nytFiles = ['res/NYT/Opinion.csv', 'res/NYT/Politics.csv']
    GuardFiles = ['res/GuardianCSVs/Business.csv','res/GuardianCSVs/Politics.csv','res/GuardianCSVs/Opinion.csv']
    filenames=['res/GuardianCSVs/Politics.csv','res/GuardianCSVs/Opinion.csv','res/NYT/Opinion.csv', 'res/NYT/Politics.csv']
    #MultiTonePlot('res/NYT/Opinion.csv', cols, tones, "US")
    #PercPlot(GuardFiles, "UK", "Sad", 10, True)
    makePlot(GuardFiles, "UK", "Analytical", 23)
    #crossPlot(filenames, "NYT", "GRD", "Tentative", 33)
    #TotalPlot(GuardFiles,"UK","Sad",9,True,"GRD")


main()
