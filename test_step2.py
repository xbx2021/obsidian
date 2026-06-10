import urllib.request
import json
import re

# Import the actual script
import sys
sys.path.append(r'd:\obsidian_github\obsidian\.trae\skills\geekbang-article\scripts')

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
    idx = content.find('<pre><code class="language-yaml">')
    if idx > 0:
        html_snippet = content[idx:idx+800]
        print('Original HTML snippet:')
        print(html_snippet[:500])
        print('\n---\n')
        
        # Simulate Step 2
        result = html_snippet
        result = result.replace('&lt;', '\x00LT\x00')
        result = result.replace('&gt;', '\x00GT\x00')
        result = result.replace('&nbsp;', '\x00NBSP\x00')
        
        print('After Step 2 (protection):')
        print(result[:500])
        print('\n---\n')
        
        # Check if &nbsp; was replaced
        if '&nbsp;' in result:
            print('ERROR: &nbsp; still exists after Step 2!')
        elif '\x00NBSP\x00' in result:
            print('OK: &nbsp; was replaced with \\x00NBSP\\x00')
        else:
            print('WARNING: No &nbsp; found in the snippet')