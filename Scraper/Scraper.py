import requests
from bs4 import BeautifulSoup
import json
import os

def extract_wikipedia_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('h1', {'id': 'firstHeading'}).text
        paragraphs = soup.find_all('p')
        content = '\n'.join([para.text for para in paragraphs])
        return title, content
    else:
        return None, None

def save_article_to_file(title, content, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    filename = os.path.join(folder, f"{title.replace(' ', '_')}.txt")
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"Title: {title}\n\n")
        file.write(content)
    return filename

def extract(urls):
    text_folder = 'articles'

    if not os.path.exists(text_folder):
        os.makedirs(text_folder)

    for url in urls:
        title, content = extract_wikipedia_data(url)
        if title and content:
            save_article_to_file(title, content, text_folder)
            print(title,"Article extracted and saved")



# Example usage
if __name__ == "__main__":
    with open('Scrapper/list.txt', 'r', encoding='utf-8') as file:
        urls = json.load(file)
    extract(urls)
