from dash import Dash, dash_table, dcc, html, Input, Output, callback, State
import pandas as pd
import dash_bootstrap_components as dbc

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

modal_1 = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Modal 1")),
        dbc.ModalBody("This is the content of the first modal"),
        dbc.ModalFooter(
            dbc.Button(
                "Open Modal 2",
                id="open-toggle-modal-2",
                className="ms-auto",
                n_clicks=0,
            )
        ),
    ],
    id="toggle-modal-1",
    size="lg",
    is_open=False,
)

modal_2 = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Modal 2")),
        dbc.ModalBody("This is the second modal"),
        dbc.ModalFooter(
            dbc.Button(
                "Back to Modal 1",
                id="open-toggle-modal-1",
                className="ms-auto",
                n_clicks=0,
            )
        ),
    ],
    id="toggle-modal-2",
    size="lg",
    is_open=False,
)

layout = html.Div([
    html.H1('Inventory'),
    dbc.Card(
        dbc.CardBody(
            [
                dbc.Row(
                    dash_table.DataTable(
                        id='datatable-interactivity',
                        columns=[
                            {"name": i, "id": i, "deletable": False, "selectable": False} for i in df.columns
                        ],
                        data=df.to_dict('records'),
                        editable=False,
                        filter_action="native", sort_action="native",
                        sort_mode="multi",
                        column_selectable=False,
                        row_selectable="single",
                        row_deletable=False,
                        selected_columns=[],
                        selected_rows=[],
                        page_action="native",
                        page_current=0,
                        page_size=18,
                    ),
                ),
                dbc.Row(
                    dbc.Col(
                        [dbc.Button('Reprice', id='open-toggle-modal', n_clicks=0),
                         modal_1,
                         modal_2,
                         ]
                    ),
                ),
            ]
        )
    ),
])


@callback(
    Output("toggle-modal-1", "is_open"),
    [
        Input("open-toggle-modal", "n_clicks"),
        Input("open-toggle-modal-1", "n_clicks"),
        Input("open-toggle-modal-2", "n_clicks"),
    ],
    [State("toggle-modal-1", "is_open")],
)
def toggle_modal_1(n0, n1, n2, is_open):
    if n0 or n1 or n2:
        return not is_open
    return is_open


@callback(
    Output("toggle-modal-2", "is_open"),
    [
        Input("open-toggle-modal-2", "n_clicks"),
        Input("open-toggle-modal-1", "n_clicks"),
    ],
    [State("toggle-modal-2", "is_open")],
)
def toggle_modal_2(n2, n1, is_open):
    if n1 or n2:
        return not is_open
    return is_open
