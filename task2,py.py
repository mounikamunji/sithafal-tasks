import requests
from bs4 import BeautifulSoup
import logging
from colorama import Fore, Style, init


init(autoreset=True)


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_content(url):
    """Fetches the content of a website and returns the text."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text(separator=' ', strip=True)
    except requests.exceptions.SSLError as ssl_err:
        logging.error(f"SSL error occurred: {ssl_err}")
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Request error occurred: {req_err}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def search_content(query, data):
    """Searches for relevant content based on the user's query."""
    return [(url, content) for url, content in data.items() if query.lower() in content.lower()]

def display_results(results):
    """Displays the search results in a formatted manner."""
    if results:
        print(Fore.GREEN + "\nResults found:" + Style.RESET_ALL)
        for url, content in results:
            print(Fore.CYAN + f"\nFrom {url}:" + Style.RESET_ALL)
            print(Fore.YELLOW + f"{content[:500]}..." + Style.RESET_ALL)  
    else:
        print(Fore.RED + "No results found for your query." + Style.RESET_ALL)

def main():
   
    urls = [
        "https://www.uchicago.edu/",
        "https://www.washington.edu/",
        "https://www.stanford.edu/",
        "https://und.edu/"
    ]

   
    scraped_data = {}
    for url in urls:
        content = fetch_content(url)
        if content:
            logging.info(f"Successfully scraped content from {url}")
            scraped_data[url] = content

  
    user_query = input(Fore.MAGENTA + "Enter your query: " + Style.RESET_ALL)
    results = search_content(user_query, scraped_data)

   
    display_results(results)

 
    print(Fore.BLUE + "\nLinks to the websites:" + Style.RESET_ALL)
    for url in urls:
        print(Fore.BLUE + url + Style.RESET_ALL)

if __name__ == "__main__":
    main()
