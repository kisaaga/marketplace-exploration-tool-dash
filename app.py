# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv('data/amazon_iphone13_phone_cases_25_1_2022.csv')

dfg=df.groupby('Brand').count().reset_index()
dfg=dfg.rename(columns={"Title": "Count"})

fig = px.bar(dfg, x="Brand", y="Count", barmode='stack')

app.layout = html.Div(children=[
    dcc.Tabs([
        dcc.Tab(label='Tab one', ),
        dcc.Tab(label='Tab two'),
        dcc.Tab(label='Tab three'),
    ]),

    html.H1(children='Dashboard'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(id='life-exp-vs-gdp',
        figure=fig),

    generate_table(df)


])

if __name__ == '__main__':
    app.run_server(debug=True)
