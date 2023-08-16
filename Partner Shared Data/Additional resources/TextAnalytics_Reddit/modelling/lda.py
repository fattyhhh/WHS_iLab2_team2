import streamlit as st
import gensim
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
from modelling.summarization import summarize_dataframe
from modelling.lda_tuning import get_best_model

cleaned_col = 'cleaned'


def get_lda(df, column, dataframe):
    """
    Perform Latent Dirichlet Allocation (LDA) topic modeling on the given DataFrame.

    Parameters:
    - df: DataFrame containing the text data to be modeled
    - column: Name of the column in the DataFrame containing the text data
    - dataframe: Original DataFrame containing additional columns

    Returns:
    None
    """

    # Extract the 'content' column as a list of sentences
    data = [str(sent).split() for sent in df[column].tolist()]

    # Create dictionary and corpus
    dictionary = gensim.corpora.Dictionary(data)
    corpus = [dictionary.doc2bow(doc) for doc in data]

    # Display visualization using Streamlit
    st.header('Latent Dirichlet Allocation (LDA Topic Model)')
    st.subheader('To categorize large volumes of text data into meaningful groups of topic.')
    st.markdown('*\*a topic means a set of words that frequently co-occur in a collection of posts.*')

    # Explanation of visualization features
    st.markdown(
        '1. Each bubble represents an identified topic. **The larger the bubble, the higher percentage of the number of posts in the corpus is about that topic**.')
    st.markdown(
        '2. Blue bars represent the overall frequency of each word in the corpus. If no topic is selected, the blue bars of the most frequently used words will be displayed.')
    st.markdown('3. Red bars represent the frequency of word within the selected topic.')
    st.markdown('4. **The further the bubbles are away from each other, the more different they are**.')
    st.markdown(
        '5. When relevance metric slider is set for λ = 1 (by default), it sorts words by their frequency within the specific topic (by their red bars).')
    st.markdown(
        '6. By contrast, setting λ = 0 words sorts words whose red bars are nearly as long as their blue bars will be sorted at the top.')

    # Build LDA model
    # Support hyperparameter tuning
    st.markdown(
        'Select if derive the best model parameters automatically or manually to the analysis. Note that auto takes time!')
    is_auto = st.radio('Select an option:', ('Manual', 'Auto'))
    if is_auto == 'Auto':
        lda_model = get_best_model(df)
    else:
        # Add a slider for the number of topics
        num_topics = st.slider('Select the number of topics:', min_value=2, max_value=10, value=3)
        lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, num_topics=num_topics, id2word=dictionary,
                                                    alpha='symmetric', eta='symmetric', iterations=100)

    # Visualize topics
    vis_data = gensimvis.prepare(lda_model, corpus, dictionary, R=10)
    html_string = pyLDAvis.prepared_data_to_html(vis_data)
    st.components.v1.html(html_string, width=1500, height=1000, scrolling=True)

    selected_word_lda = st.text_input("Enter a word to get the raw data and summarization:")
    if selected_word_lda == '':
        st.write("First put a word to see the original and summary data")
    else:
        # Join the original DataFrame with the LDA DataFrame based on the 'id' column
        joined_df = dataframe.merge(df, on='id', how='left')

        # Filter the joined DataFrame to select rows where the cleaned text column contains the selected word
        df_selected_lda = joined_df[joined_df[cleaned_col].str.contains(selected_word_lda, na=False)]
        df_selected_lda = df_selected_lda.rename(columns={'content_x': 'content'})

        if not df_selected_lda.empty:
            # Summarize the selected_word data
            summarize_dataframe(df_selected_lda, 'content', 1)
        else:
            st.write("No records found for the selected word.")
        df_selected_lda = None
