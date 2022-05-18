from dash import dcc, html, dash_table, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

df = px.data.iris()

fig = px.scatter(df, x="sepal_width", y="sepal_length")

df = pd.DataFrame(
    {
        "Revenue": ["Amazon Sales", "Refund", "Reimbursements", "Promo Rebates"],
        "$236,500.200": ["$180,250.100", "$30,357.250", "$20,500.50", "$10,300.47"],
    }
)

FutureUnit = 2457
FutureMargin = "-13%"
FutureRoi = "-10%"

PastUnit = 1967
PastMargin = "-16%"
PastRoi = "-13%"

SearchBar = html.Div(
    [
        dbc.Input(id="input", placeholder="Search", type="text"),
        html.Br(),
        html.P(id="output"),
    ]
)

ListGroup = dbc.ListGroup(
    [
        dbc.ListGroupItem("Item 1", color="secondary"),
        dbc.ListGroupItem("Item 2"),
        dbc.ListGroupItem("Item 3", color="secondary"),
    ],
    flush=True,
),

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
                    dbc.CardHeader(html.H5("Units Sold"), ),
                    dbc.CardBody(
                        [
                            dbc.Row(
                                dbc.RadioItems(
                                    options=[
                                        {"label": "Today", "value": 1},
                                        {"label": "This Month", "value": 2},
                                    ],
                                    value=1,
                                    id="radioitems-inline-input",
                                    inline=True,
                                ),
                            ),
                            html.Hr(),
                            dbc.Row(
                                dbc.Col(
                                    html.H3(
                                        [
                                            PastUnit,
                                        ],
                                        className="card-text",
                                    ),
                                ),
                            ),
                            html.Br(),
                            dbc.Row(
                                ListGroup,
                            ),
                        ],
                    ),
                ],
            ),
        ),
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader(html.H5("Net Margin"), ),
                    dbc.CardBody(
                        [
                            dbc.Row(
                                dbc.RadioItems(
                                    options=[
                                        {"label": "Today", "value": 1},
                                        {"label": "This Month", "value": 2},
                                    ],
                                    value=1,
                                    id="radioitems-inline-input",
                                    inline=True,
                                ),
                            ),
                            html.Hr(),
                            dbc.Row(
                                dbc.Col(
                                    html.H3(
                                        [
                                            PastMargin,
                                        ],
                                        className="card-text",
                                    ),
                                ),
                            ),
                            html.Br(),
                            dbc.Row(
                                ListGroup,
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
                                    id="radioitems-inline-input",
                                    inline=True,
                                ),
                            ),
                            html.Hr(),
                            dbc.Row(
                                dbc.Col(
                                    html.H3(
                                        [
                                            PastRoi,
                                        ],
                                        className="card-text",
                                    ),
                                ),
                            ),
                            html.Br(),
                            dbc.Row(
                                ListGroup,
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
                                ListGroup,
                            ),
                        ],
                    ),
                ],
            ),
        ),
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader(html.H5("Net Margin"), ),
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
                                            FutureMargin,
                                        ],
                                        className="card-text",
                                    ),
                                ),
                            ),
                            html.Br(),
                            dbc.Row(
                                ListGroup,
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
                                ListGroup,
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
                                    dcc.Graph(
                                        figure={
                                            'data': [
                                                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                                                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                                            ],
                                            'layout': {
                                                'title': 'Dash Data Visualization'
                                            }
                                        }
                                    )
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
                                    dcc.Graph(
                                        figure=dict(
                                            data=[
                                                dict(
                                                    x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                                                       2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                                                    y=[219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
                                                       350, 430, 474, 526, 488, 537, 500, 439],
                                                    name='Rest of world',
                                                    marker=dict(
                                                        color='rgb(55, 83, 109)'
                                                    )
                                                ),
                                                dict(
                                                    x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                                                       2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                                                    y=[16, 13, 10, 11, 28, 37, 43, 55, 56, 88, 105, 156, 270,
                                                       299, 340, 403, 549, 499],
                                                    name='China',
                                                    marker=dict(
                                                        color='rgb(26, 118, 255)'
                                                    )
                                                )
                                            ],
                                            layout=dict(
                                                title='US Export of Plastic Scrap',
                                                showlegend=True,
                                                legend=dict(
                                                    x=0,
                                                    y=1.0
                                                ),
                                            )
                                        ),
                                    )
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
                                    dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
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
                                    dcc.Graph(
                                        figure=dict(
                                            data=[
                                                dict(
                                                    x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                                                       2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                                                    y=[219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
                                                       350, 430, 474, 526, 488, 537, 500, 439],
                                                    name='Rest of world',
                                                    marker=dict(
                                                        color='rgb(55, 83, 109)'
                                                    )
                                                ),
                                                dict(
                                                    x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                                                       2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                                                    y=[16, 13, 10, 11, 28, 37, 43, 55, 56, 88, 105, 156, 270,
                                                       299, 340, 403, 549, 499],
                                                    name='China',
                                                    marker=dict(
                                                        color='rgb(26, 118, 255)'
                                                    )
                                                )
                                            ],
                                            layout=dict(
                                                title='US Export of Plastic Scrap',
                                                showlegend=True,
                                                legend=dict(
                                                    x=0,
                                                    y=1.0
                                                ),
                                            )
                                        ),
                                    )
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
