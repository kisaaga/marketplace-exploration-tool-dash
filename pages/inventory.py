from dash import dash, dash_table, dcc, html, Input, Output, callback, State, ctx
import pandas as pd
import dash_bootstrap_components as dbc

df = pd.read_csv('data/inventory_data.csv')

reprice = 0

modal_1 = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Reprice")),
        dbc.ModalBody(children=[], id="reprice_body"),
        dbc.ModalFooter(
            html.Div(
                [
                    dbc.Button(
                        "Conduct a demo",
                        id="open_demo_button",
                        className="ms-auto",
                        n_clicks=0,
                    ),

                    dbc.Button(
                        "Accept New Price",
                        id="accept_button",
                        className="ms-auto",
                        n_clicks=0,
                    ),
                ],
                className="d-grid gap-2 d-md-flex justify-content-md-end",
            ),
        ),
    ],
    id="reprice_modal",
    size="xl",
    is_open=False,
)

modal_2 = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Reprice Demo")),
        dbc.ModalBody(
            children=[
                dbc.Col(
                    children=[
                        html.H6(
                            "In this page, you can project the effects of the calculated price to sales in the "
                            "future. Please enter the projected time range to start the demo.",
                            style={'textAlign': 'center', 'padding': 10}),

                        dbc.InputGroup(
                            [
                                dbc.Input(id="month_input", placeholder="Amount", type="number", min=1, step=1,
                                          value=1),
                                dbc.InputGroupText("Months"),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            children=[
                                dbc.Button(
                                    "Project for profit",
                                    id="profit_project_button",
                                    className="me-1",
                                    n_clicks=0,
                                    style={
                                        'width': '150px',
                                    }
                                ),
                                dbc.Button(
                                    "Project for sales",
                                    id="sales_project_button",
                                    className="me-1",
                                    n_clicks=0,
                                    style={
                                        'width': '150px',
                                    }
                                )
                            ],
                            justify="around",
                            style={
                                'margin-bottom': '15px',
                            }
                        ),
                        dbc.Card(
                            id="demo_card",
                            children=[]
                        )
                    ]
                )

            ]
        ),
    ],
    id="demo_modal",
    size="xl",
    is_open=False,
)

modal_3 = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Success")),
        dbc.ModalBody("New price successfully saved"),
    ],
    id="Success_modal",
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
    Output("reprice_body", "children"),
    Input("reprice-button", "n_clicks"),
    State("datatable", "selected_rows"),
    prevent_initial_call=True
)
def reprice(n_click, selected_rows):
    if len(selected_rows) > 0:
        row_index = selected_rows[0]
        print(df.loc[row_index]['Price'])
        parse_price = df.loc[row_index]['Price'].split('$')
        parse_price_int = parse_price[1].split('.')
        reprice = 35
        print(parse_price)
        print(parse_price_int[0])
        percentage_change = ((reprice - int(parse_price_int[0])) / int(parse_price_int[0])) * 100
        print(percentage_change)

        if n_click:
            reprice_layout = dbc.Card(
                dbc.CardBody(
                    dbc.Row(
                        [
                            dbc.Col(

                                dcc.Graph(
                                    figure={
                                        'data': [
                                            {'x': ['Reprice', 'Current Price'], 'y': [float(parse_price[1]), reprice],
                                             'type': 'bar',
                                             'name': 'SF'},
                                        ],
                                        'layout': {
                                            'title': 'Reprice'
                                        }
                                    }
                                ),
                            ),
                            dbc.Col(
                                [
                                    dbc.Row(
                                        dbc.Card(
                                            [
                                                dbc.CardHeader("Old Price"),
                                                dbc.CardBody(
                                                    html.H5(parse_price[1]),
                                                ),
                                            ]
                                        ),
                                    ),
                                    html.Br(),
                                    dbc.Row(
                                        dbc.Card(
                                            [
                                                dbc.CardHeader("New Price"),
                                                dbc.CardBody(
                                                    html.H5("35.0"),
                                                ),
                                            ]
                                        ),
                                    ),
                                    html.Br(),
                                    dbc.Row(
                                        dbc.Card(
                                            [
                                                dbc.CardHeader("Percentage Change Between Current and New Price"),
                                                dbc.CardBody(
                                                    html.H5("%" + str(percentage_change)),
                                                ),
                                            ]
                                        ),
                                    ),
                                ]
                            ),
                        ],
                        align="center",
                    ),
                ),
            ),
            return reprice_layout
    else:
        print("No rows selected.")


@callback(
    Output("demo_modal", "is_open"),
    Input("open_demo_button", "n_clicks"),
    State("demo_modal", "is_open"),
    prevent_initial_call=True
)
def toggle_demo_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open


@callback(
    Output("demo_card", "children"),
    [Input("profit_project_button", "n_clicks"),
     Input("sales_project_button", "n_clicks"), ],
    State("month_input", "value"),
    prevent_initial_call=True
)
def demo_project(n1, n2, month):
    button_clicked = ctx.triggered_id
    if button_clicked == "profit_project_button":
        demo_graph_layout = dbc.Card(
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2], 'y': [45, 35], 'type': 'bar', 'name': 'SF'},
                    ],
                    'layout': {
                        'title': 'Repriceee'
                    }
                }
            ),
        )
    elif button_clicked == "sales_project_button":
        demo_graph_layout = dbc.Card(
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2], 'y': [12, 35], 'type': 'bar', 'name': 'SF'},
                    ],
                    'layout': {
                        'title': 'Repriceee'
                    }
                }
            ),
        )
    return demo_graph_layout

@callback(
    Output("Success_modal", "is_open"),
    Input("accept_button", "n_clicks"),
    [
        State("datatable", "selected_rows"),
        State("Success_modal", "is_open"),
    ],
)
def update_table(n_click, selected_rows, is_open):
    print("aaaaaa")
    if n_click:
        print("aaaaaa")
        row_index = selected_rows[0]
        df.loc[row_index, 'Price'] = str(reprice)
        df.to_csv("data/inventory_data.csv", index=False)
        return not is_open
    return is_open
