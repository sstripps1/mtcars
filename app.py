import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('mtcars.tsv', sep='\t', skiprows=4)
max_rows = len(df)

def create_table(dataframe, max_rows=max_rows):
    return html.Table(
        [html.Tr([html.Th(col) for col in dataframe.columns])] +
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))],
        id='my-table'
    )

def create_bar_graph(dataframe):
    return dcc.Graph(
        figure={
            'data': [
                dict(
                    x=['Min mpg', 'Mean mpg', 'Max mpg'],
                    y=[dataframe.mpg.min(), dataframe.mpg.mean(), dataframe.mpg.max()],
                    type='bar'
                )
            ],
            'layout': {'Title': 'mpg Stats'}
        }
    )

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H4(children='MT Cars'),
    html.Div(id='my-table'),
    html.Div(id='min-mean-max'),
    dcc.Slider(id='my-slider', min=1, max=8, step=1, value=1,
               marks={i: 'Carb {}'.format(i) for i in range(8)})
])

@app.callback(
    [Output('my-table', 'children'),
     Output('min-mean-max', 'children')],
    [Input('my-slider', 'value')]
)
def filter_by_carb(carb):
    filtered_df = df.query('carb == @carb')
    return create_table(filtered_df), create_bar_graph(filtered_df)

if __name__ == '__main__':
    app.run_server(debug=True)





