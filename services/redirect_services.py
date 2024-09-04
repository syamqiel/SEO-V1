import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def check_backlinks(links, target_domain):
    results = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    for link in links:
        link = link.strip()
        if not is_valid_url(link):
            results.append((link, False))
            continue

        try:
            response = requests.get(link, headers=headers, allow_redirects=True, timeout=30)
            final_url = response.url

            # Cek apakah target domain ditemukan di URL final
            if target_domain in urlparse(final_url).netloc:
                results.append((link, True))
            else:
                # Parsing HTML dengan BeautifulSoup untuk cek backlink di konten halaman
                soup = BeautifulSoup(response.text, 'html.parser')
                if target_domain in soup.get_text():
                    results.append((link, True))
                else:
                    results.append((link, False))
        except requests.RequestException as e:
            results.append((link, False))
        except Exception as e:
            results.append((link, False))

    return results
