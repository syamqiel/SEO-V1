import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Fungsi untuk memvalidasi URL
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

# Fungsi untuk menormalkan target domain
def normalize_target_domain(target_domain):
    if not target_domain.startswith(('http://', 'https://')):
        target_domain = 'http://' + target_domain
    return target_domain

# Fungsi untuk memeriksa backlink
def check_backlinks(links, target_domain):
    results = []
    redirect_count = 0
    invalid_count = 0

    # Normalisasi target domain
    target_domain = normalize_target_domain(target_domain)
    parsed_target = urlparse(target_domain)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    for link in links:
        link = link.strip()
        if not is_valid_url(link):
            results.append((link, False))
            invalid_count += 1
            continue

        try:
            response = requests.get(link, headers=headers, allow_redirects=False, timeout=30)

            # Cek apakah ada pengalihan
            while response.status_code in (301, 302):
                redirect_url = response.headers.get('Location')
                if redirect_url:
                    print(f"Redirecting to: {redirect_url}")  # Log pengalihan
                    response = requests.get(redirect_url, headers=headers, allow_redirects=False, timeout=30)
                else:
                    break  # Jika tidak ada 'Location', hentikan loop

            final_url = response.url
            
            # Cek apakah target domain ditemukan di URL final
            if parsed_target.netloc in urlparse(final_url).netloc:
                results.append((link, True))
                redirect_count += 1
            else:
                # Parsing HTML dengan BeautifulSoup untuk cek backlink di konten halaman
                soup = BeautifulSoup(response.text, 'html.parser')
                if parsed_target.netloc in soup.get_text():
                    results.append((link, True))
                    redirect_count += 1
                else:
                    results.append((link, False))
                    invalid_count += 1
        except requests.RequestException as e:
            print(f"Request error for {link}: {e}")  # Log error request
            results.append((link, False))
            invalid_count += 1
        except Exception as e:
            print(f"Error for {link}: {e}")  # Log error umum
            results.append((link, False))
            invalid_count += 1

    # Cetak hasil statistik ke konsol
    print(f"Total valid links redirecting to {target_domain}: {redirect_count}")
    print(f"Total invalid links: {invalid_count}")
    print(f"Total links processed: {len(links)}")

    return results, redirect_count, invalid_count
