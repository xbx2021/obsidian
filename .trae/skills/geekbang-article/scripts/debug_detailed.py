import urllib.request
import json
import re
import html

def debug_html_processing(html_content):
    """Debug HTML processing step by step."""
    result = html_content
    
    print("=== Step 0: Original HTML (first 500 chars) ===")
    print(result[:500])
    print(f"Total length: {len(result)}")
    print()
    
    # Step 1: Remove HTML comments
    result = re.sub(r'<!--.*?-->', '', result, flags=re.DOTALL)
    print("=== Step 1: After removing HTML comments ===")
    print(f"Length: {len(result)}")
    
    # Check if 容器能否完全替代数组 is still there
    if '容器能否完全替代数组' in result:
        print("✓ '容器能否完全替代数组' found")
    else:
        print("✗ '容器能否完全替代数组' NOT found")
    print()
    
    # Step 2: Process code blocks
    def process_code_block(match):
        code = match.group(1)
        code = html.unescape(code)
        return f'\n```\n{code}\n```\n'
    
    result = re.sub(r'<pre\s*[^>]*>\s*<code\s*[^>]*>(.*?)</code>\s*</pre>', 
                    process_code_block, result, flags=re.DOTALL)
    result = re.sub(r'<pre\s*[^>]*>(.*?)</pre>', 
                    process_code_block, result, flags=re.DOTALL)
    
    print("=== Step 2: After processing code blocks ===")
    print(f"Length: {len(result)}")
    if '容器能否完全替代数组' in result:
        print("✓ '容器能否完全替代数组' found")
    else:
        print("✗ '容器能否完全替代数组' NOT found")
    print()
    
    # Step 3: Process inline code
    def process_inline_code(match):
        code = match.group(1)
        code = html.unescape(code)
        return f'`{code}`'
    
    result = re.sub(r'<code\s*[^>]*>(.*?)</code>', 
                    process_inline_code, result, flags=re.DOTALL)
    
    print("=== Step 3: After processing inline code ===")
    print(f"Length: {len(result)}")
    if '容器能否完全替代数组' in result:
        print("✓ '容器能否完全替代数组' found")
    else:
        print("✗ '容器能否完全替代数组' NOT found")
    print()
    
    # Step 4: Unescape HTML entities
    result_before_unescape = result
    result = html.unescape(result)
    
    print("=== Step 4: After unescaping HTML entities ===")
    print(f"Length: {len(result)}")
    if '容器能否完全替代数组' in result:
        print("✓ '容器能否完全替代数组' found")
    else:
        print("✗ '容器能否完全替代数组' NOT found")
    
    # Check for ArrayList pattern
    if 'ArrayList' in result:
        print("✓ 'ArrayList' found")
        # Find the context
        idx = result.find('ArrayList')
        print(f"Context: {result[idx:idx+100]}")
    else:
        print("✗ 'ArrayList' NOT found")
    print()
    
    # Check what happens around the problematic area
    if '<object>' in result:
        print("WARNING: '<object>' found in result after unescape!")
        idx = result.find('<object>')
        print(f"Context: {result[idx-50:idx+100]}")
    
    return result

def debug_extract_article(url, cookie):
    """Debug: Extract article from GeekBang."""
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
            debug_html_processing(article_content)
        else:
            error_msg = json_data.get('error', {}).get('msg', 'Unknown error')
            print(f"Error: {error_msg}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python debug_detailed.py <url> <cookie>")
        sys.exit(1)
    
    url = sys.argv[1]
    cookie = sys.argv[2]
    debug_extract_article(url, cookie)
