from dash import dcc, html, Input, Output, callback
import plotly.express as px

df = px.data.iris()  # iris is a pandas DataFrame
fig = px.scatter(df, x="sepal_width", y="sepal_length")

layout = html.Div([
    html.H1('Inventory'),
    dcc.Graph(figure=fig),
])
