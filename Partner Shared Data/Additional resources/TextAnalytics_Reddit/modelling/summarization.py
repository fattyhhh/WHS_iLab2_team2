import pandas as pd
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.nlp.tokenizers import Tokenizer
import streamlit as st
import re


def summarize_dataframe(df, column_name, num_sentences=2):
    """
    Function to summarize the text in a dataframe column using the TextRank algorithm.
    :param df: pandas.DataFrame, the dataframe containing the text column
    :param column_name: str, the name of the text column to summarize
    :param num_sentences: int, the number of sentences to include in the summary
    """
    # Clean the None values from the dataframe
    df = df.dropna(subset=[column_name])

    # Remove duplicate values in the specified column
    df.drop_duplicates(subset=[column_name], inplace=True)

    # Initialize a TextRankSummarizer object
    summarizer = TextRankSummarizer()

    # Create a new column for the summarized text
    df[column_name + '_summarized'] = ''

    # Summarize each record in the dataframe
    for index, row in df.iterrows():
        # Initialize a parser with the text to summarize
        text = row[column_name]
        parser = PlaintextParser.from_string(text, Tokenizer('english'))

        # Summarize the text
        summary = summarizer(parser.document, num_sentences)
        summarized_version = [str(sentence) for sentence in summary]

        # Add the summarized version to the new column
        df.at[index, column_name + '_summarized'] = ' '.join(summarized_version)

        # Remove special characters from the summarized text using regex
        pattern = r'[^a-zA-Z0-9\s]+'
        df.at[index, column_name + '_summarized'] = re.sub(pattern, '', ' '.join(summarized_version)).strip()

    # Display the original and summarized data
    st.header('Original and Summarized Data')
    st.dataframe(df[[column_name, column_name + '_summarized']])
