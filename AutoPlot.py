import csv

import plotly.graph_objects as go
import pandas as pd
from plotly.validators.scatter.marker import SymbolValidator

from BigCSV import sum_total

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
    # fig.update_layout(title=dict(bgcolor="#FFF" ))
    for i in range(0, len(filenames)):
        fname = filenames[i]
        start = fname.rfind("/")
        end = fname.rfind(".")
        fname = fname[start + 1:end + 1]
        data = GetCols(filenames[i], 33)
        traceName = fname[:fname[i].find(".")]
        fig.add_trace(
            go.Scatter(x=weeks, y=data, name=traceName, yaxis="y", mode='lines+markers', marker_symbol=symbols[i]))
    fig.update_xaxes(title_text="Weeks", title_font_size=18, tickangle=90, showgrid=False, range=[-.25, 42.15])
    fig.update_yaxes(title_text=tone + " Tone Scores", title_font_size=18, range=[.5, 1], showgrid=False)
    # fig = make_subplots(specs=[[{"secondary_y": True}]])

    Covid_Data = GetCols("res/CovidData/UScovidAVG.csv", 0)
    fig.update_layout(yaxis2=dict(
        title="Weekly Average Covid Cases in the " + country,
        titlefont=dict(
            size=18
        ),
        range=[0, 50000],
        anchor="x",
        overlaying="y",
        side="right"
    ))
    fig.add_trace(go.Scatter(x=weeks, y=Covid_Data, name='Covid cases', yaxis='y2', fill='tozeroy'))
    fig.update_layout(title_text="Weekly Average Analytical Tone Score per Primary Desk")
    fig.update_layout(title_x=.1, paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)')
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

    # fig.write_image("fig1.png", width=1200, height=600, scale=1)
    fig.show()


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
    filenames = ['res/NYT/Overall/NYT_Business.csv',
                 'res/NYT/Overall/NYT_Science.csv',
                 'res/NYT/Overall/NYT_Politics.csv',
                 'res/NYT/Overall/NYT_Opinion.csv']
    # makePlot(filenames, "US", "Analytical")
    overall_graph_single_source(filenames, "New York Times")

    # GetCols("res/NYT/Business.csv", 3)


main()
