from dash import dcc, html, dash_table, Input, Output, callback, State
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

df = pd.read_csv('data/sales_data.csv')
df.dropna(how='all', inplace=True)

tot_profit = 0

for i in df['Profit']:
    tot_profit = tot_profit + i

units_sold = 0

for m in df['Amount']:
    units_sold = units_sold + m

tot_cost = 0

for j in df['Cost']:
    tot_cost = tot_cost + j

tot_revenue = 0

for i in range(len(df['Price($)'])):
    if df['State'][i] == 'Sold-out':
        tot_revenue = tot_revenue + df['Price($)'][i]

tot_revenue = int(tot_revenue)

current_roi = tot_profit / tot_cost

FutureUnit = 2457
FutureProfit = "-13%"
FutureRoi = "-10%"

PastUnit = str(int(units_sold)) + " Units"
PastProfit = str(int(tot_profit)) + "$"
PastRoi = str(int(current_roi * 100)) + "%"

SearchBar = html.Div(
    [
        dbc.Input(id="input", placeholder="Search", type="text"),
        html.Br(),
        html.P(id="output"),
    ]
)

VerticalNav = dbc.Nav(
    [
        dbc.NavItem(
            SearchBar,
        ),
        dbc.DropdownMenu(
            [dbc.DropdownMenuItem("Update account informations"), dbc.DropdownMenuItem("Sign out")],
            label="Account",
            nav=True,
        ),
    ]
)
CurrentContent = dbc.Row(
    [
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader(html.H5("Units Sold")),
                    dbc.CardBody(
                        [
                            dbc.Row(
                                dbc.RadioItems(
                                    options=[
                                        {"label": "Today", "value": 1},
                                        {"label": "This Month", "value": 2},
                                    ],
                                    value=1,
                                    id="radioitems-units-input",
                                    inline=True,
                                ),
                            ),
                            html.Hr(),
                            dbc.Row(
                                dbc.Col(
                                    html.H3(
                                        children=[
                                            PastUnit,
                                        ],
                                        className="card-text",
                                        id="unit_sold_text"
                                    ),
                                ),
                            ),
                        ],
                    ),
                ],
            ),
        ),
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader(html.H5("Net Profit"), ),
                    dbc.CardBody(
                        [
                            dbc.Row(
                                dbc.RadioItems(
                                    options=[
                                        {"label": "Today", "value": 1},
                                        {"label": "This Month", "value": 2},
                                    ],
                                    value=1,
                                    id="radioitems-profit-input",
                                    inline=True,
                                ),
                            ),
                            html.Hr(),
                            dbc.Row(
                                dbc.Col(
                                    html.H3(
                                        children=[
                                            PastProfit,
                                        ],
                                        className="card-text",
                                        id="profit-text"
                                    ),
                                ),
                            ),
                        ],
                    ),
                ],
            ),
        ),
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader(html.H5("ROI"), ),
                    dbc.CardBody(
                        [
                            dbc.Row(
                                dbc.RadioItems(
                                    options=[
                                        {"label": "Today", "value": 1},
                                        {"label": "This Month", "value": 2},
                                    ],
                                    value=1,
                                    id="radioitems-roi-input",
                                    inline=True,
                                ),
                            ),
                            html.Hr(),
                            dbc.Row(
                                dbc.Col(
                                    html.H3(
                                        children=[
                                            PastRoi,
                                        ],
                                        className="card-text",
                                        id="roi-text"
                                    ),
                                ),
                            ),
                        ],
                    ),
                ],
            ),
        ),
    ]
),

FutureContent = dbc.Row(
    [
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader(html.H5("Units Sold"), ),
                    dbc.CardBody(
                        [
                            dbc.Row(
                                dbc.Col(
                                    [
                                        html.H6("Number of months"),
                                        dcc.Slider(0, 12, 1, value=5, marks=None,
                                                   tooltip={"placement": "bottom", "always_visible": True}),
                                    ],
                                ),
                            ),
                            html.Hr(),
                            dbc.Row(
                                dbc.Col(
                                    html.H3(
                                        [
                                            FutureUnit,
                                        ],
                                        className="card-text",
                                    ),
                                ),
                            ),
                            html.Br(),
                            dbc.Row(
                                dbc.ListGroup(
                                    [
                                        dbc.ListGroupItem(
                                            "Item 1",
                                            color="secondary",
                                        ),
                                    ],
                                    flush=True,
                                ),
                            ),
                        ],
                    ),
                ],
            ),
        ),
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader(html.H5("Net Profit"), ),
                    dbc.CardBody(
                        [
                            dbc.Row(
                                dbc.Col(
                                    [
                                        html.H6("Number of months"),
                                        dcc.Slider(0, 12, 1, value=5, marks=None,
                                                   tooltip={"placement": "bottom", "always_visible": True}),
                                    ],
                                ),
                            ),
                            html.Hr(),
                            dbc.Row(
                                dbc.Col(
                                    html.H3(
                                        [
                                            FutureProfit,
                                        ],
                                        className="card-text",
                                    ),
                                ),
                            ),
                            html.Br(),
                            dbc.Row(
                                dbc.ListGroup(
                                    [
                                        dbc.ListGroupItem(
                                            "Item 1",
                                            color="secondary",
                                        ),
                                    ],
                                    flush=True,
                                ),
                            ),
                        ],
                    ),
                ],
            ),
        ),
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader(html.H5("ROI"), ),
                    dbc.CardBody(
                        [
                            dbc.Row(
                                dbc.Col(
                                    [
                                        html.H6("Number of months"),
                                        dcc.Slider(0, 12, 1, value=5, marks=None,
                                                   tooltip={"placement": "bottom", "always_visible": True}),
                                    ],
                                ),
                            ),
                            html.Hr(),
                            dbc.Row(
                                dbc.Col(
                                    html.H3(
                                        [
                                            FutureRoi,
                                        ],
                                        className="card-text",
                                    ),
                                ),
                            ),
                            html.Br(),
                            dbc.Row(
                                dbc.ListGroup(
                                    [
                                        dbc.ListGroupItem(
                                            "Item 1",
                                            color="secondary",
                                        ),
                                    ],
                                    flush=True,
                                ),
                            ),
                        ],
                    ),
                ],
            ),
        ),
    ]
),

tab1_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Container(
                            [
                                dbc.Row(
                                    html.H4("Summary"),
                                ),
                                dbc.Row(
                                ),
                            ]
                        ),
                    ),

                    dbc.Col(
                        dbc.Container(
                            [
                                dbc.Row(
                                    html.H4("Cost Over Time"),
                                ),
                                dbc.Row(
                                ),
                            ]
                        ),
                    ),
                ],
                justify="between",
                align="start",
            ),
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Container(
                            [
                                dbc.Row(
                                    html.H4("Summary"),
                                ),
                                dbc.Row(
                                ),
                            ]
                        ),
                    ),

                    dbc.Col(
                        dbc.Container(
                            [
                                dbc.Row(
                                    html.H4("Revenue Over Time"),
                                ),
                                dbc.Row(
                                ),
                            ]
                        ),
                    ),
                ],
                justify="between",
            ),
        ]
    ),
    className="mt-3",
)

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.H1('Dashboard'),
                ),
                dbc.Col(
                    VerticalNav,
                    width={"size": 4, "order": 1, "offset": 2},

                ),
            ],
            justify="between",
            align="start",
        ),
        dbc.Tabs(
            [
                dbc.Tab(CurrentContent, label="Past/Current"),
                dbc.Tab(FutureContent, label="Future"),
            ],
        ),
        html.Div(id="content"),
        html.Br(),
        dbc.Row(
            dbc.Tabs(
                [
                    dbc.Tab(tab1_content, label="Cost"),
                    dbc.Tab(tab2_content, label="Revenue"),
                ],
            ),
        ),
    ],
    className="pad-row",
)


@callback(
    Output("unit_sold_text", "children"),
    Input("radioitems-units-input", "value"),
    prevent_initial_call=True
)
def units_sold_radio(n1):
    if n1 == 2:
        df['Date '] = pd.to_datetime(df['Date '], dayfirst=True)
        dfm2 = df.groupby(pd.Grouper(key='Date ', freq='M')).sum()
        amount = dfm2.iloc[-1]["Amount"]
        print(amount)
        return str(int(amount)) + " Units"
    else:
        print(PastUnit)
        return PastUnit


@callback(
    Output("profit-text", "children"),
    Input("radioitems-profit-input", "value"),
    prevent_initial_call=True
)
def profit_radio(n1):
    if n1 == 2:
        df['Date '] = pd.to_datetime(df['Date '], dayfirst=True)
        dfm2 = df.groupby(pd.Grouper(key='Date ', freq='M')).sum()
        profit = dfm2.iloc[-1]["Profit"]
        return str(profit) + " $"
    else:
        return PastProfit


@callback(
    Output("roi-text", "children"),
    Input("radioitems-roi-input", "value"),
    prevent_initial_call=True
)
def profit_radio(n1):
    if n1 == 2:
        df['Date '] = pd.to_datetime(df['Date '], dayfirst=True)
        dfm2 = df.groupby(pd.Grouper(key='Date ', freq='M')).sum()
        profit = dfm2.iloc[-1]["Profit"]
        cost = dfm2.iloc[-1]["Cost"]
        calc_roi = profit / cost
        return str(int(calc_roi * 100)) + "%"
    else:
        return PastRoi
