import requests


PING_SERVICES = [
    {
        "name": "Ping-O-Matic",
        "url": "https://pingomatic.com/ping/",
        "method": "POST",
        "params": ["title", "blogurl", "rssurl", "chk_services[]"]
    },
    {
        "name": "Twingly",
        "url": "https://rpc.twingly.com/ping/",
        "method": "POST",
        "params": ["url"]
    },
    # Tambahkan lebih banyak layanan ping di sini
]

def ping_all_services(url, category):
    results = []
    for service in PING_SERVICES:
        data = {}
        if "blogurl" in service['params']:
            data['blogurl'] = url
        if "chk_services[]" in service['params']:
            data['chk_services[]'] = "all"
        if "sitemap" in service['params']:
            data['sitemap'] = url
        if "category" in service['params']:
            data['category'] = category

        # Mengirim ping
        try:
            if service['method'] == 'POST':
                response = requests.post(service['url'], data=data)
            elif service['method'] == 'GET':
                response = requests.get(service['url'], params=data)

            if response.status_code == 200:
                results.append((service['name'], "success"))
            else:
                results.append((service['name'], f"failed: HTTP {response.status_code}"))
        except Exception as e:
            results.append((service['name'], f"failed: {str(e)}"))
    
    return results
