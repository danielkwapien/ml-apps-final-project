import pandas as pd
from dash import Dash, dcc, html

"""data = (
    pd.read_csv("avocado.csv")
    .query("type == 'conventional' and region == 'Albany'")
    .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d"))
    .sort_values(by="Date")
)"""

external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Avocado Analytics: Understand Your Avocados!"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🎙️", className="header-emoji"),
                html.H1(
                children="Podcast Classifier",className="header-title"
                ),
                html.P(
                    children=(
                        "Analyze podcast data to predict the genre of the podcast"
                    ),className="header-description"        
                ),
            ] 
        )
    ],className="header"
)



if __name__ == "__main__":
    app.run_server(debug=True)