# Dash imports
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_table

# Other library imports
import pandas as pd
from django_plotly_dash import DjangoDash
import plotly.graph_objects as go

from dpd_cc_example.data.models import Team, PlayerResults

# Define Django Dash App
app = DjangoDash("report_app", external_stylesheets=[dbc.themes.BOOTSTRAP])

DROP_COLS = ["name", "team_id", "gw", "fixture", "round"]

########################################################################################################################
##############################################    Styles      ##########################################################
########################################################################################################################

# Dict to hold all inline styling for dash components. Any style edits should be made here.
styles = {
    "control_section": {
        "margin-top": "0"
    },
    "cardheader" : {
        "background-color": "#f7f7f7",
        "border-color": "#f7f7f7",
        "border-radius": "2rem 2rem 0rem 0rem",
        "color": "black"
    }
}

########################################################################################################################
##############################################    Data Queries      ####################################################
########################################################################################################################

def query_all_teams(gw=None):
    if gw:
        return Team.objects.filter(gw=gw)
    else:
        return Team.objects.all()

def query_team_players(team_id):
    return PlayerResults.objects.filter(team_id=team_id)

def query_player_gws(player_element):
    return PlayerResults.objects.filter(element=player_element).order_by('gw').values_list('gw', flat=True).distinct('gw')

def query_player_data(player_element):
    fields = [f.attname for f in PlayerResults._meta.fields]
    queryset = PlayerResults.objects.filter(element=player_element).values_list(*fields)
    return pd.DataFrame(list(queryset), columns=fields)

########################################################################################################################
##############################################    Dash helper functions      ###########################################
########################################################################################################################

def create_section_header(title, button_id):
    """ Create a custom card header for sections"""
    return dbc.CardHeader(
        dbc.Button(
            html.H2(title, className="text-black"),
            id=button_id,
            block=True,
            className="shadow-none",
            style=styles["cardheader"]
        ),
        className="text-center",
        style=styles["cardheader"]
    )

def empty_styled_table(export_format=None):
    return dash_table.DataTable(
        style_table={'overflowX': 'scroll', 'overflowY': 'auto', 'color': 'black'},
        style_header={'fontWeight': 'bold', 'backgroundColor': 'white', 'fontSize': 14},
        style_cell={
            'minWidth': '2vw', 'width': '4vw', 'maxWidth': '10vw',
            'whiteSpace': 'normal', 'textAlign': 'left',
            'font-family': 'sans-serif',
            'fontSize': 12
        },
        export_format=export_format
    )

def overview_table(data):
    table = empty_styled_table()
    table.data = data
    table.columns = [{"name": i, "id": i} for i in list(data[0].keys())]
    table.id = "data-table"
    return table


def create_multiline(df):
    """
    Wrapper for basic plotly multiline chart fig
    :param pd_dataframe:
    :return: fig object
    """
    fig = go.Figure()
    for column in df.columns:
        sub_df = df.copy().dropna(subset=[column])
        fig.add_trace(go.Scatter(x=sub_df.index, y=sub_df[column], mode='lines+markers', name=column))

    fig.update_layout(
        yaxis_title="Score",
        template='simple_white',
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.22,
            xanchor="left",
            x=0
        ),
        font=dict(size=12),
        margin=dict(t=0),
    )
    return fig

########################################################################################################################
##############################################    Layout      ##########################################################
########################################################################################################################

# Layout for user inputs
control_section = dbc.Row(
    [
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label("Select Team", html_for="team-dropdown"),
                    dcc.Dropdown(
                        id="team-dropdown",
                        placeholder="Team List",
                        options=[
                        ],
                    ),
                ]
            ),
            width=4
        ),
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label("Select Player", html_for="player-dropdown"),
                    dcc.Dropdown(
                        id="player-dropdown",
                        placeholder="Player List",
                        options=[
                        ],
                    ),
                ]
            ),
            width=4
        ),
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label("Select Gameweek", html_for="gw-dropdown"),
                    dcc.Dropdown(
                        id="gw-dropdown",
                        placeholder="Gameweek List",
                        options=[
                        ],
                    ),
                ]
            ),
            width=4
        ),
    ],
    form=True,
    justify="center",
    style=styles["control_section"]
)


# Layout for the data section
data_section = html.Div([
    dbc.Row(
        html.H2("Overview Table"),
        className="text-center text-uppercase text-black mb-4",
        justify="center"
    ),
    dbc.Row(
        dbc.Col(
            html.Div(
                id="table1-div",
            ),
            width=8
        ),
        justify="center",
        className="text-center mt-3"
    ),
    dbc.Row(
        dbc.Col([
            dbc.FormGroup(
                [
                    dbc.Label("Select time period to average:", html_for="player-groupby-input"),
                    dbc.RadioItems(
                        options=[
                            {"label": "No Averaging", "value": None},
                            {"label": "3 Months", "value": "3M"},
                            {"label": "1 Year", "value": "1Y"},

                        ],
                        value=None,
                        id="player-groupby-input",
                        inline=True,

                    ),
                ],
            ),
        ]),
        justify="center",
        className="text-center mt-3"
    ),
    dbc.Row(
        dbc.Col(
            [
                dcc.Dropdown(
                    options=[
                    ],
                    value=[],
                    placeholder="select metric",
                    multi=True,
                    id="metric-dropdown",
                )
            ]
        )
    ),
    dbc.Row(
        dbc.Col(
            [
                dcc.Store(id='player-overview-memory'),
                html.Div(id="player-overview-div"),
            ],
            width={"size": 10, "offset": 1}),
        justify="center",
        className="mt-3"
    ),
])

app.layout = dbc.Container(
    [
        dbc.Card(
            dbc.CardBody(control_section),
            className="w-100 mb-3",
        ),
        create_section_header("Player Data Section", button_id="collapse-1-toggle"),
        dbc.Card(
            dbc.Collapse(
                dbc.CardBody(data_section),
                id="collapse-1",
                is_open=False,
            ),
            className="w-100 mb-5",
        ),
    ],
    fluid=True,
    style=dict(overflow=True)
)


########################################################################################################################
##############################################    Callbacks   ##########################################################
########################################################################################################################

@app.expanded_callback(
    [Output('team-dropdown', 'options'),
     Output('team-dropdown', 'value')],
    [Input('team-dropdown', 'placeholder')],
)
def populate_team_dropdown(*args, **kwargs):
    favourite_team = kwargs['user'].favourite_team
    all_teams = query_all_teams()
    if all_teams:
        return [{'label': team.name, 'value': team.id} for team in all_teams], favourite_team
    else:
        raise PreventUpdate

@app.expanded_callback(
    Output('player-dropdown', 'options'),
    [Input('team-dropdown', 'value')],
)
def populate_player_dropdown(*args, **kwargs):
    if not args[0]:
        raise PreventUpdate
    team_id = args[0]
    players = query_team_players(team_id)
    if players:
        return [{'label': player.name, 'value': player.element} for player in players]
    else:
        raise PreventUpdate

@app.expanded_callback(
    Output('gw-dropdown', 'options'),
    [Input('player-dropdown', 'value')],
)
def populate_gw_dropdown(*args, **kwargs):
    if not args[0]:
        raise PreventUpdate
    player_element = args[0]
    gws = query_player_gws(player_element)
    if gws:
        return [{'label': gw, 'value':gw} for gw in gws]
    else:
        raise PreventUpdate


@app.expanded_callback(
    Output('table1-div', 'children'),
    [Input('player-dropdown', 'value')],
)
def populate_overview_table(*args, **kwargs):
    if not args[0]:
        raise PreventUpdate
    player_element = args[0]
    data_df = query_player_data(player_element)
    data_df = data_df.drop(columns=["id", "team_id"]).sort_values(by="gw")
    data_records = data_df.to_dict('records')
    if data_records:
        return overview_table(data_records)
    else:
        raise PreventUpdate


@app.callback(
    [Output("player-overview-memory", "data"),
     Output("metric-dropdown", "options")],
    [Input("player-dropdown", "value")],
)
def load_multiline_data(player_element):
    """ Callback to load composite overview data to memory.
     Storing here prevents a query everytime data is aggregated"""
    if player_element is None:
        raise PreventUpdate

    def aggregate(df, freq):
        df.index = pd.to_datetime(df.index)
        df = df.groupby(pd.Grouper(freq=freq)).mean()
        df.index = df.index.date.astype(str)
        return df

    df = query_player_data(player_element)
    df = df.drop(columns=["id", "element"]).set_index("kickoff_time")
    # Compute aggregations upfront
    df_dict = {
        "None": df.to_json(),
        "1M": aggregate(df, "1M").to_json(),
        "3M": aggregate(df, "3M").to_json(),
    }
    metric_dropdown_options = [ {'label': x, 'value': x} for x in df.columns if x not in DROP_COLS]

    return df_dict, metric_dropdown_options


@app.callback(
    Output("player-overview-div", "children"),
    [Input("player-overview-memory", 'modified_timestamp'),
     Input("player-groupby-input", "value"),
     Input("metric-dropdown", "value")],
    [State("player-overview-memory", 'data')]
)
def update_multiline_plot(_trigger, groupby_selection, metric, df_dict):
    if df_dict:
        if groupby_selection is not None:
            df = pd.read_json(df_dict[groupby_selection])
        else:
            df = pd.read_json(df_dict["None"])
        df = df.drop(DROP_COLS, axis=1, errors='ignore').sort_index()
        multiline_fig = create_multiline(df[metric])
        return dcc.Graph(id='fig1', figure=multiline_fig)
    else:
        raise PreventUpdate

@app.callback(
    [Output(f"collapse-{i}", "is_open") for i in range(1, 2)],
    [Input(f"collapse-{i}-toggle", "n_clicks") for i in range(1, 2)],
    [State(f"collapse-{i}", "is_open") for i in range(1, 2)],
)
def toggle_accordion(*args, **kwargs):
    """ Callback for all section collapse.
    To add another section simply name it collapse-{n} and its button collapse-{n}-toggle
    range(1,n) in the callback inputs must be updated to match
    """
    ctx = kwargs["callback_context"]
    if ctx.triggered:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        collapse_num = button_id.split("-")[1]
        ctx.states[f"collapse-{collapse_num}.is_open"] = not ctx.states[f"collapse-{collapse_num}.is_open"]
        if ctx.inputs[f"{button_id}.n_clicks"]:
            return tuple(ctx.states.values())
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
