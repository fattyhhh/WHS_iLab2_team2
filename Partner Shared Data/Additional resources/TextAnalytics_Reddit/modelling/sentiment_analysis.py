# Import necessary libraries
from textblob import TextBlob
import plotly.express as px
import streamlit as st


# Define a function to perform sentiment analysis on a given sentence
def get_sentiment(sentence):
    """
    Function to perform sentiment analysis on a given sentence using TextBlob library.
    :param sentence: str, the input sentence to analyze
    :return: str, the sentiment of the sentence ('Positive', 'Negative', or 'Neutral')
    """
    # Create a TextBlob object for the sentence
    blob = TextBlob(sentence)

    # Get the polarity score of the sentence
    sentiment = blob.sentiment.polarity

    # Determine the sentiment label based on the polarity score
    if sentiment > 0:
        return "Positive"
    elif sentiment < 0:
        return "Negative"
    else:
        return "Neutral"


def plot_sentiment_analysis(df, column_name):
    """
    Function to perform sentiment analysis on a column of a DataFrame and visualize the sentiment distribution.
    :param df: pandas.DataFrame, the DataFrame containing the text column
    :param column_name: str, the name of the text column to analyze
    """
    # Apply the get_sentiment function to the column and create a new 'sentiment' column in the DataFrame
    df['sentiment'] = df[column_name].apply(get_sentiment)

    # Count the occurrences of each sentiment label
    sentiment_counts = df['sentiment'].value_counts().reset_index()
    sentiment_counts.columns = ['sentiment', 'count']

    # Specify the color of the bars based on sentiment
    color_discrete_map = {'Positive': 'green', 'Negative': 'red', 'Neutral': 'yellow'}

    # Create a bar plot to visualize the sentiment distribution
    fig = px.bar(sentiment_counts, x='sentiment', y='count',
                 color='sentiment', color_discrete_map=color_discrete_map)

    # Add a title and legend to the plot
    fig.update_layout(title='Sentiment Analysis of {}'.format(column_name),
                      legend_title='Sentiment')

    # Display the plot using Streamlit
    st.plotly_chart(fig)
