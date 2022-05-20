import dash
from dash import Dash, dash_table, dcc, html, Input, Output, callback, State
import pandas as pd
import dash_bootstrap_components as dbc

df = pd.read_csv('data/amazon_iphone13_phone_cases_25_1_2022.csv')

modal_1 = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Reprice")),
        dbc.ModalBody(children=[], id="reprice_body"),
        dbc.ModalFooter(
            dbc.Button(
                "Conduct a demo",
                id="open_demo_button",
                className="ms-auto",
                n_clicks=0,
            )
        ),
    ],
    id="reprice_modal",
    size="lg",
    is_open=False,
)

modal_2 = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Modal 2")),
        dbc.ModalBody("This is the second modal"),
    ],
    id="demo_modal",
    size="lg",
    is_open=False,
)

layout = html.Div([
    html.H1('Inventory'),
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
                    dbc.Button('Reprice', id='reprice-button', n_clicks=0),
                    modal_1,
                    modal_2,
                    dbc.Alert(
                        "Please select a product!",
                        id="reprice_alert",
                        dismissable=True,
                        is_open=False,
                        color="danger"
                    ),
                ]
            )
        )
    )
])


@callback(
    [
        Output("reprice_modal", "is_open"),
        Output("reprice_alert", "is_open"),
    ],
    [
        Input("reprice-button", "n_clicks"),
        Input("open_demo_button", "n_clicks"),
    ],
    [
        State("reprice_modal", "is_open"),
        State("datatable", "selected_rows"),
    ],
    prevent_initial_call=True
)
def toggle_reprice_modal(n0, n1, is_open_modal, selected_rows):
    if len(selected_rows) > 0:
        if n0 or n1:
            return (not is_open_modal), False
    elif n0 != 0:
        return dash.no_update, True
    else:
        return False, False


@callback(
    Output("reprice_modal", "children"),
    Input("reprice-button", "n_clicks"),
    State("datatable", "selected_rows"),
    prevent_initial_call=True
)
def reprice(n_click, selected_rows):
    if len(selected_rows) > 0:
        row_index = selected_rows[0]
        print(df.loc[row_index]['Price'])
        parse_price = df.loc[row_index]['Price'].split('$')
        print(parse_price)

        if n_click:
            reprice_layout = dbc.Card(
                dcc.Graph(
                    figure={
                        'data': [
                            {'x': [1, 2], 'y': [float(parse_price[1]), 35], 'type': 'bar', 'name': 'SF'},
                        ],
                        'layout': {
                            'title': 'Repriceee'
                        }
                    }
                ),
            )
            return reprice_layout
    else:
        print("No rows selected.")


@callback(
    Output("demo_modal", "is_open"),
    Input("open_demo_button", "n_clicks"),
    [State("demo_modal", "is_open")],
    prevent_initial_call=True
)
def toggle_demo_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open
