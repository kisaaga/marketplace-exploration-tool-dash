from dash import dcc, html, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc

df = px.data.iris()  # iris is a pandas DataFrame
fig = px.scatter(df, x="sepal_width", y="sepal_length")

layout = html.Div([
    html.H1('Dashboard'),
    dbc.Row(
        [
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H3("Units Sold", className="card-title"),
                        html.H4(
                            [
                                "1943",
                            ],
                            className="card-text",
                        ),
                    ]
                ),
            ),
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H3("Units Sold", className="card-title"),
                        html.H4(
                            [
                                "1943",
                            ],
                            className="card-text",
                        ),
                    ]
                ),
            ),
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H3("Units Sold", className="card-title"),
                        html.H4(
                            [
                                "1943",
                            ],
                            className="card-text",
                        ),
                    ]
                ),
            ),
        ]
    ),
])
