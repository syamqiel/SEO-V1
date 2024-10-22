import requests
from bs4 import BeautifulSoup
from langdetect import detect, DetectorFactory

# Mengatur seed untuk konsistensi hasil deteksi bahasa
DetectorFactory.seed = 0

def check_comments(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Deteksi bahasa konten
            language = detect(response.text)

            # Elemen komentar berdasarkan bahasa
            comment_elements = {
                'en': ['comment', 'respond', 'reply', 'discussion', 'comments', 'leave a reply', 'add a comment', 'post a comment'],
                'es': ['comentarios', 'respuesta', 'dejar un comentario', 'agregar un comentario'],
                'ar': ['تعليقات', 'ردود', 'أضف تعليقًا', 'اكتب تعليقًا'],
                'ja': ['コメント', '返信', 'コメントを追加', '返信を書く'],
                'zh': ['评论', '回复', '添加评论', '写评论'],
                'id': ['komentar', 'balasan', 'tulis komentar', 'tambahkan komentar'],
            }.get(language, ['comment', 'respond', 'reply', 'discussion', 'comments'])  # default ke elemen umum

            # Memeriksa elemen komentar
            for element in comment_elements:
                comment_sections = soup.find_all(class_=element) + soup.find_all(id=element)
                for section in comment_sections:
                    # Periksa keberadaan tag HTML seperti <a href="">, <script>, <iframe>, <embed>
                    if section.find_all(['a', 'script', 'iframe', 'embed', 'object']):
                        return {
                            'comments_allowed': True,
                            'backlink_allowed': False
                        }  # HTML tidak diperbolehkan

            # Mencari form komentar di halaman
            comment_form = soup.find('form', {'id': 'commentform'})  # Contoh, tergantung situs
            if comment_form:
                # Mencari elemen textarea di form komentar
                textarea = comment_form.find('textarea') or comment_form.find('input', {'type': 'text'})

                # Memeriksa apakah ada informasi tentang diperbolehkannya link (<a>)
                if textarea:
                    # Cari keterangan di dekat formulir komentar yang mungkin menyebutkan aturan HTML
                    html_allowed = 'HTML' in comment_form.get_text()

                    backlink_allowed = 'a href' in comment_form.get_text().lower() or html_allowed

                    return {
                        'comments_allowed': True,
                        'backlink_allowed': backlink_allowed
                    }

            return {'comments_allowed': False, 'backlink_allowed': False}
        
        return {'comments_allowed': False, 'backlink_allowed': False}
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return {'comments_allowed': False, 'backlink_allowed': False}

    except Exception as e:
        print(f"General error for {url}: {e}")
        return {'comments_allowed': False, 'backlink_allowed': False}
