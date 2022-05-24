import pandas as pd
from dash import dash_table, html, Input, Output, callback
import dash_bootstrap_components as dbc

df = pd.read_csv('data/sales_data.csv')
df = df.drop(columns=['Lookup_Id', 'Lookup_Price', 'Lookup_Name'])

layout = html.Div([
    html.H1('Sales'),
    dbc.Card(
        dbc.CardBody(
            dbc.Col(
                [
                    dash_table.DataTable(
                        id='datatable',
                        columns=[
                            {"name": i, "id": i, "deletable": False, "selectable": False} for i in df.columns
                        ],
                        style_data={
                            'whiteSpace': 'normal',
                            'height': 'auto',
                        },
                        data=df.to_dict('records'),
                        editable=True,
                        filter_action="native", sort_action="native",
                        sort_mode="multi",
                        column_selectable=False,
                        row_selectable="single",
                        row_deletable=False,
                        selected_rows=[],
                        page_action="native",
                        page_current=0,
                        page_size=10,
                    ),
                ]
            )
        )
    )
])
