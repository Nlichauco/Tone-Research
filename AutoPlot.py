import chart_studio
import chart_studio.plotly as py
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
Plotkey="dymEazJoXLUsbf5wCGxf"

chart_studio.tools.set_credentials_file(username='NateL777', api_key=Plotkey)



def GetCols(filename,col):
    ToneScores=[]
    df = pd.read_csv(filename, usecols = [col])
    list=df.keys()
    ToneScores=df[list[0]].tolist()
    return ToneScores


def makePlot(filenames):
    fig = go.Figure()
    weeks=GetCols(filenames[0],0)
    fig.update_layout(title=dict(text="",))
    for i in range(0,len(filenames)):
        fname=filenames[i]
        data=GetCols(filenames[i],19)
        traceName=fname[:fname[i].find(".")]
        fig.add_trace(go.Scatter(x=weeks, y=data, name=traceName))
    fig.update_xaxes(title_text="Weeks",title_font_size=18)
    fig.update_yaxes(title_text="Analytical Tone Scores",title_font_size=18,range=[.48,1])


    #fig.update_layout(legend_title_text="Weekly Average Analytical Tone Score per Primary Desk")
    # fig.update_layout(legend_title=dict(
    # text="Weekly Average Analytical Tone Score per Primary Desk"
    # ),legend_title_font_size=20,legend_title_side="")
    fig.update_layout(title_text="Weekly Average Analytical Tone Score per Primary Desk")
    fig.update_layout(title_x=.1)
    fig.update_layout(title_font_size=20)
    fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
    ))

    #legend_title_side="top"
    #fig.update_layout(legend_orientation="h")
    fig.show()




def main():
    filenames=["GuardianSci.csv","GuardianOped.csv"]
    makePlot(filenames)




main()
    
