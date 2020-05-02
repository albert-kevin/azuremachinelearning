import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.offline as pyo
import plotly.graph_objs as go
import dash_table as dt
import pandas as pd
import random
from collections import deque
import data
import plot

# based on 12 columns, bootstrap css
external_stylesheets = ['https://codepen.io/amyoshino/pen/jzXypZ.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = 'Hotspots'

map_data = data.data_prep()

X = deque(maxlen=20)
Y = deque(maxlen=20)
X.append(1)
Y.append(1)

app.layout = html.Div([
    html.Div([
        # Title and Logo
        html.Div([
            html.H1("Interactive Dashboard Title", className="nine columns"),
            html.Img(src="https://businessidentity.nl/wp-content/uploads/2018/09/het-belang-van-een-goed-logo.png",
                    className='three columns',
                    style={
                        'height': '6%',
                        'width': '6%',
                        'float': 'right',
                        'position': 'relative',
                        'padding-top': 6,
                        'padding-right': 6
                    },
            ),
            html.Div(children='''Dash Template Example: Working with a geographic map''',
                    className='nine columns'
            ),
        ], className='row'),
        # Selectors:
        html.Div([
            html.Div([
                html.P('Choose a City:'),
                dcc.Checklist(
                    id='choose_a_city',
                    options=[
                        {'label': str(item),
                         'value': str(item)}
                        for item in set(map_data['name'])],
                    # selected values when app starts
                    value=list(set(map_data['name'])),
                    labelStyle={'display': 'inline-block'} # put next to eachother
                )
            ], className='six columns'),
            html.Div([
                html.P('Choose an Age Group:'),
                dcc.Dropdown(
                    id='choose_an_age',
                    options=[
                        {'label': str(item),
                        'value': str(item)}
                        for item in set(map_data['age'])],
                    multi=True,
                    value=list(set(map_data['age'])), # selected values when app starts
                )
            ], className='six columns'),
        ], className='row'),
        # Map, dataTable, graph and footer:
        html.Div([
            html.Div([
                dcc.Graph(
                    id='geographic_map',
                    # animate=True,
                ),
            ], className='six columns'),
            html.Div([
                dt.DataTable(
                    id='data_table',
                    columns=[{"name": i, "id": i} for i in map_data.columns],
                    data=map_data.to_dict('records'),
                    selected_rows=[],
                    editable=True,
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    row_selectable="multi",
                ),
            ], className="six columns"),
            html.Div([
                dcc.Graph(
                    id='bar_graph',
                ),
            ], className='twelve columns'),
            html.Div([
                dcc.Graph(
                    id='live-graph',
                    animate=True
                ),
                dcc.Interval(
                    id='graph-update',
                    interval=1000 * 1
                )
            ], className='twelve columns'),
            html.Div([
                html.P('Developed by Kevin Albert - ', style={'display': 'inline'}),
                html.A('beire_@hotmail.com', href='mailto:beire_@hotmail.com'),
            ], className='twelve columns'),
        ], className="row"),
    ], className='ten columns offset-by-one'),
])

# live stream graph
@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')])
def update_live_graph(input_data):
    X.append(X[-1] + 1)
    Y.append(Y[-1] + Y[-1] * random.uniform(-0.1, 0.1))

    data = go.Scatter(
        x=list(X),
        y=list(Y),
        name='Scatter',
        mode='lines+markers'
    )

    return {'data': [data],
            'layout': go.Layout(
                xaxis=dict(range=[min(X), max(X)]),
                yaxis=dict(range=[min(Y), max(Y)]),
            )}

# interactivity on the geo map:
@app.callback(
    Output('geographic_map', 'figure'),
    [Input('data_table', 'data'),
     Input('data_table', 'selected_rows')])
def map_selection(data, selected_rows):
    aux = pd.DataFrame(data)
    temp_df = aux.iloc[selected_rows, :]
    if len(selected_rows) == 0:
        return plot.gen_map(aux)
    return plot.gen_map(temp_df)

@app.callback(
    Output('data_table', 'selected_rows'),
    [Input('choose_a_city', 'value'),
     Input('choose_an_age', 'value')])
def update_selected_row_indices(city, age):
    map_aux = map_data.copy()
    map_aux = map_aux[map_aux['name'].isin(city)]  # City filter
    map_aux = map_aux[map_aux["age"].isin(age)]  # Age filter
    rows = list(map_aux.index.values)
    return rows

@app.callback(
    Output('bar_graph', 'figure'),
    [Input('data_table', 'data'),
     Input('data_table', 'selected_rows')])
def update_figure(rows, selected_row_indices):
    dff = pd.DataFrame(rows)
    layout = go.Layout(
        bargap=0.05,
        bargroupgap=0,
        barmode='group',
        showlegend=False,
        dragmode="select",
        xaxis=dict(
            showgrid=False,
            nticks=50,
            fixedrange=False
        ),
        yaxis=dict(
            showticklabels=True,
            showgrid=False,
            fixedrange=False,
            rangemode='nonnegative'
        )
    )

    data = go.Bar(
            x=dff.groupby('name', as_index=False).count()['name'],
            y=dff.groupby('name', as_index=False).count()['age']
            )

    return go.Figure(data=data, layout=layout)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True, port=8050)
