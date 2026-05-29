import urllib.request
import json
import re
import html

def debug_extract_article(url, cookie):
    """Debug: Extract article from GeekBang and show raw data."""
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
        
        print("=== API Response Keys ===")
        print(json_data.keys())
        
        if 'data' in json_data:
            print("\n=== Data Keys ===")
            print(json_data['data'].keys())
            
            article_title = json_data['data'].get('article_title', 'N/A')
            article_content = json_data['data'].get('article_content', '')
            
            print(f"\n=== Article Title ===")
            print(article_title)
            
            print(f"\n=== Article Content Length ===")
            print(f"HTML content length: {len(article_content)} chars")
            
            # Save raw HTML for inspection
            with open('debug_raw.html', 'w', encoding='utf-8') as f:
                f.write(article_content)
            print("\nRaw HTML saved to: debug_raw.html")
            
            # Check for specific sections
            if '数组' in article_content:
                print("\n✓ '数组' found in content")
            if '课后思考' in article_content:
                print("✓ '课后思考' found in content")
            if '内容小结' in article_content:
                print("✓ '内容小结' found in content")
            if '解答开篇' in article_content:
                print("✓ '解答开篇' found in content")
                
        else:
            error_msg = json_data.get('error', {}).get('msg', 'Unknown error')
            print(f"Error: {error_msg}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python debug_article.py <url> <cookie>")
        sys.exit(1)
    
    url = sys.argv[1]
    cookie = sys.argv[2]
    debug_extract_article(url, cookie)
