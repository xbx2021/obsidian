import re

# Simulate the full HTML content
html = '<code class="language-yaml">\x00NBSP\x00 namespaces:</code>'

# Step 2: Protect &nbsp; (already done in the HTML)
# html = html.replace('&nbsp;', '\x00NBSP\x00')

# Test the regex pattern
pattern = r'<code\s+class\s*=\s*["\'](?:language-|hljs-)?(\w*)["\'][^>]*>(.*?)</code>'
matches = re.findall(pattern, html, flags=re.DOTALL)
print('Matches:', matches)

# Test replacement with nbsp placeholder
def process_language_code(match):
    code = match.group(2)
    lang = match.group(1) if match.group(1) else ''
    # Restore angle brackets and nbsp in code blocks
    code = code.replace('\x00LT\x00', '<').replace('\x00GT\x00', '>')
    code = code.replace('\x00NBSP\x00', ' ')
    # Convert HTML quotation entities in code blocks
    code = code.replace('&quot;', '"').replace('&#34;', '"')
    code = code.replace('&apos;', "'").replace('&#39;', "'")
    if lang:
        lang = lang.replace('language-', '').replace('hljs-', '')
    return f'\n``` {lang}\n{code}\n```\n'

result = re.sub(pattern, process_language_code, html, flags=re.DOTALL)
print('Result:', repr(result))
