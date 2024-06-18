import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

def extract_article_text(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.find('title').get_text().strip()                   #Extract Title

        article_text = ""
        for paragraph in soup.find_all('p'):
            article_text += paragraph.get_text() + "\n"                 #Extract article text

        article_text = re.sub(r'\n+', '\n', article_text)               #Remove extra newlines
        article_text = re.sub(r'\s+', ' ', article_text)                #Remove extra whitespaces

        return title, article_text

    except Exception as e:
        print(f"Error extracting text from {url}: {e}")
        return None, None

def main():
    input_file = "Articles.xlsx"
    output_folder = "Extracted_Articles/"

    df = pd.read_excel(input_file)

    for _ , row in df.iterrows():
        url_id = row['URL_ID']
        url = row['URL']
 
        title, article_text = extract_article_text(url)                 #Extract article text
        
        if title and article_text:
            with open(output_folder + f"{url_id}.txt", 'w', encoding='utf-8') as f:             #Writing into file
                f.write(f"Title: {title}\n\n")
                f.write(article_text)
            print(f"Article extracted and saved: {url_id}.txt")
        else:
            print(f"Failed to extract article from {url}")

if __name__ == "__main__":
    main()
