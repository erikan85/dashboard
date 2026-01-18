import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Load Excel file
df = pd.read_excel("mu.xlsx")

# Select numeric columns
num_cols = df.select_dtypes(include="number").columns
x_col = num_cols[0]
y_col = num_cols[1]

app = Dash(__name__)

app.layout = html.Div([
    html.H2("Interactive Data Analysis Dashboard"),

    dcc.Graph(id="scatter"),

    html.Div([
        dcc.Graph(id="histogram"),
        dcc.Graph(id="boxplot")
    ], style={"display": "flex"}),

    dcc.Graph(id="barchart")
])

@app.callback(
    Output("scatter", "figure"),
    Input("scatter", "selectedData")
)
def update_scatter(_):
    fig = px.scatter(df, x=x_col, y=y_col)
    fig.update_layout(dragmode="select")
    return fig

@app.callback(
    Output("histogram", "figure"),
    Output("boxplot", "figure"),
    Output("barchart", "figure"),
    Input("scatter", "selectedData")
)
def update_views(selected):
    if selected:
        idx = [p["pointIndex"] for p in selected["points"]]
        filtered = df.iloc[idx]
    else:
        filtered = df

    hist = px.histogram(filtered, x=x_col, title="Distribution")
    box = px.box(filtered, y=y_col, title="Spread")
    bar = px.bar(filtered, y=y_col, title="Values")

    return hist, box, bar

if __name__ == "__main__":
    app.run(debug=True)
