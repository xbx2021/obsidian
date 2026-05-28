import urllib.request
import json
import sys
import re
import html

def extract_and_debug(url, cookie):
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
        
        if 'data' in json_data and 'article_content' in json_data['data']:
            article_content = json_data['data']['article_content']
            article_title = json_data['data'].get('article_title', article_id)
            
            print(f"Article title: {article_title}")
            print(f"Original HTML content length: {len(article_content)}")
            
            # Save original HTML
            with open('original_content.html', 'w', encoding='utf-8') as f:
                f.write(article_content)
            
            # Test each step
            result = article_content
            
            # Step 1: Remove comments
            result = re.sub(r'<!--.*?-->', '', result, flags=re.DOTALL)
            print(f"After removing comments: {len(result)}")
            
            # Step 2: Unescape
            result = html.unescape(result)
            print(f"After html.unescape: {len(result)}")
            
            # Step 3: Process code blocks
            def process_code_block(match):
                code = match.group(1)
                return f'\n```\n{code}\n```\n'
            
            result = re.sub(r'<pre\s*[^>]*><code\s*[^>]*>(.*?)</code></pre>', process_code_block, result, flags=re.DOTALL)
            print(f"After <pre><code> blocks: {len(result)}")
            
            result = re.sub(r'<pre\s*[^>]*>(.*?)</pre>', process_code_block, result, flags=re.DOTALL)
            print(f"After <pre> blocks: {len(result)}")
            
            # Step 4: Process h2 tags
            result = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\n## \1\n', result, flags=re.DOTALL)
            print(f"After <h2> tags: {len(result)}")
            
            # Step 5: Process p tags
            result = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', result, flags=re.DOTALL)
            print(f"After <p> tags: {len(result)}")
            
            # Step 6: Remove remaining tags
            result = re.sub(r'<[^>]+>', '', result)
            print(f"After removing all tags: {len(result)}")
            
            # Step 7: Clean up
            result = re.sub(r'\n{3,}', '\n\n', result)
            result = result.strip()
            print(f"Final result: {len(result)}")
            
            with open('final_result.md', 'w', encoding='utf-8') as f:
                f.write(result)
            
            print("\n--- First 1000 chars of final result ---")
            print(result[:1000])
            
            return True
        else:
            error_msg = json_data.get('error', {}).get('msg', 'Unknown error')
            print(f"Error: {error_msg}")
            return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python debug_full.py <url> <cookie>")
        sys.exit(1)
    
    url = sys.argv[1]
    cookie = sys.argv[2]
    extract_and_debug(url, cookie)
