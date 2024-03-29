import requests
from bs4 import BeautifulSoup
import json

# Скрапінг цитат та інформації про авторів з сайту
def scrape_quotes_and_authors():
    url = "http://quotes.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    quotes = []
    authors = {}
    
    for quote in soup.find_all('div', class_='quote'):
        text = quote.find('span', class_='text').get_text(strip=True)
        author = quote.find('small', class_='author').get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote.find_all('a', class_='tag')]
        
        quotes.append({
            "quote": text,
            "author": author,
            "tags": tags
        })
        
        if author not in authors:
            authors[author] = scrape_author_info(url + f"author/{author.replace(' ', '-')}")
        
    return quotes, authors.values()

# Скрапінг інформації про автора
def scrape_author_info(author_url):
    response = requests.get(author_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    birth_date = soup.find('span', class_='author-born-date').get_text(strip=True)
    birth_location = soup.find('span', class_='author-born-location').get_text(strip=True)
    description = soup.find('div', class_='author-description').get_text(strip=True)
    
    return {
        "fullname": author_url.split("/")[-1].replace("-", " ").title(),
        "born_date": birth_date,
        "born_location": birth_location,
        "description": description
    }

# Збереження даних у JSON файли
def save_to_json(data, filename):
    with open(filename, 'w', encoding = 'utf-8') as file:
        json.dump(list(data), file, ensure_ascii=False, indent=2)

# Отримання цитат та інформації про авторів
quotes, authors = scrape_quotes_and_authors()

# Збереження цитат у quotes.json
save_to_json(quotes, 'quotes.json')

# Збереження інформації про авторів у authors.json
save_to_json(authors, 'authors.json')
