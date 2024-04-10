import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_user_input():
    book_name = input("Enter book name: ")
    author = input("Enter author name: ")
    return book_name, author

def get_data(book_name, author):
    url = f'https://www.amazon.in/s?k={book_name}+by+{author}&ref=nb_sb_noss_2'
    headers = {
        "User-Agent": "Your User Agent",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT": "1",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1"
    }

    r = requests.get(url, headers=headers)
    content = r.content
    soup = BeautifulSoup(content, 'html.parser')

    alls = []
    for d in soup.findAll('div', attrs={'class': 'a-section a-spacing-medium'}):
        name = d.find('span', attrs={'class': 'a-size-medium a-color-base a-text-normal'})
        book_name = name.text.strip() if name else 'Unknown Product'

        author = d.find('span', attrs={'class': 'a-size-base'})
        author_name = author.text.strip() if author else 'Unknown Author'

        rating = d.find('span', attrs={'class': 'a-icon-alt'})
        rating_value = rating.text.strip() if rating else 'No Rating'

        price = d.find('span', attrs={'class': 'a-price-whole'})
        price_value = price.text.strip() if price else 'Price Not Available'

        print(f"Book: {book_name}, Author: {author_name}, Rating: {rating_value}, Price: {price_value}")

        alls.append([book_name, author_name, rating_value, price_value])

    return alls

book_name, author = get_user_input()
results = get_data(book_name, author)

df = pd.DataFrame(results, columns=['Book Name', 'Author', 'Rating', 'Price'])
df.to_csv('amazon_products.csv', index=False, encoding='utf-8')

df = pd.read_csv("amazon_products.csv")
print("Shape of DataFrame:", df.shape)
print("First few rows of DataFrame:")
print(df.head())
print("Data types of each column:")
print(df.dtypes)
