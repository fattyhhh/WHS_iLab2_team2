# Import required libraries
import streamlit as st
import pandas as pd
import base64
import os

# Import user-defined modules
from DataCollection.praw_reddit_data_collector import RedditScraper
from EDA.dataClean import cleandata
from EDA.cleanpreviousfiles import cleanpreviousfiles
from modelling.wordcloud import generate_wordcloud
from modelling.maxminwords import get_max_min_words
from EDA.customstopword import remove_custom_stopwords
from modelling.concordance import get_concordance
from modelling.lda import get_lda
from modelling.ner import get_ner
from modelling.ngrams import get_ngrams
from modelling.summarization import summarize_dataframe
from modelling.sentiment_analysis import plot_sentiment_analysis
from modelling.summarization import summarize_dataframe

# Set the title and favicon of the Streamlit app
st.set_page_config("Reddit Data Exploration", "🤖", layout='wide')

# Add a title to the app
st.title('Reddit Search and Data Exploration')

# Add a space
st.write("")

# Clean the previous files from the file system
cleanpreviousfiles()

# The above function is user-defined and it cleans the files that were created during the last run of the app.
# This is done so that the new files created during the current run do not get mixed up with the old ones.

# Option to upload previous data
#uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
st.subheader("**Upload a CSV file (Previously collected data)**")
uploaded_file = st.file_uploader("", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    data = data.reset_index().rename(columns={'index': 'id'})  # Add index column and rename it to 'id'
    st.success("Data uploaded successfully!")
    st.markdown("""
                            **Raw Data:**  
                            *The Raw Data section displays the unprocessed, original data obtained from the Reddit search or uploaded CSV file. It provides a glimpse of the data in its raw form without any modifications or cleaning.*
                        """)
    st.dataframe(data[['content', 'date']], width=1000)
    # Hide search options if file is uploaded
    st.experimental_set_query_params(file_uploaded="true")
else:
    data = None
    # Show search options if file is not uploaded
    if st.experimental_get_query_params().get("file_uploaded") != "true":
        st.warning("Please upload a CSV file or run a new search.")
        st.subheader("Or enter your search query:")
        time_filters = ['all', 'hour', 'day', 'week', 'month', 'year']
        st.markdown("""
            **Time filters**  
            Specify a time filter to narrow down the search results based on the time of the Reddit posts. By default, the search includes posts from all time periods.

            - **all**: collects data randomly.  
            - **hour**: collects data of last 1 hour.  
            - **day**: collects data of last 1 day.  
            - **week**: collects data of last 1 week.  
            - **month**: collects data of last 1 month.
            - **year**: collects data of last 1 year.  
        """)

        time_filter = st.selectbox('Choose a time filter:', time_filters, index=0)
        sort_methods = ['relevance', 'hot', 'top', 'new', 'comments']
        st.markdown("""
                    **Sort methods:**  
                    Select a sorting method to organize the search results. The default sorting method is relevance, which prioritizes posts that are most relevant to your search query.

                    - **relevance** : sorts posts based on their relevance to the search query.  
                    - **hot**: sorts posts based on popularity and recent activity.
                    - **top**: sorts posts based on the highest upvotes and engagement.
                    - **new**: sorts posts based on their submission time, displaying the most recent ones first.  
                    - **comments**: sorts posts based on the number of comments they have received.
                """)
        sort_method = st.selectbox('Choose a sort method:', sort_methods, index=0)
        search_query = st.text_input(
            'Enter the keywords or phrases you want to search and press ENTER. (Example: (burnout OR stress OR "mental anxiety") AND work))"',
            value='')
        if search_query != '' and time_filter != '' and sort_method != '':
            cleanpreviousfiles()
            scraper = RedditScraper(time_filter=time_filter, sort_method=sort_method)
            scraper.run(search_query, 'reddit_data.csv')
            # Load the saved data
            data = pd.read_csv('reddit_data.csv')
            data = data.reset_index().rename(columns={'index': 'id'})  # Add index column and rename it to 'id'
            # Display the data in a table
            st.markdown("""
                        **Raw Data:**  
                        *The Raw Data section displays the unprocessed, original data obtained from the Reddit search or uploaded CSV file. It provides a glimpse of the data in its raw form without any modifications or cleaning.*
                    """)
            st.dataframe(data[['content', 'date']], width=1000)

            # add the download functionality
            if len(data) > 0:
                st.write("To download uncleaned the data, click the button below:")
                csv = data.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="reddit_data_uncleaned.csv"><button>Download Raw Data</button></a>'
                st.markdown(href, unsafe_allow_html=True)

if data is not None:
    # call the cleaning function

    cleandf = cleandata(data)

    # Display the cleaned data in a table
    st.markdown("""
                            **Clean Data:**  
                            *In the Cleaned Data section, you can find the processed and refined version of the data. It has undergone cleaning techniques to remove irrelevant or erroneous information, making it easier to analyze and interpret.*
                        """)
    st.dataframe(cleandf[['cleaned', 'date']], width=1000)

    # add the download functionality
    if len(cleandf) > 0:
        st.write("To download the cleaned data, click the button below:")
        csvclean = cleandf.to_csv(index=False)
        b64clean = base64.b64encode(csvclean.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64clean}" download="reddit_data_cleaned.csv"><button>Download Cleaned Data</button></a>'
        st.markdown(href, unsafe_allow_html=True)

    # Remove custom stop words
    st.subheader("Custom Stopwords")
    st.markdown(""" 
                    *If there are specific words you don't want to include in the word cloud or any other analysis, you can enter them in the Custom Stopwords section. This allows you to customize the output by excluding those particular words.*
                    """)
    custom_stop_words = st.text_input("Enter comma-separated words to remove from the text and press ENTER:")
    if custom_stop_words:
        stop_words_list = [word.lower().strip() for word in custom_stop_words.split(",")]
        remove_custom_stopwords(cleandf, stop_words_list)
        st.success(f"Removed custom stop words: {stop_words_list}")
    # Generate and display the wordcloud
    st.subheader("Wordcloud")
    st.markdown("""  
                    *The Word Cloud feature generates a visual representation of the most frequently occurring words in the dataset. You can adjust the slider to control the number of words displayed in the cloud, allowing you to focus on the most relevant or significant terms.*
                    """)
    text = ' '.join(cleandf['cleaned'].astype(str).tolist())
    max_words = st.slider("Max Words", 50, 300, 100)
    generate_wordcloud(text, max_words)

    # Show top and bottom 10 words
    st.subheader("Top and Rare 10 words")
    st.markdown("""  
                *The section highlights the top and least frequently occurring 10 words in the dataset. It provides insights into unique or uncommon terms that may require special attention during analysis*
                """)
    fig = get_max_min_words(cleandf, 'cleaned')
    st.plotly_chart(fig)

    # show the other modelling
    st.subheader("Advanced Analysis")
    st.markdown("""
                *In this section, you have five options to choose from: Concordance, Summarization, NGrams, NER (Named Entity Recognition), and Topic Modelling.*
                """)

    modelling = st.selectbox('Choose an analysis type', ['Concordance', 'Summarization', 'NGrams', 'Topic modelling', 'NER', "Sentiment Analysis"])#"Sentiment Analysis", 'NER', 'LDA'])
    if modelling == 'Concordance':
        st.header('Concordance')
        st.subheader('To show the context surrounding a particular word in a post.')

        # Explanation of visualization features
        st.write('1. Enter a single keyword.')
        st.write(
            '2. The result allows you to see all the instances of the word in all the posts, along with the words immediately preceding and following it.')
        st.write(
            '3. By examining the context in which a word appears, it may be possible to **determine its intended/broader meaning of the word** in the post.')

        # Add a text input box for the user to enter the input word
        input_word = st.text_input("Enter a word for concordance:")
        if input_word:
            st.write(f"Concordance associated with '{input_word}':")
            #num_words = st.slider('Number of words', 1, 200, 30)
            result = get_concordance(cleandf, "cleaned", input_word, num_words=100)
            for line in result:
                st.markdown(line, unsafe_allow_html=True)
        else:
            st.write("Please enter a word for concordance.")
    elif modelling == 'Topic modelling':
        get_lda(cleandf, 'cleaned', data)
    elif modelling == 'NER':
        get_ner(cleandf, 'cleaned', data)
    elif modelling == 'NGrams':
        get_ngrams(cleandf, 'cleaned', data)
    elif modelling == 'Summarization':
        summarize_dataframe(data,'content')
    elif modelling == 'Sentiment Analysis':
        plot_sentiment_analysis(cleandf, 'cleaned')

else:
    st.write("Nothing to show now. Search or upload file first")
