from dash import dcc, html, Input, Output, callback
import plotly.express as px

df = px.data.iris()  # iris is a pandas DataFrame
fig = px.scatter(df, x="sepal_width", y="sepal_length")

layout = html.Div([
    html.H3('Page 2'),
    dcc.Dropdown(
        {f'Page 2 - {i}': f'{i}' for i in ['London', 'Berlin', 'Paris']},
        id='page-2-dropdown'
    ),
    html.Div(id='page-2-display-value'),
    dcc.Graph(figure=fig),
    dcc.Link('Go to Page 1', href='/page1')
])


@callback(
    Output('page-2-display-value', 'children'),
    Input('page-2-dropdown', 'value'))
def display_value(value):
    return f'You have selected {value}'
