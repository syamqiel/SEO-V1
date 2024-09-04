import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def check_redirect(url, target_domain):
    try:
        response = requests.get(url, allow_redirects=True, timeout=30)
        final_url = response.url
        
        # Cek apakah final URL mengarah ke target domain
        if target_domain in urlparse(final_url).netloc:
            return True
        else:
            # Periksa apakah konten di halaman memiliki referensi ke target domain
            soup = BeautifulSoup(response.text, 'html.parser')
            if target_domain in soup.get_text():
                return True
            return False
    except requests.RequestException as e:
        return False
