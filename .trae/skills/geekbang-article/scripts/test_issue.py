import re
import html

# The problematic HTML snippet
test_html = '''<p>ArrayList&lt;ArrayList<object> &gt; array。<p></p>
<p>我总结一下，对于业务开发，直接使用容器就足够了</p>
<h2>解答开篇</h2>'''

print("Original HTML:")
print(test_html)
print()

# After unescape
unescaped = html.unescape(test_html)
print("After html.unescape:")
print(unescaped)
print()

# After removing HTML tags
result = re.sub(r'<[^>]+>', '', unescaped)
print("After removing HTML tags:")
print(result)
print()

# The issue: <ArrayList<object> is treated as a single tag!
# Let's check what the regex matches
matches = re.findall(r'<[^>]+>', unescaped)
print("Tags found by regex:")
for m in matches:
    print(f"  {m}")
