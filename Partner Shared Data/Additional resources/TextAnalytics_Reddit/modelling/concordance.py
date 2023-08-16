import streamlit as st
from nltk.text import ConcordanceIndex

def get_concordance(df, column, word, num_words=100):
    """
    Get the concordance lines for a given word in a DataFrame column
    :param df: pandas.DataFrame, the DataFrame containing the column
    :param column: str, the column to search for the word
    :param word: str, the word to find concordance for
    :param num_words: int, the number of words to show on either side of the word
    :return: list of str, the concordance lines for the word
    """
    # Check if the word is a single word and is not empty
    if " " in word or len(word.strip()) == 0:
        st.warning("Please put one word for concordance search")
        return []

    # Join the text in the column into a single string
    text = " ".join(df[column].values)

    # Create a ConcordanceIndex object from the text
    concordance_index = ConcordanceIndex(text.split())

    # Find concordance lines for the word
    concordance_lines = concordance_index.find_concordance(word, width=num_words*2)

    # Build the HTML div elements for the concordance lines
    result = []
    for line in concordance_lines:
        # Highlight the word in the line
        highlighted_line = line.line.replace(word, f"<b>{word}</b>")
        # Split the line into words
        words = highlighted_line.split()
        # Find the index of the word in the line
        word_index = words.index(f"<b>{word}</b>")
        # Get the start and end indices of the window around the word
        start_index = max(0, word_index - num_words)
        end_index = min(len(words), word_index + num_words + 1)
        # Extract the window around the word
        window = words[start_index:end_index]
        # Join the window back into a string and wrap it in a div element
        div_element = f'<div style="margin-bottom: 10px;">{" ".join(window)}</div>'
        result.append(div_element)

    # Return the list of HTML div elements
    if len(result) > 0:
        return result
    else:
        return [f"No concordance lines found for the word '{word}'"]
