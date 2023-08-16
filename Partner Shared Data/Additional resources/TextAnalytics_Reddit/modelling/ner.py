import spacy.cli
import streamlit as st
import spacy
from modelling.summarization import summarize_dataframe

def load_model():
    """
    Load the spaCy language model for Named Entity Recognition (NER).
    If the model is not installed, download and install it.

    Returns:
    - nlp: Loaded spaCy language model
    """
    try:
        nlp = spacy.load('en_core_web_sm')
    except OSError:
        st.write('Downloading language model... this may take a while')
        spacy.cli.download("en_core_web_sm")
        nlp = spacy.load('en_core_web_sm')
    return nlp

def get_ner(df, column, dataframe):
    """
    Perform Named Entity Recognition (NER) on the text data in a given column of a DataFrame.

    Parameters:
    - df: DataFrame containing the text data
    - column: Name of the column containing the text data
    - dataframe: Original DataFrame used for joining and summarization

    Returns:
    None
    """
    # Check if en_core_web_sm model is installed, and install it if not
    # Display visualization using Streamlit
    st.header('Named Entity Recognition')
    st.subheader('To identify important people, places, events, and other entities mentioned in the posts.')

    # Load the spaCy language model
    nlp = load_model()

    nlp.max_length = 2000000

    # Process the text with spaCy
    text = ' '.join(df[column])
    doc = nlp(text)

    # Chunk the input text into smaller pieces
    text_chunks = [df[column][i:i + 100000] for i in range(0, len(df[column]), 100000)]

    # Process each chunk with spaCy
    entities_by_label = {}
    for chunk in text_chunks:
        doc = nlp(' '.join(chunk))

        # Group the entities by label
        for ent in doc.ents:
            label = ent.label_
            if label not in entities_by_label:
                entities_by_label[label] = []
            entities_by_label[label].append(ent.text)

    # Map SpaCy label to plain English
    label_map = {
        'PERSON': 'People',
        'NORP': 'Nationality/Interest Group',
        'FAC': 'Infrastructure',
        'ORG': 'Organization',
        'GPE': 'Country/City',
        'LOC': 'Location (Not Country/City)',
        'PRODUCT': 'Product',
        'EVENT': 'Event',
        'WORK_OF_ART': 'Literature',
        'LAW': 'Law',
        'LANGUAGE': 'Language',
        'MONEY': 'Money'
    }

    # Print the entities grouped by label with remapped labels
    for label, entities in entities_by_label.items():
        remapped_label = label_map.get(label, None)
        if remapped_label is not None:
            # use set() to remove duplicates
            st.write(remapped_label, list(set(entities)))

    # get the raw and summarized data from here
    selected_word_ner = st.text_input("Enter a word to get the raw data and summarization:")
    if selected_word_ner == '':
        st.write("First put a word to see the original and summary data")
    else:
        joined_df = dataframe.merge(df, on='id', how='left')
        df_selected_ner = joined_df[joined_df['cleaned'].str.contains(selected_word_ner, na=False)]
        df_selected_ner = df_selected_ner.rename(columns={'content_x': 'content'})
        if not df_selected_ner.empty:
            # Summarize the selected_word data
            summarize_dataframe(df_selected_ner, 'content', 1)
        else:
            st.write("No records found for the selected word.")
        df_selected_ner = None
