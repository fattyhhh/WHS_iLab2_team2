import pandas as pd
import nltk

# Protik
def remove_custom_stopwords(df, stop_words):
    """
    Function to remove custom stop words from the 'cleaned' column of a dataframe.
    :param df: pandas.DataFrame, the dataframe containing the 'cleaned' column
    :param stop_words: list of strings, the custom stop words to remove
    :return: None
    """
    # Split the lemmatized words in each row into a list of words
    df['cleaned'] = df['cleaned'].str.split()

    # Remove custom stop words from each list of words
    df['cleaned'] = df['cleaned'].apply(lambda words: [word for word in words if word not in stop_words])

    # Join the remaining words back into a string
    df['cleaned'] = df['cleaned'].apply(lambda words: ' '.join(words))

    # Update the 'cleaned' column with the new string
    df['cleaned'] = df['cleaned'].str.strip()
