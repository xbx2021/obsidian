import urllib.request
import json
import re
import sys
import html
import os

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

def analyze_content_integrity(html_content, markdown_content):
    """
    Analyze and check content integrity between HTML and Markdown.
    Returns a dictionary with analysis results and warnings.
    """
    issues = {
        'warnings': [],
        'info': [],
        'html_headings': [],
        'markdown_headings': [],
        'html_length': len(html_content),
        'markdown_length': len(markdown_content),
        'conversion_ratio': 0,
        'is_complete': True
    }

    # Extract headings from HTML
    html_headings = re.findall(r'<h[1-4][^>]*>(.*?)</h[1-4]>', html_content, flags=re.DOTALL)
    issues['html_headings'] = [h.strip() for h in html_headings]

    # Extract headings from Markdown
    markdown_headings = re.findall(r'^#{1,4}\s+(.+)', markdown_content, flags=re.MULTILINE)
    issues['markdown_headings'] = [h.strip() for h in markdown_headings]

    # Calculate conversion ratio
    if len(html_content) > 0:
        issues['conversion_ratio'] = (len(markdown_content) / len(html_content)) * 100

    # Check heading count
    if len(html_headings) != len(markdown_headings):
        issues['warnings'].append(
            f"标题数量不一致：HTML中有 {len(html_headings)} 个标题，Markdown中有 {len(markdown_headings)} 个标题"
        )
        issues['is_complete'] = False

    # Check for missing headings
    html_headings_set = set([h.strip() for h in html_headings])
    markdown_headings_set = set([h.strip() for h in markdown_headings])
    missing_headings = html_headings_set - markdown_headings_set
    if missing_headings:
        issues['warnings'].append(
            f"缺失的标题：{', '.join(missing_headings)}"
        )
        issues['is_complete'] = False

    # Check conversion ratio (normal ratio is around 60-80%)
    if issues['conversion_ratio'] < 40:
        issues['warnings'].append(
            f"转换率异常：{issues['conversion_ratio']:.1f}%（正常范围：40%-90%）"
        )
        issues['is_complete'] = False

    # Check for empty sections
    if len(markdown_content) < 100:
        issues['warnings'].append(
            f"生成的Markdown内容过短（{len(markdown_content)} 字符），可能内容缺失"
        )
        issues['is_complete'] = False

    # Info messages
    issues['info'].append(f"HTML内容长度：{len(html_content)} 字符")
    issues['info'].append(f"Markdown内容长度：{len(markdown_content)} 字符")
    issues['info'].append(f"转换率：{issues['conversion_ratio']:.1f}%")

    return issues

def print_integrity_report(issues, article_title):
    """Print content integrity report."""
    print("\n" + "="*60)
    print(f"内容完整性检查报告 - {article_title}")
    print("="*60)

    # Print info messages
    print("\n【信息】")
    for info in issues['info']:
        print(f"  [OK] {info}")

    # Print HTML headings
    print("\n【HTML中的标题】")
    for i, heading in enumerate(issues['html_headings'], 1):
        print(f"  {i}. {heading}")

    # Print Markdown headings
    print("\n【Markdown中的标题】")
    for i, heading in enumerate(issues['markdown_headings'], 1):
        print(f"  {i}. {heading}")

    # Print warnings
    if issues['warnings']:
        print("\n【警告】")
        for warning in issues['warnings']:
            print(f"  [WARN] {warning}")
        print(f"\n  内容完整性状态：{'不完整' if not issues['is_complete'] else '完整'}")
    else:
        print("\n【警告】")
        print("  [OK] 未检测到内容缺失问题")
        print(f"\n  内容完整性状态：完整")

    print("\n" + "="*60)

def extract_article(url, cookie, output_dir=None):
    """Extract article from GeekBang and save as Markdown with integrity check."""
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

    try:
        req = urllib.request.Request(api_url, data=data, headers=headers, method='POST')
        with urllib.request.urlopen(req) as response:
            response_text = response.read().decode('utf-8')
            json_data = json.loads(response_text)

            if 'data' in json_data and 'article_content' in json_data['data']:
                article_content = json_data['data']['article_content']
                article_title = json_data['data'].get('article_title', article_id)

                # Convert HTML to Markdown
                markdown_content = html_to_markdown(article_content)

                # Analyze content integrity
                issues = analyze_content_integrity(article_content, markdown_content)

                # Clean filename
                filename = article_title.replace('|', ' ').replace(':', ' ').replace('\\', ' ').replace('/', ' ').strip()
                filename = re.sub(r'^(\d+)\s+', r'\1 ', filename)
                filename = f"{filename}.md"

                # Determine output path
                if output_dir and os.path.isdir(output_dir):
                    output_path = os.path.join(output_dir, filename)
                else:
                    output_path = filename

                # Write Markdown file
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)

                print(f"\n[OK] Markdown文件已保存：{output_path}")
                print(f"[OK] 内容长度：{len(markdown_content)} 字符")

                # Print integrity report
                print_integrity_report(issues, article_title)

                return True, issues
            else:
                error_msg = json_data.get('error', {}).get('msg', 'Unknown error')
                print(f"[ERROR] 错误：{error_msg}")
                if 'permission' in error_msg.lower() or '权限' in error_msg:
                    print("提示：Cookie可能已过期或无效，请提供新的Cookie。")
                return False, None

    except Exception as e:
        print(f"[ERROR] 请求失败：{str(e)}")
        return False, None

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法：python geekbang_article.py <url> <cookie> [output_dir]")
        print("示例：python geekbang_article.py \"https://time.geekbang.org/column/article/40961\" \"cookie内容\"")
        sys.exit(1)

    url = sys.argv[1]
    cookie = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else None

    extract_article(url, cookie, output_dir)
