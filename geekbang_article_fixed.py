import urllib.request
import json
import re
import sys
import html

def detect_language(code):
    """Detect programming language from code content."""
    code_clean = code.strip()
    if re.search(r'\bstd::\b|\bclass\s+\w+\s*\{|\bpublic:\b|\bprivate:\b|\b~[A-Za-z_]+\s*\(|std::mutex', code_clean):
        return 'cpp'
    elif re.search(r'\bfunc\s+\w+\s*\(|\bpackage\s+\w+|\bimport\s+\(|bdefer\s+|\bnil\b|\bmake\s*\(', code_clean):
        return 'go'
    elif re.search(r'\b#include\s*<|\bmalloc\s*\(|\bfree\s*\(|\bfprintf\s*\(|\bFILE\s*\*|\berrno\b', code_clean):
        return 'c'
    elif re.search(r'\bpublic\s+class\s+|\bpublic\s+static\s+void\s+main|\bSystem\.out\.', code_clean):
        return 'java'
    elif re.search(r'\bdef\s+\w+\s*\(|\bimport\s+\w+|\bprint\s*\(|\bTrue\b|\bFalse\b|\bNone\b', code_clean):
        return 'python'
    else:
        return ''

def html_to_markdown(html_content):
    """Convert HTML content to Markdown format."""
    result = html_content

    # Step 1: Remove HTML comments
    result = re.sub(r'<!--.*?-->', '', result, flags=re.DOTALL)

    # Step 2: Protect &lt; and &gt; in text (not in actual HTML tags)
    # Replace them with placeholders before unescaping
    # This prevents <object> in ArrayList<object> from being treated as HTML tag
    result = result.replace('&lt;', '\x00LT\x00')
    result = result.replace('&gt;', '\x00GT\x00')

    # Step 3: Process code blocks FIRST
    def process_code_block(match):
        code = match.group(1)
        # Restore angle brackets in code blocks
        code = code.replace('\x00LT\x00', '<').replace('\x00GT\x00', '>')
        lang = detect_language(code)
        return f'\n``` {lang}\n{code}\n```\n'

    # Handle <pre><code>...</code></pre> blocks
    result = re.sub(r'<pre\s*[^>]*>\s*<code\s*[^>]*>(.*?)</code>\s*</pre>',
                    process_code_block, result, flags=re.DOTALL)

    # Handle <pre>...</pre> blocks (without inner <code>)
    result = re.sub(r'<pre\s*[^>]*>(.*?)</pre>',
                    process_code_block, result, flags=re.DOTALL)

    # Step 4: Handle inline <code>...</code>
    code_blocks = []
    def save_code_block(match):
        code_blocks.append(match.group(0))
        return f"\x00CODEBLOCK{len(code_blocks)-1}\x00"

    result = re.sub(r'\n``` [^\n]*\n.*?\n```\n', save_code_block, result, flags=re.DOTALL)

    # Process inline code
    def process_inline_code(match):
        code = match.group(1)
        # Restore angle brackets in inline code
        code = code.replace('\x00LT\x00', '<').replace('\x00GT\x00', '>')
        return f'`{code}`'

    result = re.sub(r'<code\s*[^>]*>(.*?)</code>',
                    process_inline_code, result, flags=re.DOTALL)

    # Step 5: Process headings
    result = re.sub(r'<h1[^>]*>(.*?)</h1>', r'\n# \1\n', result, flags=re.DOTALL)
    result = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\n## \1\n', result, flags=re.DOTALL)
    result = re.sub(r'<h3[^>]*>(.*?)</h3>', r'\n### \1\n', result, flags=re.DOTALL)
    result = re.sub(r'<h4[^>]*>(.*?)</h4>', r'\n#### \1\n', result, flags=re.DOTALL)

    # Step 6: Process formatting
    result = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', result, flags=re.DOTALL)
    result = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', result, flags=re.DOTALL)
    result = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', result, flags=re.DOTALL)
    result = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', result, flags=re.DOTALL)
    result = re.sub(r'<span[^>]*>(.*?)</span>', r'\1', result, flags=re.DOTALL)

    # Step 7: Process lists
    result = re.sub(r'<li>\s*<p>(.*?)</p>\s*</li>', r'\n- \1', result, flags=re.DOTALL)
    result = re.sub(r'<li>(.*?)</li>', r'\n- \1', result, flags=re.DOTALL)
    result = re.sub(r'</?(ul|ol)\s*[^>]*>', '', result, flags=re.DOTALL)

    # Step 8: Process paragraphs
    result = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', result, flags=re.DOTALL)

    # Step 9: Process line breaks
    result = re.sub(r'</?br\s*/?>', '\n', result, flags=re.DOTALL)

    # Step 10: Process images
    result = re.sub(r'<img\s+[^>]*?src\s*=\s*["\']([^"\']+)["\'][^>]*?alt\s*=\s*["\']([^"\']*)["\'][^>]*?>',
                    r'![\2](\1)', result, flags=re.DOTALL)
    result = re.sub(r'<img\s+[^>]*?alt\s*=\s*["\']([^"\']*)["\'][^>]*?src\s*=\s*["\']([^"\']+)["\'][^>]*?>',
                    r'![\1](\2)', result, flags=re.DOTALL)
    result = re.sub(r'<img\s+[^>]*?src\s*=\s*["\']([^"\']+)["\'][^>]*?>',
                    r'![](\1)', result, flags=re.DOTALL)

    # Step 11: Process links
    result = re.sub(r'<a\s+[^>]*?href\s*=\s*["\']([^"\']*)["\'][^>]*?>(.*?)</a>',
                    r'[\2](\1)', result, flags=re.DOTALL)

    # Step 12: Remove any remaining HTML tags
    result = re.sub(r'<[^>]+>', '', result)

    # Step 13: Restore angle brackets
    result = result.replace('\x00LT\x00', '<').replace('\x00GT\x00', '>')

    # Step 14: Restore code blocks
    def restore_code_block(match):
        idx = int(match.group(1))
        return code_blocks[idx] if idx < len(code_blocks) else match.group(0)

    result = re.sub(r'\x00CODEBLOCK(\d+)\x00', restore_code_block, result)

    # Step 15: Clean up whitespace
    result = re.sub(r'\n{3,}', '\n\n', result)
    result = re.sub(r'-\s+', '- ', result)

    return result.strip()

def extract_article(url, cookie):
    """Extract article from GeekBang and save as Markdown."""
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

            # Clean filename
            filename = article_title.replace('|', ' ').replace(':', ' ').replace('\\', ' ').replace('/', ' ').strip()
            filename = re.sub(r'^(\d+)\s+', r'\1 ', filename)
            filename = f"{filename}.md"

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(markdown_content)

            print(f"Markdown file saved as: {filename}")
            print(f"Content length: {len(markdown_content)} chars")
            return True
        else:
            error_msg = json_data.get('error', {}).get('msg', 'Unknown error')
            print(f"Error: {error_msg}")
            if 'permission' in error_msg.lower() or '权限' in error_msg:
                print("Cookie may be expired or invalid. Please provide a new cookie.")
            return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python geekbang_article_fixed.py <url> <cookie>")
        sys.exit(1)

    url = sys.argv[1]
    cookie = sys.argv[2]
    extract_article(url, cookie)
