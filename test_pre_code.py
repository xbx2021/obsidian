import re

html = '<pre><code class="language-yaml">\x00NBSP\x00 namespaces:</code></pre>'

# Test the <pre><code> regex
pattern1 = r'<pre\s*[^>]*>\s*<code\s*[^>]*>(.*?)</code>\s*</pre>'
matches1 = re.findall(pattern1, html, flags=re.DOTALL)
print(f'<pre><code> matches: {len(matches1)}')
for m in matches1:
    print(f'  Code: {m}')

# Test the <code class> regex
pattern2 = r'<code\s+class\s*=\s*["\'](?:language-|hljs-)?(\w*)["\'][^>]*>(.*?)</code>'
matches2 = re.findall(pattern2, html, flags=re.DOTALL)
print(f'\n<code class> matches: {len(matches2)}')
for m in matches2:
    print(f'  Lang: {m[0]}, Code: {m[1]}')
