from plotly.subplots import make_subplots
import plotly.graph_objects as go
from AutoPlot import *
weeks = GetCols('res/NYT/Opinion.csv', 0)
fig = make_subplots(
rows=2, cols=2,
subplot_titles=("Plot 1", "Plot 2", "Plot 3", "Plot 4"))

fig.add_trace(go.Scatter(x=weeks, y=[4, 5,6,4,6,1,2,5,2,3,5,1,2,4,1,2,3,4,2,3,5,2,3,5,1,2,3,5,1,23,5,1,3,5]),
              row=1, col=1)


fig.add_trace(go.Scatter(x=weeks, y=[4, 5,6,4,6,1,2,5,2,3,5,1,2,4,1,2,3,4,2,3,5,2,3,5,1,2,3,5,1,23,5,1,3,5]),
              row=1, col=1)


fig.add_trace(go.Scatter(x=weeks, y=[4, 5,6,4,6,1,2,5,2,3,5,1,2,4,1,2,3,4,2,3,5,2,3,5,1,2,3,5,1,23,5,1,3,5]),
              row=1, col=2)

fig.add_trace(go.Scatter(x=weeks, y=[4, 5,6,4,6,1,2,5,2,3,5,1,2,4,1,2,3,4,2,3,5,2,3,5,1,2,3,5,1,23,5,1,3,5]),
              row=2, col=1)

fig.add_trace(go.Scatter(x=weeks, y=[7000, 8000, 9000]),
              row=2, col=2)

fig.update_layout(height=800, width=1200,
                  title_text="Multiple Subplots with Titles")

fig.show()
