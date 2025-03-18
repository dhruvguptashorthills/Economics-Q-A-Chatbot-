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

def txt_files_to_json(output_file,folder_path="articles"):
    data = []

    try:
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".txt"):
                file_path = os.path.join(folder_path, file_name)
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
    with open('Scrapper/list.txt', 'r', encoding='utf-8') as file:
        urls = json.load(file)
    extract(urls)
    output_file = 'Data/combined_Raw_Data.json'   
    txt_files_to_json(output_file)