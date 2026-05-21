import urllib.request
import json
import re
import sys

def html_to_markdown(html_content):
    result = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)
    result = re.sub(r'<h1>(.*?)</h1>', r'\n# \1\n', result, flags=re.DOTALL)
    result = re.sub(r'<h2>(.*?)</h2>', r'\n## \1\n', result, flags=re.DOTALL)
    result = re.sub(r'<h3>(.*?)</h3>', r'\n### \1\n', result, flags=re.DOTALL)
    result = re.sub(r'<strong>(.*?)</strong>', r'**\1**', result, flags=re.DOTALL)
    result = re.sub(r'<b>(.*?)</b>', r'**\1**', result, flags=re.DOTALL)
    result = re.sub(r'<li>\s*<p>(.*?)</p>\s*</li>', r'\n- \1', result, flags=re.DOTALL)
    result = re.sub(r'<li>(.*?)</li>', r'\n- \1', result, flags=re.DOTALL)
    result = re.sub(r'<p>(.*?)</p>', r'\1\n\n', result, flags=re.DOTALL)
    result = re.sub(r'</?(ul|ol)>', '', result)
    result = re.sub(r'</?br\s*/?>', '\n', result)
    
    result = re.sub(r'<a\s+([^>]*?)href\s*=\s*["\']([^"\']*)["\']([^>]*?)>(.*?)</a>', r'[\4](\2)', result, flags=re.DOTALL)
    
    result = re.sub(r'<[^>]+>', '', result)
    result = re.sub(r'\n{3,}', '\n\n', result)
    result = re.sub(r'-\s+', '- ', result)
    return result.strip()

def extract_article(url, cookie):
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
            
            markdown_content = html_to_markdown(article_content)
            
            filename = article_title.replace('|', '-').replace(':', '-').replace('\\', '-').replace('/', '-').strip()
            filename = f"{filename}.md"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            print(f"Markdown file saved as: {filename}")
            return True
        else:
            error_msg = json_data.get('error', {}).get('msg', 'Unknown error')
            print(f"Error: {error_msg}")
            if 'permission' in error_msg.lower() or '权限' in error_msg:
                print("Cookie may be expired or invalid. Please provide a new cookie.")
            return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python geekbang_article.py <url> <cookie>")
        sys.exit(1)
    
    url = sys.argv[1]
    cookie = sys.argv[2]
    extract_article(url, cookie)
