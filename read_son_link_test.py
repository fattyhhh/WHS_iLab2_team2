import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_all_sublinks(url, max_depth=None, visited=None):
    """
    Recursively retrieve all sublinks from a webpage.

    Args:
        url (str): The starting URL.
        max_depth (int, optional): Maximum depth of recursion. None means no limit.
        visited (set, optional): Set of visited URLs to avoid duplicates.

    Returns:
        set: A set of all sublinks found.
    """
    if visited is None:
        visited = set()

    if max_depth is not None and max_depth <= 0:
        return set()

    try:
        response = requests.get(url)
        if response.status_code == 200:
            visited.add(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            sublinks = set()

            for link in soup.find_all('a', href=True):
                absolute_link = urljoin(url, link['href'])
                if absolute_link not in visited:
                    sublinks.add(absolute_link)
                    sublinks.update(get_all_sublinks(absolute_link, max_depth - 1, visited))

            return sublinks
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return set()

# Example usage:
start_url = 'http://nobullconstructions.com.au'  # Replace with your desired starting URL
all_sublinks = get_all_sublinks(start_url, max_depth=1)  # Adjust the maximum depth as needed

for link in all_sublinks:
    print(link)
