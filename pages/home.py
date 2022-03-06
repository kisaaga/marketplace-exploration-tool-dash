from dash import dcc, html, Input, Output, callback

layout = html.Div([
    dcc.Link('Go to Page 1', href='/page1'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page2'),
])