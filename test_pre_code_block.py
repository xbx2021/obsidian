import re

def detect_language(code):
    """Detect programming language from code content."""
    code_clean = code.strip()
    if re.search(r'\bstd::\b|\bclass\s+\w+\s*\{|\bpublic:\b', code_clean):
        return 'cpp'
    elif re.search(r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*:', code_clean):
        # YAML pattern
        return 'yaml'
    else:
        return ''

# Test HTML from the actual content (simulating after Step 2 protection)
html = '''<pre><code class="language-yaml">---
clusterURL: 127.0.0.1

addons:

\x00NBSP\x00 namespaces:
\x00NBSP\x00 \x00NBSP\x00 default: addons-system
</code></pre>'''

# Step 3: Process code blocks FIRST
def process_code_block(match):
    code = match.group(1)
    # Restore angle brackets and nbsp in code blocks
    code = code.replace('\x00LT\x00', '<').replace('\x00GT\x00', '>')
    code = code.replace('\x00NBSP\x00', ' ')
    # Convert HTML quotation entities in code blocks
    code = code.replace('&quot;', '"').replace('&#34;', '"')
    code = code.replace('&apos;', "'").replace('&#39;', "'")
    lang = detect_language(code)
    return f'\n``` {lang}\n{code}\n```\n'

# Handle <pre><code>...</code></pre> blocks
result = re.sub(r'<pre\s*[^>]*>\s*<code\s*[^>]*>(.*?)</code>\s*</pre>',
                process_code_block, html, flags=re.DOTALL)

print('Result:')
print(result)
