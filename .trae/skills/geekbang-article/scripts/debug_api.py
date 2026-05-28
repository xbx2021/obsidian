import urllib.request
import json
import sys

def test_api(url, cookie):
    article_id = url.split('/')[-1]
    api_url = "https://time.geekbang.org/serv/v1/article"
    
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Cookie": cookie,
        "Origin": "https://time.geekbang.org",
        "Referer": f"https://time.geekbang.org/column/article/{article_id}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
        "X-GEEK-REQ-ID": f"{article_id}@1@web"
    }
    
    data = json.dumps({
        "id": article_id,
        "include_neighbors": True,
        "is_freelyread": True
    }).encode('utf-8')
    
    req = urllib.request.Request(api_url, data=data, headers=headers, method='POST')
    with urllib.request.urlopen(req) as response:
        response_text = response.read().decode('utf-8')
        json_data = json.loads(response_text)
        
        print("Keys in data:", list(json_data.get('data', {}).keys()))
        
        if 'article_content' in json_data.get('data', {}):
            content = json_data['data']['article_content']
            print(f"\nArticle content length: {len(content)}")
            print(f"\nFirst 2000 chars:\n{content[:2000]}")
            print(f"\nLast 1000 chars:\n{content[-1000:]}")
            
        if 'article_title' in json_data.get('data', {}):
            print(f"\nArticle title: {json_data['data']['article_title']}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python debug_api.py <url> <cookie>")
        sys.exit(1)
    
    url = sys.argv[1]
    cookie = sys.argv[2]
    test_api(url, cookie)
