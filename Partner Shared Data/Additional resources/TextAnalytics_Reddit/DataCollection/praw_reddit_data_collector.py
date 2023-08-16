import praw
import csv
import threading
from queue import Queue
from datetime import datetime

class RedditScraper:
    # Reddit API credentials
    client_id = 'T0Yw8hzg-_CpReakMslQZQ'
    client_secret = 'bnigIaBeAaX2c0ENNZwwKdYGdKmrxg'
    user_agent = 'Mostafa Mohiuddin Jalal'

    def __init__(self, search_limit=None, num_threads=10, time_filter='all', sort_method='relevance'):
        """
        Initialize the RedditScraper class with specified parameters.

        Parameters:
        - search_limit: The maximum number of posts to fetch (default: None, fetch all matching posts)
        - num_threads: The number of threads to use for fetching posts (default: 10)
        - time_filter: The time filter for posts ('all', 'day', 'hour', 'month', 'week', 'year') (default: 'all')
        - sort_method: The sorting method for posts ('relevance', 'hot', 'top', 'new', 'comments') (default: 'relevance')
        """
        self.reddit = praw.Reddit(client_id=self.client_id, client_secret=self.client_secret, user_agent=self.user_agent)
        self.search_limit = search_limit
        self.num_threads = num_threads
        self.time_filter = time_filter
        self.sort_method = sort_method

        # Queue to store the scraped Reddit posts
        self.result_queue = Queue()
        self.processed_ids = set()  # Set to keep track of processed post IDs

    def scrape_data(self):
        """
        Generator function to process scraped data.

        Yields:
        - result_dict: A dictionary containing the processed post data
        """
        while True:
            post = self.result_queue.get()
            if post is None:
                break
            content = post.selftext.replace('\n', ' ')  # Replace newlines with spaces
            post_date = datetime.fromtimestamp(post.created_utc).strftime('%d-%m-%Y')  # Convert UTC timestamp to conventional format
            result_dict = {
                'subreddit': post.subreddit.display_name,
                'username': post.author.name,
                'url': post.url,
                'upvotes': post.score,
                'content': content,
                'date': post_date
            }
            if post.id not in self.processed_ids:
                self.processed_ids.add(post.id)
                self.result_queue.task_done()
                yield result_dict  # Yield the processed result
            else:
                self.result_queue.task_done()

    def fetch_data(self, search_query):
        """
        Fetch data from Reddit based on the search query.

        Parameters:
        - search_query: The query string to search for in Reddit posts
        """
        for post in self.reddit.subreddit('all').search(search_query, limit=self.search_limit, time_filter=self.time_filter, sort=self.sort_method):
            if post.is_self:  # Exclude posts that only contain a link to an image or video
                self.result_queue.put(post)

        for i in range(self.num_threads):
            self.result_queue.put(None)

    def save_data(self, csv_file):
        """
        Save the scraped data to a CSV file.

        Parameters:
        - csv_file: The name of the CSV file to save the data
        """
        with open(csv_file, mode='w', newline='', encoding='utf-8') as f:
            fieldnames = ['subreddit', 'username', 'url', 'content', 'upvotes', 'date']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for result_dict in self.scrape_data():
                writer.writerow(result_dict)
                print(f'{len(self.processed_ids)} posts found so far...')

    def run(self, search_query, csv_file):
        """
        Run the Reddit scraper to fetch and save data.

        Parameters:
        - search_query: The query string to search for in Reddit posts
        - csv_file: The name of the CSV file to save the data
        """
        threads = []
        for i in range(self.num_threads):
            t = threading.Thread(target=self.fetch_data, args=(search_query,))
            t.start()
            threads.append(t)

        self.save_data(csv_file)

        for t in threads:
            t.join()

