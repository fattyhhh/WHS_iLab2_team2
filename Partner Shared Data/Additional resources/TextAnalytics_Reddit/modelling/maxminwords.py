import pandas as pd
from collections import Counter
import plotly.graph_objs as go
from plotly.subplots import make_subplots


def get_max_min_words(df, col):
    """
    Function to get the top 10 and bottom 10 occurring words in a given column of a dataframe

    Parameters:
    - df: pandas.DataFrame, the dataframe containing the text column
    - col: str, the name of the text column

    Returns:
    - plotly.graph_objs.Figure, a figure object showing the 10 most and least frequent words side by side
    """
    # Create a list of all words in the column
    words_list = df[col].str.split(expand=True).stack().tolist()

    # Count the frequency of each word
    word_counts = dict(Counter(words_list))

    # Get the top 10 and bottom 10 most frequent words
    top10 = dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:10][::-1])
    bottom10 = dict(sorted(word_counts.items(), key=lambda x: x[1])[:10])

    # Create the plotly subplots
    fig = make_subplots(rows=1, cols=2, subplot_titles=('Top 10 Words', 'Rare 10 Words'), horizontal_spacing=0.3)

    # Add bar traces for top 10 words subplot
    fig.add_trace(go.Bar(x=list(top10.values()), y=list(top10.keys()), name='Top words', orientation='h'), row=1, col=1)

    # Add bar traces for bottom 10 words subplot
    fig.add_trace(go.Bar(x=list(bottom10.values()), y=list(bottom10.keys()), name='Rare words', orientation='h'), row=1,
                  col=2)

    # Update layout of the figure
    fig.update_layout(title='Top and Rare 10 words', barmode='group')

    return fig
