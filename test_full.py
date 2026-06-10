import urllib.request
import json
import re
import sys

# Import the actual script
sys.path.append(r'd:\obsidian_github\obsidian\.trae\skills\geekbang-article\scripts')
from geekbang_article import html_to_markdown

article_id = '774323'
api_url = 'https://time.geekbang.org/serv/v1/article'

cookie_file = r'd:\obsidian_github\obsidian\.trae\skills\geekbang-article\cookie'
with open(cookie_file, 'r', encoding='utf-8') as f:
    cookie = f.read().strip()

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json',
    'Cookie': cookie,
    'Origin': 'https://time.geekbang.org',
    'Referer': f'https://time.geekbang.org/column/article/{article_id}',
    'User-Agent': 'Mozilla/5.0',
    'X-GEEK-REQ-ID': f'{article_id}@1@web'
}

data = json.dumps({'id': article_id, 'include_neighbors': True, 'is_freelyread': True}).encode('utf-8')
req = urllib.request.Request(api_url, data=data, headers=headers, method='POST')
with urllib.request.urlopen(req) as response:
    content = json.loads(response.read().decode('utf-8'))['data']['article_content']
    
    # Find the YAML code block
    idx = content.find('addons:')
    if idx > 0:
        html_snippet = content[idx-50:idx+500]
        print('HTML snippet:')
        print(html_snippet[:500])
        print('\n---\n')
        
        # Test html_to_markdown
        markdown = html_to_markdown(html_snippet)
        print('Markdown result:')
        print(markdown[:500])
