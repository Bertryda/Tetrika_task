import requests
from bs4 import BeautifulSoup
import csv
from collections import defaultdict
import re

def get_animal_count_by_letter():
    base_url = "https://ru.wikipedia.org"
    start_url = base_url + "/wiki/Категория:Животные_по_алфавиту"
    
    letter_counts = defaultdict(int)
    russian_letters = set('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')
    
    # Множество уникальных значений
    processed_titles = set()
    pages_to_process = [start_url]
    processed_pages = set()
    
    while pages_to_process:
        current_url = pages_to_process.pop(0)
        
        if current_url in processed_pages:
            continue
        
        try:
            response = requests.get(current_url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            continue
            
        soup = BeautifulSoup(response.text, 'html.parser')
        category_div = soup.find('div', id='mw-pages')
        
        if not category_div:
            continue
            
        # Все элементы в группе ссылок
        link_groups = category_div.find_all(['ul', 'div'], class_=lambda x: x in ['mw-category-group', None])
        
        for group in link_groups:
            for link in group.find_all('a'):
                title = link.get('title', '')
                if not title or title in processed_titles:
                    continue
                
                processed_titles.add(title)
                
                if title.startswith('Категория:'):
                    subcategory_url = base_url + link.get('href')
                    if subcategory_url not in processed_pages:
                        pages_to_process.append(subcategory_url)
                else:
                    first_char = title[0].upper()
                    if first_char in russian_letters:
                        letter_counts[first_char] += 1
        
        processed_pages.add(current_url)
        
        next_page_link = soup.find('a', text=re.compile(r'Следующая страница'))
        if next_page_link:
            next_page_url = base_url + next_page_link.get('href')
            if next_page_url not in processed_pages:
                pages_to_process.append(next_page_url)
    
    return letter_counts

def save_to_csv(letter_counts, filename='beasts.csv'):
    sorted_counts = sorted(letter_counts.items(), key=lambda x: x[0])
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for letter, count in sorted_counts:
            writer.writerow([letter, count])
    

if __name__ == '__main__':
    counts = get_animal_count_by_letter()
    save_to_csv(counts)