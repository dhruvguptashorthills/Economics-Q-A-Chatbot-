import requests
from bs4 import BeautifulSoup
import json
import os

class Scraper:
    def __init__(self, text_folder='articles'):
        self.text_folder = text_folder
        if not os.path.exists(self.text_folder):
            os.makedirs(self.text_folder)

    def extract_wikipedia_data(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find('h1', {'id': 'firstHeading'}).text
            paragraphs = soup.find_all('p')
            content = '\n'.join([para.text for para in paragraphs])
            return title, content
        else:
            return None, None

    def save_article_to_file(self, title, content):
        if not os.path.exists(self.text_folder):
            os.makedirs(self.text_folder)
        filename = os.path.join(self.text_folder, f"{title.replace(' ', '_')}.txt")
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(f"Title: {title}\n\n")
            file.write(content)
        return filename

    def extract(self, urls):
        for url in urls:
            title, content = self.extract_wikipedia_data(url)
            if title and content:
                self.save_article_to_file(title, content)
                print(title, "Article extracted and saved")

    def txt_files_to_json(self, output_file):
        data = []
        try:
            for file_name in os.listdir(self.text_folder):
                if file_name.endswith(".txt"):
                    file_path = os.path.join(self.text_folder, file_name)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        data.append({
                            "title": file_name,
                            "content": content
                        })

            with open(output_file, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)

            print(f"Data successfully written to {output_file}")

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    with open('Scraper/list.txt', 'r', encoding='utf-8') as file:
        urls = json.load(file)
    scraper = Scraper()
    scraper.extract(urls)
    output_file = 'Data/combined_Raw_Data.json'
    scraper.txt_files_to_json(output_file)