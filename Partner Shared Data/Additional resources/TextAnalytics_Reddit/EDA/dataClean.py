import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download all resources from NLTK
nltk.download('all')
# nltk.download('wordnet')
# nltk.download('stopwords')

def cleandata(data):
    """
    Clean the data by performing various preprocessing steps.

    Parameters:
    - data: Pandas DataFrame containing the data to be cleaned

    Returns:
    - df: Cleaned Pandas DataFrame
    """

    # Read the CSV file into a Pandas DataFrame
    df = data

    if df is None:
        return None

    # Removing None values
    df = df.dropna(subset=['content'])

    # Removing duplicate values
    df.drop_duplicates(subset=['content'], inplace=True)

    # Converting into lower case
    df['content'] = df['content'].str.lower()

    # Remove special characters
    def remove_special_characters(text):
        """
        Remove special characters from the text using regular expressions.

        Parameters:
        - text: Text to be processed

        Returns:
        - Cleaned text with special characters removed
        """
        if isinstance(text, str):
            pattern = r'[^a-zA-Z\s]+'
            return re.sub(pattern, '', text)
        else:
            return text

    df.content = df.content.apply(lambda x: remove_special_characters(x))

    # Tokenization
    df['content_tokens'] = df['content'].astype(str).apply(nltk.word_tokenize)

    # Lemmatization
    lemmatizer = WordNetLemmatizer()

    def lemmatize(token_list):
        """
        Lemmatize the tokens in a token list.

        Parameters:
        - token_list: List of tokens to be lemmatized

        Returns:
        - String with lemmatized tokens joined by spaces
        """
        tokens = [lemmatizer.lemmatize(token) for token in token_list]
        return " ".join(tokens)

    df['cleaned_without_stopwords'] = df['content_tokens'].apply(lemmatize)

    # Built-in stopword removal
    stop_words = set(stopwords.words('english'))  # Set of stopwords

    def remove_stopwords(text):
        """
        Remove stopwords from the text.

        Parameters:
        - text: Text to be processed

        Returns:
        - Text with stopwords removed
        """
        if isinstance(text, str):
            # Remove URLs
            text = re.sub(r'http\S+|www\S+', '', text)
            # Remove stop words
            text = ' '.join([word for word in text.split() if word.lower() not in stop_words])
        return text

    # Apply the remove_stopwords function to the 'cleaned_without_stopwords' column
    df['cleaned'] = df['cleaned_without_stopwords'].apply(lambda x: remove_stopwords(x))

    # Export to a local CSV file
    cleaned_filename = 'cleaned.csv'
    df.to_csv(cleaned_filename, index=True)

    return df

