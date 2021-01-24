import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.validators.scatter.marker import SymbolValidator
import statistics as sta
symbols = []
raw_symbols = SymbolValidator().values
for i in range(0, len(raw_symbols), 12):
    symbols.append(raw_symbols[i])


def set_yaxes_range_avg(fig):
    fig.update_xaxes(title_text="Weeks", title_font_size=18)
    fig.update_yaxes(title_text="Weekly Avg Tone Scores", title_font_size=18, showgrid=True, gridcolor='black',
                     zeroline=True, zerolinewidth=1, zerolinecolor='black')

    fig.update_yaxes(range=[.5, .75])


def set_yaxes_range_percent(fig, tone):

    fig.update_yaxes(title_text="% Of Total Articles", title_font_size=18, range=[0, 100], ticksuffix="%")



def set_yaxes_range_total(fig):

    #fig.update_xaxes(title_text="Weeks", title_font_size=18)
    fig.update_yaxes(title_text="Cumulative Tone Score", title_font_size=18, showgrid=True, gridcolor='black',
                     zeroline=True, zerolinewidth=1, zerolinecolor='black')

    fig.update_yaxes(range=[0, 65])






def single_tone_four_desks_subplot(source, col_name, tone_name):


    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Business", "Opinion", "Science", "Politics"))

    df = pd.read_csv('res/' + source + '/Business.csv')
    df1 = pd.read_csv('res/' + source + '/Opinion.csv')
    df2 = pd.read_csv('res/' + source + '/Sport.csv')
    df3 = pd.read_csv('res/' + source + '/Politics.csv')

    fig.add_trace(go.Scatter(x=df['Week'], y=df[col_name],mode='lines+markers'),
                  row=1, col=1)

    fig.add_trace(go.Scatter(x=df1['Week'], y=df1[col_name],mode='lines+markers'),
                  row=1, col=2)

    fig.add_trace(go.Scatter(x=df2['Week'], y=df2[col_name],mode='lines+markers'),
                  row=2, col=1)

    fig.add_trace(go.Scatter(x=df3['Week'], y=df3[col_name],mode='lines+markers'),
                  row=2, col=2)

    fig.update_layout(height=800, width=1500,
                      title_text=source)
    fig.update_xaxes(title_text="Weeks", title_font_size=18,tickangle=90)
    fig.update_yaxes(title_text="Weekly Cumulative " + tone_name + " Tone Score", title_font_size=18,
                     showgrid=False)
    fig.update_layout(title_x=.1,
                      yaxis_title_font_size=18,
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)', title_font_size=20, autosize=True,
                      margin=dict(
                          pad=10
                      ))
    fig.update_yaxes(showgrid=True, gridcolor='black')
    fig.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='black',range=[0,75])
    fig.show()
    #fig.write_image("31.eps", width=2000, height=1000, scale=1)


def cross_source_comparison(desk,stat):


    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Analytical Tone Comparison", "Fear Tone Comparison", "Tentative Tone Comparison", "Sad Tone Comparison"))
    df=pd.read_csv('res/Guardian/Opinion.csv')
    #df = pd.read_csv('res/NYT/' + desk + '.csv')
    df1 = pd.read_csv('res/Guardian/' + desk + '.csv')

    fig.add_traces(
        [go.Scatter(x=df['Week'], y=df["Analy_"+stat], name="NYT", mode='lines+markers',
                    marker=dict(color='red', symbol=symbols[0]), line=dict(color='red')),
         go.Scatter(x=df1['Week'], y=df1["Analy_"+stat], name="Guardian", mode='lines+markers',
                    marker=dict(color='blue', symbol=symbols[1]), line=dict(color='blue'))],
        rows=1, cols=1)

    fig.add_traces(
        [go.Scatter(x=df['Week'], y=df["Fear_"+stat], showlegend=False, mode='lines+markers',
                    marker=dict(color='red', symbol=symbols[0]), line=dict(color='red')),
         go.Scatter(x=df1['Week'], y=df1["Fear_"+stat], showlegend=False, mode='lines+markers',
                    marker=dict(color='blue', symbol=symbols[1]), line=dict(color='blue'))],
        rows=1, cols=2)

    fig.add_traces(
        [go.Scatter(x=df['Week'], y=df["Tenta_"+stat], showlegend=False, mode='lines+markers',
                    marker=dict(color='red', symbol=symbols[0]), line=dict(color='red')),
         go.Scatter(x=df1['Week'], y=df1["Tenta_"+stat], showlegend=False, mode='lines+markers',
                    marker=dict(color='blue', symbol=symbols[1]), line=dict(color='blue'))],
        rows=2, cols=1)

    fig.add_traces(
        [go.Scatter(x=df['Week'], y=df["Sad_"+stat], showlegend=False, mode='lines+markers',
                    marker=dict(color='red', symbol=symbols[0]), line=dict(color='red')),
         go.Scatter(x=df1['Week'], y=df1["Sad_"+stat], showlegend=False, mode='lines+markers',
                    marker=dict(color='blue', symbol=symbols[1]), line=dict(color='blue'))],
        rows=2, cols=2)

    fig.update_layout(height=800, width=1500,
                      title={
                          'text': desk + ' Comparison, NYT VS Guardian',
                          'y': 0.95,
                          'x': 0.5,
                          'xanchor': 'center',
                          'yanchor': 'top'
                      })

    if stat=='total':
        set_yaxes_range_total(fig)
    elif stat=="ratio":
        set_yaxes_range_percent(fig)
    else:
        set_yaxes_range_avg(fig)




    fig.update_layout(
        yaxis_title_font_size=18,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)', title_font_size=20, autosize=True,
        margin=dict(
            pad=10
        ))

    # fig.write_image("31.eps", width=2000, height=1000, scale=1)
    fig.show()


#single_tone_four_desks_subplot("Guardian", "Analy_total", "Analytical")
cross_source_comparison("Politics","total")
