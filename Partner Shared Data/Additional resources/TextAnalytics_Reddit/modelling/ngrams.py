import streamlit as st
import pandas as pd
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder
from nltk.collocations import TrigramAssocMeasures, TrigramCollocationFinder
from modelling.concordance import get_concordance
from modelling.summarization import summarize_dataframe

w_bigram = 'Bi-gram'
w_trigram = 'Tri-gram'

def get_top_bigrams(text, n=10):
    """
    Get the top n most significant bigrams from a given text.

    Parameters:
    - text: str, the input text
    - n: int, the number of top bigrams to retrieve (default: 10)

    Returns:
    - top_bigrams: pd.DataFrame, a DataFrame with the top bigrams and their scores
    """
    # Split the lemmatized sentences into individual words
    words = text.split()

    # Create a BigramCollocationFinder object
    bigram_finder = BigramCollocationFinder.from_words(words)

    # Use the PMI association measure to score bigrams
    bigram_measures = BigramAssocMeasures()
    scored_bigrams = bigram_finder.score_ngrams(bigram_measures.pmi)

    # Sort the bigrams by score in descending order
    sorted_bigrams = sorted(scored_bigrams, key=lambda x: x[1], reverse=True)

    # Return the top n bigrams as a DataFrame
    top_bigrams = pd.DataFrame(sorted_bigrams[:n], columns=[w_bigram, 'Score'])
    return top_bigrams

def get_top_trigrams(text, n=10):
    """
    Get the top n most significant trigrams from a given text.

    Parameters:
    - text: str, the input text
    - n: int, the number of top trigrams to retrieve (default: 10)

    Returns:
    - top_trigrams: pd.DataFrame, a DataFrame with the top trigrams and their scores
    """
    # Split the lemmatized sentences into individual words
    words = text.split()

    # Create a TrigramCollocationFinder object
    trigram_finder = TrigramCollocationFinder.from_words(words)

    # Use the PMI association measure to score trigrams
    trigram_measures = TrigramAssocMeasures()
    trigram_scores = trigram_finder.score_ngrams(trigram_measures.pmi)

    # Sort the trigrams by score in descending order
    sorted_trigrams = sorted(trigram_scores, key=lambda x: x[1], reverse=True)

    # Return the top n trigrams as a DataFrame
    top_trigrams = pd.DataFrame(sorted_trigrams[:n], columns=['Tri-gram', 'Score'])
    return top_trigrams

def get_ngrams(df, column, data):
    """
    Perform N-grams analysis on the text data in a given column of a DataFrame.

    Parameters:
    - df: DataFrame containing the text data
    - column: Name of the column containing the text data
    - data: Original DataFrame used for Concordance and Summarization

    Returns:
    None
    """
    # Display visualization using Streamlit
    st.header('N-grams Model')
    st.subheader('To measure the strength of association between words in a text document.')

    # Explanation of visualization features
    st.markdown('1. Choose ' + w_bigram + ' or ' + w_trigram)
    st.markdown('2. Choose the size of the result set.')
    st.markdown('3. The score in the result shows the strength of association between the words.')
    st.markdown(
        '4. Higher scores indicate stronger associations between the words. It implies **these words together are probably more important than the individual words** when studying the post content.')
    st.markdown('5. You can further choose a word to see its Concordance results.')

    sel_gram = st.selectbox('Select ' + w_bigram + ' or ' + w_trigram, [w_bigram, w_trigram])

    if sel_gram == w_bigram:
        # Get the top N bi-grams
        bigram_n = st.number_input('Select top N ' + w_bigram, min_value=5, max_value=50, value=5, step=5)
        bigrams = get_top_bigrams(df[column].str.cat(sep=' '), bigram_n)
        st.write(bigrams)

        # Extract all Bi-gram distinct words into a list of words for Select Box
        words = sorted(list(set([word for bi_gram in bigrams[w_bigram] for word in bi_gram])))
        selected_word = st.selectbox('Select a word', words)

        # Call Concordance or Summarization with the selected word
        selected_option = st.selectbox('Select an option', ['Concordance', 'Summarization'])

        if selected_option == 'Concordance':
            # Call Concordance with selected word
            result = get_concordance(df, column, selected_word, num_words=40)
            for line in result:
                st.markdown(line, unsafe_allow_html=True)
        else:
            joined_df = data.merge(df, on='id', how='left')
            df_selected_ngrams = joined_df[joined_df['cleaned'].str.contains(selected_word, na=False)]
            df_selected_ngrams = df_selected_ngrams.rename(columns={'content_x': 'content'})
            summarize_dataframe(df_selected_ngrams, 'content', 1)
    else:
        # Get the top N tri-grams
        trigram_n = st.number_input('Select top N ' + w_trigram, min_value=5, max_value=50, value=5, step=5)
        trigrams = get_top_trigrams(df[column].str.cat(sep=' '), trigram_n)
        st.write(trigrams)

        # Extract all Tri-gram distinct words into a list of words for Select Box
        words = sorted(list(set([word for tri_gram in trigrams[w_trigram] for word in tri_gram])))
        selected_word = st.selectbox('Select a word', words)

        # Call Concordance or Summarization with selected word
        selected_option = st.selectbox('Select an option', ['Concordance', 'Summarization'])

        if selected_option == 'Concordance':
            # Call Concordance with selected word
            result = get_concordance(df, column, selected_word, num_words=40)
            for line in result:
                st.markdown(line, unsafe_allow_html=True)
        else:
            joined_df = data.merge(df, on='id', how='left')
            df_selected_ngrams = joined_df[joined_df['cleaned'].str.contains(selected_word, na=False)]
            df_selected_ngrams = df_selected_ngrams.rename(columns={'content_x': 'content'})
            summarize_dataframe(df_selected_ngrams, 'content', 1)