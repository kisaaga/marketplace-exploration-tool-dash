from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from pages import dashboard, sales, inventory, stats, settings

app = Dash(external_stylesheets=[dbc.themes.FLATLY], suppress_callback_exceptions=True)

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "12rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "12rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H1("Dash", className="display-5"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Dashboard", href="/dashboard", active="exact"),
                dbc.NavLink("Sales", href="/sales", active="exact"),
                dbc.NavLink("Inventory", href="/inventory", active="exact"),
                dbc.NavLink("Stats", href="/stats", active="exact"),
                dbc.NavLink("Settings", href="/settings", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@callback(Output('page-content', 'children'),
          Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return dashboard.layout
    elif pathname == '/dashboard':
        return dashboard.layout
    elif pathname == '/sales':
        return sales.layout
    elif pathname == '/inventory':
        return inventory.layout
    elif pathname == '/stats':
        return stats.layout
    elif pathname == '/settings':
        return settings.layout
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)
