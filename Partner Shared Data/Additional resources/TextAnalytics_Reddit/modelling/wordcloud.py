import matplotlib

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st

def generate_wordcloud(text, max_words):
    """
    Function to generate a wordcloud from text data.
    :param text: str, the text data to generate the wordcloud from.
    """

    # Convert any non-string values to strings
    if not isinstance(text, str):
        text = [str(t) for t in text]
        text = ' '.join(text)

    # Create a wordcloud object
    wc = WordCloud(
        width=800,                     # Width of the wordcloud image
        height=400,                    # Height of the wordcloud image
        background_color='black',      # Background color of the wordcloud image
        colormap='tab20c',             # Colormap used to color the wordcloud image
        max_words=max_words            # Maximum number of words to include in the wordcloud
    )

    # Generate wordcloud from the text
    wc.generate(text)
    #wordcloudres = wc.generate(text)
    #print(dict(wordcloudres.words_))

    # Display the wordcloud
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
