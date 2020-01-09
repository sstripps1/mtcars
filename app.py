import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

df = pd.read_csv("mtcars.tsv", sep="\t", skiprows=4)
max_rows = len(df)


def count_and_std(dataframe):
    count = dataframe.mpg.count()
    std = dataframe.mpg.std()
    return "Number of Cars: {}<br>Standard Dev of mpg: {}".format(count, round(std, 2))


def create_table(dataframe, max_rows=max_rows):
    return html.Table(
        [html.Tr([html.Th(col) for col in dataframe.columns])]
        + [
            html.Tr([html.Td(dataframe.iloc[i][col]) for col in dataframe.columns])
            for i in range(min(len(dataframe), max_rows))
        ],
    )


def display_model_info(dataframe, min_max):
    if len(dataframe) == 0:
        return ""
    else:
        if min_max == "min":
            row = dataframe.loc[dataframe.mpg.idxmin()]
        elif min_max == "max":
            row = dataframe.loc[dataframe.mpg.idxmax()]
        return "Model: {}<br>mpg: {}<br>Cylinders: {}".format(
            row.model, row.mpg, row.cyl
        )


def create_bar_graph(dataframe):
    return dcc.Graph(
        figure={
            "data": [
                dict(
                    x=["Min mpg", "Mean mpg", "Max mpg"],
                    y=[dataframe.mpg.min(), dataframe.mpg.mean(), dataframe.mpg.max()],
                    type="bar",
                    hovertext=[
                        display_model_info(dataframe, "min"),
                        "Mean mpg: {}<br>{}".format(
                            round(dataframe.mpg.mean(), 2), count_and_std(dataframe)
                        ),
                        display_model_info(dataframe, "max"),
                    ],
                    hoverinfo="text",
                )
            ],
            "layout": {"Title": "mpg Stats"},
        }
    )


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        html.H4(children="Motor Trend Cars"),
        dcc.Tabs(
            id="tabs",
            value="tab-1",
            children=[
                dcc.Tab(label="Table", value="tab-1"),
                dcc.Tab(label="Chart", value="tab-2"),
            ],
        ),
        dcc.Slider(
            id="my-slider",
            min=1,
            max=8,
            step=1,
            value=1,
            marks={i: "Carb: {}".format(i) for i in range(8)},
        ),
        html.Div(id="my-output"),
    ]
)


@app.callback(
    Output("my-output", "children"),
    [Input("tabs", "value"), Input("my-slider", "value")],
)
def filter_by_carb(tab, carb):
    filtered_df = df.query("carb == @carb")
    if tab == "tab-1":
        return create_table(filtered_df)
    elif tab == "tab-2":
        return create_bar_graph(filtered_df)


if __name__ == "__main__":
    app.run_server(debug=True)
