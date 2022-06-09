from dash import dcc, html, Input, Output, callback
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import pandas as pd

from pages.utils import get_sales_from_model

df = pd.read_csv('data/sales_data.csv')
df.dropna(how='all', inplace=True)
df = df.drop(columns=['Lookup_Id', 'Lookup_Price', 'Lookup_Name'])

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
FutureProfit = 257
FutureRoi = "-10%"

PastUnit = str(int(units_sold)) + " Units"
PastProfit = str(int(tot_profit)) + "$"
PastRoi = str(int(current_roi * 100)) + "%"

ProfitMonth = 0
UnitMonth = 0
RoiMonth = 0

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
                                        {"label": "All Time", "value": 1},
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
                                        {"label": "All Time", "value": 1},
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
                                        {"label": "All Time", "value": 1},
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
                    dbc.CardHeader(html.H5("Units To Be Sold"), ),
                    dbc.CardBody(
                        [
                            dbc.Row(
                                dbc.Col(
                                    [
                                        html.H6("Number of months"),
                                        dcc.Slider(1, 12, 1, value=1, marks=None,
                                                   id="futureUnitSlider",
                                                   tooltip={"placement": "bottom", "always_visible": True}),
                                    ],
                                ),
                            ),
                            html.Hr(),
                            dbc.Row(
                                dbc.Col(
                                    html.H3(
                                        [
                                        ],
                                        id="futureUnit",
                                        className="card-text",
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
                    dbc.CardHeader(html.H5("Net Projected Profit"), ),
                    dbc.CardBody(
                        [
                            dbc.Row(
                                dbc.Col(
                                    [
                                        html.H6("Number of months"),
                                        dcc.Slider(1, 12, 1, value=1, marks=None,
                                                   id="futureProfitSlider",
                                                   tooltip={"placement": "bottom", "always_visible": True}),
                                    ],
                                ),
                            ),
                            html.Hr(),
                            dbc.Row(
                                html.H3(
                                    [
                                    ],
                                    id="futureProfit",
                                    className="card-text",
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
                    html.Div(
                        id="cost_Summary",
                        children=[],
                        style={
                            "width": 575
                        }
                    ),
                    html.Div(
                        id="cost_Time", children=[],
                        style={
                            "width": 575
                        }
                    ),
                ]
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
                    html.Div(
                        id="revenue_Summary",
                        children=[],
                        style={
                            "width": 575
                        }
                    ),
                    html.Div(
                        id="revenue_Time", children=[],
                        style={
                            "width": 575
                        }
                    ),
                ]
            ),
            # justify="between",
        ]
    ),
    className="mt-3",
)

tab3_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row(
                [
                    html.Div(
                        id="profit_Summary",
                        children=[],
                        style={
                            "width": 575
                        }
                    ),
                    html.Div(
                        id="profit_Time", children=[],
                        style={
                            "width": 575
                        }
                    ),
                ]
            ),
            # justify="between",
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
                    dbc.Tab(tab1_content, label="Cost", tab_id="1"),
                    dbc.Tab(tab2_content, label="Revenue", tab_id="2"),
                    dbc.Tab(tab3_content, label="Profit", tab_id="3"),
                ],
                id="general_tab"
            ),
        ),
    ],
    className="pad-row",
)


@callback(
    Output("unit_sold_text", "children"),
    Input("radioitems-units-input", "value"),
)
def units_sold_radio(n1):
    global UnitMonth
    df['Date '] = pd.to_datetime(df['Date '], dayfirst=True)
    dfm2 = df.groupby(pd.Grouper(key='Date ', freq='M')).sum()
    amount = dfm2.iloc[-1]["Amount"]
    UnitMonth = int(amount)
    if n1 == 2:
        return str(int(amount)) + " Units"
    else:
        return PastUnit


@callback(
    Output("profit-text", "children"),
    Input("radioitems-profit-input", "value"),
)
def profit_radio(n1):
    global ProfitMonth
    df['Date '] = pd.to_datetime(df['Date '], dayfirst=True)
    dfm2 = df.groupby(pd.Grouper(key='Date ', freq='M')).sum()
    profit = dfm2.iloc[-1]["Profit"]
    ProfitMonth = profit
    if n1 == 2:
        return str(profit) + " $"
    else:
        return PastProfit


@callback(
    Output("roi-text", "children"),
    Input("radioitems-roi-input", "value"),
)
def roi_radio(n1):
    global RoiMonth
    df['Date '] = pd.to_datetime(df['Date '], dayfirst=True)
    dfm2 = df.groupby(pd.Grouper(key='Date ', freq='M')).sum()
    profit = dfm2.iloc[-1]["Profit"]
    cost = dfm2.iloc[-1]["Cost"]
    calc_roi = profit / cost
    RoiMonth = int(calc_roi * 100)
    if n1 == 2:
        return str(int(calc_roi * 100)) + "%"
    else:
        return PastRoi


@callback(
    Output("futureUnit", "children"),
    Input("futureUnitSlider", "value"),
)
def future_unit_slider(n):
    sale_num, day_list = get_sales_from_model(df, n, 'Month')
    return str(int(sale_num)) + " Units"


@callback(
    Output("futureProfit", "children"),
    Input("futureProfitSlider", "value"),
)
def future_profit_slider(n):
    sale_num, day_list = get_sales_from_model(df, n, 'Month')
    profit_num = (sale_num * ProfitMonth) / UnitMonth
    return str(int(profit_num)) + " $"


@callback(
    [Output("revenue_Summary", "children"),
     Output("revenue_Time", "children"),
     ],
    Input("general_tab", "tab_id"),
    prevent_initial_call=False
)
def revenue(tab_id):
    total = 0
    total_cummilative = 0
    average_revenue = 0
    struct = df.shape
    row_num = struct[0]
    revenue_cummilative = []
    date_array = df['Date ']
    revenue_array = df['Price($)']

    for i in range(row_num):
        total_cummilative = total_cummilative + revenue_array[i]
        revenue_cummilative.append(total_cummilative)

    for x in range(row_num):
        price_str = df.loc[x]['Price($)']
        price_float = float(price_str)
        total = total + price_float
    average_revenue = total / row_num
    revenue_layout_1 = dbc.Card(
        [
            dbc.Row(
                dbc.Card(
                    [
                        dbc.CardHeader("Summary"),
                        dbc.CardBody(
                            dbc.ListGroup(
                                [
                                    dbc.ListGroupItem("Total Revenue: " + str(round(total, ndigits=2)) + "$"),
                                    dbc.ListGroupItem(
                                        "Average Revenue: " + str(round(average_revenue, ndigits=2)) + "$"),
                                ]
                            ),
                        ),
                    ]
                ),
            ),
            dbc.Row(
                dbc.Card(
                    [
                        dbc.CardHeader("Revenue For Each Date"),
                        dbc.CardBody(
                            dcc.Graph(figure=go.Figure(data=[go.Scatter(x=date_array, y=revenue_array)])),
                        ),
                    ]
                ),
            ),
        ]
    ),
    revenue_layout_2 = dbc.Card(
        [
            dbc.CardHeader("Revenue Over Time"),
            dbc.CardBody(
                dcc.Graph(figure=go.Figure(data=[go.Scatter(x=date_array, y=revenue_cummilative)])),
            ),
        ]
    ),
    return revenue_layout_1, revenue_layout_2


@callback(
    [Output("cost_Summary", "children"),
     Output("cost_Time", "children"),
     ],
    Input("general_tab", "tab_id"),
    prevent_initial_call=False
)
def cost(tab_id):
    total = 0
    total_cummilative = 0
    average_revenue = 0
    struct = df.shape
    row_num = struct[0]
    cost_cummilative = []
    date_array = df['Date ']
    cost_array = df['Cost']

    for i in range(row_num):
        total_cummilative = total_cummilative + cost_array[i]
        cost_cummilative.append(total_cummilative)

    for x in range(row_num):
        price_str = df.loc[x]['Cost']
        price_float = float(price_str)
        total = total + price_float
    average_revenue = total / row_num
    revenue_layout_1 = dbc.Card(
        [
            dbc.Row(
                dbc.Card(
                    [
                        dbc.CardHeader("Summary"),
                        dbc.CardBody(
                            dbc.ListGroup(
                                [
                                    dbc.ListGroupItem("Total Cost: " + str(round(total, ndigits=2)) + "$"),
                                    dbc.ListGroupItem("Average Cost: " + str(round(average_revenue, ndigits=2)) + "$"),
                                ]
                            ),
                        ),
                    ]
                ),
            ),
            dbc.Row(
                dbc.Card(
                    [
                        dbc.CardHeader("Cost For Each Date"),
                        dbc.CardBody(
                            dcc.Graph(figure=go.Figure(data=[go.Scatter(x=date_array, y=cost_array)])),
                        ),
                    ]
                ),
            ),
        ]
    ),
    revenue_layout_2 = dbc.Card(
        [
            dbc.CardHeader("Cost Over Time"),
            dbc.CardBody(
                dcc.Graph(figure=go.Figure(data=[go.Scatter(x=date_array, y=cost_cummilative)])),
            ),
        ]
    ),
    return revenue_layout_1, revenue_layout_2


@callback(
    [Output("profit_Summary", "children"),
     Output("profit_Time", "children"),
     ],
    Input("general_tab", "tab_id"),
    prevent_initial_call=False
)
def revenue(tab_id):
    total_profit = 0
    total_cummilative = 0
    Profit_day = []
    struct = df.shape
    row_num = struct[0]
    profit_cummilative = []
    date_array = df['Date ']
    cost_array = df['Cost']
    revenue_array = df['Price($)']

    for i in range(row_num):
        Profit_day.append(revenue_array[i] - cost_array[i])
        total_cummilative = total_cummilative + (revenue_array[i] - cost_array[i])
        profit_cummilative.append(total_cummilative)

    for x in range(row_num):
        cost_str = df.loc[x]['Cost']
        revenue_str = df.loc[x]['Price($)']
        cost = float(cost_str)
        revenue = float(revenue_str)
        total_profit = total_profit + (revenue - cost)
    average_profit = total_profit / row_num
    revenue_layout_1 = dbc.Card(
        [
            dbc.Row(
                dbc.Card(
                    [
                        dbc.CardHeader("Summary"),
                        dbc.CardBody(
                            dbc.ListGroup(
                                [
                                    dbc.ListGroupItem("Total Profit: " + str(round(total_profit, ndigits=2)) + "$"),
                                    dbc.ListGroupItem("Average Profit: " + str(round(average_profit, ndigits=2)) + "$"),
                                ]
                            ),
                        ),
                    ]
                ),
            ),
            dbc.Row(
                dbc.Card(
                    [
                        dbc.CardHeader("Profit For Each Date"),
                        dbc.CardBody(
                            dcc.Graph(figure=go.Figure(data=[go.Scatter(x=date_array, y=Profit_day)])),
                        ),
                    ]
                ),
            ),
        ]
    ),
    revenue_layout_2 = dbc.Card(
        [
            dbc.CardHeader("Profit Over Time"),
            dbc.CardBody(
                dcc.Graph(figure=go.Figure(data=[go.Scatter(x=date_array, y=profit_cummilative)])),
            ),
        ]
    ),
    return revenue_layout_1, revenue_layout_2
