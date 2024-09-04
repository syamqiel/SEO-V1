import requests
from bs4 import BeautifulSoup

def check_comments(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Contoh elemen untuk mencari komentar
            comment_elements = ['comment', 'respond', 'reply']
            for element in comment_elements:
                comment_sections = soup.find_all(class_=element) + soup.find_all(id=element)
                for section in comment_sections:
                    # Periksa keberadaan tag HTML seperti <a href="">
                    if section.find_all(['a', 'script', 'img']):
                        return False  # HTML tidak diperbolehkan
            return True
        return False
    except requests.exceptions.RequestException as e:
        return False
