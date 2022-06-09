from dash import dash, dash_table, dcc, html, Input, Output, callback, State, ctx
import pandas as pd
import dash_bootstrap_components as dbc

from pages.utils import get_price_from_model

df = pd.read_csv('data/inventory_data.csv')

reprice = 0

reprice_modal = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Reprice")),
        dbc.ModalBody(children=[], id="reprice_body"),
        dbc.ModalFooter(
            html.Div(
                [
                    dbc.Button(
                        "How is this calculated?",
                        id="explain_button",
                        className="ms-auto",
                        color="info",
                        n_clicks=0,
                    ),
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
                        color="danger",
                        n_clicks=0,
                    ),
                ],
                className="d-grid gap-2 d-md-flex justify-content-md-end",
            ),
        ),
        dbc.Alert(
            "New price successfully saved",
            id="success",
            dismissable=True,
            is_open=False,
            color="success"
        ),
    ],
    id="reprice_modal",
    size="xl",
    is_open=False,
)

demo_modal = dbc.Modal(
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
                                    "Project For Profit",
                                    id="profit_project_button",
                                    className="me-1",
                                    n_clicks=0,
                                    style={
                                        'width': '150px',
                                    }
                                ),
                                dbc.Button(
                                    "Project For Sales",
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

explain_modal = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("How is the suggested price calculated?")),
        dbc.ModalBody(children=[], id="explain_body"),
        dbc.ModalFooter(
            html.Div(
                [
                    dbc.Button(
                        "Go Back",
                        id="explain_back_button",
                        className="ms-auto",
                        color="primary",
                        n_clicks=0,
                    ),
                ],
                className="d-grid gap-2 d-md-flex justify-content-md-end",
            ),
        ),
    ],
    id="explain_modal",
    size="xl",
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
                        style_cell={'textAlign': 'left'},
                        css=[{
                            'selector': '.dash-spreadsheet td div',
                            'rule': '''
                            line-height: 30px;
                            max-height: 40px; min-height: 40px; height: 40px;
                            display: block;
                            overflow-y: auto;
                            '''
                        }],
                        filter_action="native", sort_action="native",
                        sort_mode="multi",
                        column_selectable=False,
                        row_selectable="single",
                        row_deletable=False,
                        selected_rows=[],
                        page_action="native",
                        page_current=0,
                        page_size=10,
                        fill_width=False,
                        style_table={'overflowX': 'auto'},
                    ),
                    dbc.Button('Reprice', id='reprice-button', n_clicks=0),
                    reprice_modal,
                    demo_modal,
                    explain_modal,
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
        Output("explain_modal", "is_open"),
    ],
    [
        Input("reprice-button", "n_clicks"),
        Input("open_demo_button", "n_clicks"),
        Input("explain_button", "n_clicks"),
        Input("explain_back_button", "n_clicks"),
    ],
    [
        State("reprice_modal", "is_open"),
        State("datatable", "selected_rows"),
        State("explain_modal", "is_open"),
    ],
    prevent_initial_call=True
)
def toggle_reprice_modal(n0, n1, n2, n3, is_open_modal, selected_rows, explain_is_open):
    button_clicked = ctx.triggered_id
    if len(selected_rows) > 0:
        if button_clicked == "reprice-button" or button_clicked == "open_demo_button":
            return (not is_open_modal), False, False
        elif button_clicked == "explain_button":
            return (not is_open_modal), False, (not explain_is_open)
        else:
            return (not is_open_modal), False, (not explain_is_open)
    elif n0 != 0:
        return dash.no_update, True, False
    else:
        return False, False, False


@callback(
    [
        Output("reprice_body", "children"),
        Output("explain_body", "children"),
    ],
    [
        Input("reprice-button", "n_clicks"),
        Input("explain_button", "n_clicks"),
    ],
    State("datatable", "selected_rows"),
    prevent_initial_call=True
)
def reprice_func(n_click1, n2, selected_rows):
    button_clicked = ctx.triggered_id
    global reprice
    if len(selected_rows) > 0:
        price_increaser = []
        price_decreaser = []
        row_index = selected_rows[0]
        parse_price = df.loc[row_index]['Price'].split('$')
        parse_price_int = parse_price[1].split('.')
        cols = ['Overall_Rating', 'Total-Reviews', 'Availability', 'Color', 'Brand',
                'Total-Sellers', 'Wireless Charging Compatible', 'Magnetic',
                'Faux Leather']

        df_temp = df.drop('Price', axis=1).loc[row_index:row_index + 1]
        df_temp['Total-Sellers'] = df.loc[row_index]['Total-Sellers']

        if 'Wireless Charging Compatible' in df_temp['Special-Feature']:
            df_temp['Wireless Charging Compatible'] = 1
            price_increaser.append('Wireless Charging Compatible')
        else:
            price_decreaser.append('Wireless Charging Compatible')
            df_temp['Wireless Charging Compatible'] = 0

        if 'Magnetic' in df_temp['Special-Feature']:
            price_increaser.append('Magnetic')
            df_temp['Magnetic'] = 1
        else:
            price_decreaser.append('Magnetic')
            df_temp['Magnetic'] = 1

        if 'Faux Letter' in df_temp['Material']:
            price_decreaser.append('Faux Letter')
            df_temp['Faux Leather'] = 1
        else:
            price_decreaser.append('Faux Letter')
            df_temp['Faux Leather'] = 0

        df_temp['Overall_Rating'] = df_temp['Overall-Rating']

        parse_rating = df.loc[row_index]['Overall-Rating'].split(' ')
        parse_rating_int = parse_rating[0]

        if float(parse_rating_int) > 3.5:
            price_increaser.append('High rating')
        else:
            price_decreaser.append('Low rating')

        df_temp['Overall_Rating'] = parse_rating_int

        parse_reviews = df.loc[row_index]['Total-Reviews'].split(' ')
        parse_reviews_temp = parse_reviews[0]
        parse_reviews_split = parse_reviews_temp.split(".")

        if len(parse_reviews_split) == 2:
            parse_reviews_int = str((int(parse_reviews_split[0]) * 1000) + int(parse_reviews_split[1]))
        else:
            parse_reviews_int = parse_reviews_split[0]

        if int(parse_reviews_int) >= 500:
            price_increaser.append('High review count')
        else:
            price_decreaser.append('Low review count')

        df_temp['Total-Reviews'] = parse_reviews_int

        for col in df_temp.columns:
            if col not in cols:
                df_temp = df_temp.drop(col, axis=1)
        reprice_res = get_price_from_model(df_temp)
        reprice = reprice_res[0]
        percentage_change = ((reprice - int(parse_price_int[0])) / int(parse_price_int[0])) * 100

        is_changed = 0

        parse_price_float = int(parse_price_int[0]) / int(parse_price_int[0]) * 100

        if float(reprice) > parse_price_float:
            is_changed = 1
        else:
            is_changed = -1

        if button_clicked == "reprice-button":
            reprice_layout = dbc.Card(
                dbc.CardBody(
                    dbc.Row(
                        [
                            dbc.Col(

                                dcc.Graph(
                                    figure={
                                        'data': [
                                            {'x': ['Current Price', 'Optimized Price'],
                                             'y': [float(parse_price[1]), round(reprice, ndigits=2)],
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
                                                    html.H5(round(float(parse_price[1]), ndigits=2)),
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
                                                    html.H5(round(reprice, ndigits=2)),
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
                                                    html.H5("%" + str(round(percentage_change, ndigits=2))),
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
            return reprice_layout, dash.no_update
        else:
            explain_layout = dbc.Card(
                dbc.CardBody(
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        html.Div(
                                            html.P(
                                                "Our machine learning algorithm examines all other similar products and "
                                                "analyses the main trends among these listings from other sellers. The main "
                                                "features which our model takes into account are brand, color, build material "
                                                "and other special features like wireless charging ability for a phone case. "
                                                "Another important point is the competition in the market for that specific "
                                                "product. Our algorithm also considers the total number of sellers while "
                                                "calculating the optimized price for that product. ",
                                                className='text-center',
                                                style={
                                                    'font-size': '18px',
                                                    'textAlign': 'justify',
                                                }
                                            ),
                                        )
                                    )
                                )
                            ),
                            dbc.Col(
                                [
                                    dbc.Row(
                                        dbc.Card(
                                            [
                                                dbc.CardHeader("Price Increasing Factor"),
                                                dbc.CardBody(
                                                    html.H5(round(float(parse_price[1]), ndigits=2)),
                                                ),
                                            ]
                                        ),
                                    ),
                                    html.Br(),
                                    dbc.Row(
                                        dbc.Card(
                                            [
                                                dbc.CardHeader("Price Decreasing Factor"),
                                                dbc.CardBody(
                                                    html.H5(round(reprice, ndigits=2)),
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
            return dash.no_update, explain_layout


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
    demo_graph_layout = dbc.Card()
    if button_clicked == "profit_project_button":
        demo_graph_layout = dbc.Card(
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2], 'y': [45, 35], 'type': 'bar', 'name': 'SF'},
                    ],
                    'layout': {
                        'title': 'Project For Profit'
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
                        'title': 'Project For Sales'
                    }
                }
            ),
        )
    return demo_graph_layout


@callback(
    [Output("success", "is_open"),
     Output("datatable", "data"),
     ],
    Input("accept_button", "n_clicks"),
    [
        State("datatable", "selected_rows"),
        State("success", "is_open"),
    ],
    prevent_initial_call=True
)
def update_table(n_click, selected_rows, is_open):
    global df
    if n_click:
        row_index = selected_rows[0]
        df.loc[row_index, 'Price'] = "$" + str(round(reprice, ndigits=2))
        df.to_csv("data/inventory_data.csv", index=False)
        df = pd.read_csv('data/inventory_data.csv')
        return not is_open, df.to_dict('records')
    return is_open, df.to_dict('records')
