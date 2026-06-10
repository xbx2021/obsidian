import re

# Test HTML from the actual content (simulating after Step 2 protection)
html = '''<code class="language-yaml">---
clusterURL: 127.0.0.1

addons:

\x00NBSP\x00 namespaces:
\x00NBSP\x00 \x00NBSP\x00 default: addons-system
</code>'''

# Test the regex pattern
pattern = r'<code\s+class\s*=\s*["\'](?:language-|hljs-)?(\w*)["\'][^>]*>(.*?)</code>'
matches = re.findall(pattern, html, flags=re.DOTALL)
print(f'Matches: {len(matches)}')
for m in matches:
    print(f'  Lang: {m[0]}, Code: {m[1][:50]}...')

# Test replacement
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
print('\nResult:')
print(result)
