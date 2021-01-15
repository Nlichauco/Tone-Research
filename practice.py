from plotly.subplots import make_subplots
import plotly.graph_objects as go
from AutoPlot import *
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=("Plot 1", "Plot 2", "Plot 3", "Plot 4"))

fig.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6]),
              row=1, col=1)


# fig.add_trace(go.Scatter(x=[1.5, 2.5, 3.5], y=[4, 5, 6]),
#               row=1, col=1)
#
#
# fig.add_trace(go.Scatter(x=[20, 30, 40], y=[50, 60, 70]),
#               row=1, col=2)
#
# fig.add_trace(go.Scatter(x=[300, 400, 500], y=[600, 700, 800]),
#               row=2, col=1)
#
# fig.add_trace(go.Scatter(x=[4000, 5000, 6000], y=[7000, 8000, 9000]),
#               row=2, col=2)

fig.update_layout(height=500, width=700,
                  title_text="Multiple Subplots with Titles")

fig.show()

def func(fname,row,col):
    data = GetCols(fname, tone_col)

for i in range(0,rows):
    row=i+1
    for j in range(0,cols):
        col=j+1
        func(filename,row,col)
