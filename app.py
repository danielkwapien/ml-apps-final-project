import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
from wordcloud import WordCloud
import base64
import io


data = (pd.read_csv("talks.csv"))
data['recorded_date'] = pd.to_datetime(data['recorded_date'], format="mixed")

data['topic_names'] = data['topic_names'].str.split(',')
data = data.explode('topic_names')
topic_counts = data['topic_names'].value_counts()
speaker_counts = data['speaker'].value_counts()
talk = data['title']
speaker_counts = data['speaker'].value_counts().sort_values(ascending=False)
speakers = speaker_counts.index.unique()
topics = data['topic_names'].sort_values().unique()




external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]
def generate_wordcloud_image():
    all_topics = ','.join(data['topic_names'].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_topics)
    img = io.BytesIO()
    wordcloud.to_image().save(img, 'PNG')
    img.seek(0)
    base64_img = base64.b64encode(img.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{base64_img}"



app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "TEDtalks analysis"


app.layout = html.Div([
    
    html.Div(children=[
                html.Img(src="/static/image.png", className="header-image"),
                html.H1(
                children="TEDtalks Classifier",className="header-title"
                ),
                html.P(
                    children=(
                        "Analyze TED talks content to predict the topic of the talk"
                    ),className="header-description"        
                ),],className="header"),
    html.Div([
        html.Img(src=generate_wordcloud_image(), className="graph-container cloud")
    ],),
    html.Div([
        dcc.Graph(figure=px.bar(
            x=topic_counts.index,
            y=topic_counts.values,
            labels={'x': 'Topic', 'y': 'Number of Talks'},
            title='Distribution of Topics Covered in TED Talks'),
            style={'color': '#EB0028'})
    ], className="graph-container"),
    html.Div([
        dcc.Graph(figure=px.scatter(
            data,
            x='event',
            y='views',
            title='Scatter Plot of TED Talks by Event and Views'))
    ], className="graph-container"),
    html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Speaker", className="menu-title"),
                        dcc.Dropdown(
                            id="speaker-filter",
                            options=[
                                {"label": str(speaker), "value": str(speaker)}
                                for speaker in speakers
                            ],
                            value="TED-Ed",
                            clearable=False,
                            className="dropdown",
                        ),
                    ], className="input-section"
                ),

                html.Div(
                    children=[
                        html.Div(
                            children=dcc.Graph(
                                id="views-chart",
                                config={"displayModeBar": False},
                            )
                        ),
                    ],
                    className="graph-container",
                ),
            ]),
        html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Div(children="Topic", className="menu-title"),
                            dcc.Dropdown(
                                id="topic-filter",
                                options=[
                                    {"label": str(topic), "value": str(topic)}
                                    for topic in topics
                                ],
                                value="science",
                                clearable=False,
                                className="dropdown",
                            ),
                        ], className="input-section"
                    ),
                    html.Div(
                        children=[
                            html.Div(
                                children=dcc.Graph(
                                    id="topics-chart",
                                    config={"displayModeBar": False},
                                ),
                                className="card",
                            ),
                        ],
            className="graph-container",
        )],
            className="menu",
        ),
               
], style={'backgroundColor': '#d4d4d4'})

@app.callback(
    Output("views-chart", "figure"),
    Input("speaker-filter", "value"),
)
def view_chart(speaker):

    filtered_data = data[(data["speaker"] == speaker)]
    views_chart_figure = {
        "data": [
            {
                "x": filtered_data["title"],
                "y": filtered_data["views"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {
                "text": "Views of talks",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {
                "fixedrange": True,
                "tickangle": 20  
            },
            "colorway": ["#EB0028"]
        },
    }

    return views_chart_figure

@app.callback(
    Output("topics-chart", "figure"),
    Input("topic-filter", "value")
)
def view_chart(topic):

    filtered_data = data[(data["topic_names"] == topic)]

    topics_chart = {
        "data": [
            {
                "x": filtered_data["duration"],
                "y": filtered_data["views"],
                "mode": "markers",
                "marker": {
                    "size": 10,      
                    "color": "#EB0028"  
                },
            },
        ],
        "layout": {
            "title": {
                "text": "Duration and views of talks with your selected topic",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {
                "title": "Duration (minutes)",
                "fixedrange": True,
                "tickangle": 20 
            },
            "yaxis": {
                "title": "Views"  
            },
            "colorway": ["#17B897"]
        },
    }
    return topics_chart



if __name__ == "__main__":
    app.run_server(debug=True)