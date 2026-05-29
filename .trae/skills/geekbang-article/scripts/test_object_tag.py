import re
import html

# Simulated problematic HTML snippet
test_html = '''<p>ArrayList<object> array</p><p>More content here</p><p>Even more content</p>'''

# Step 12: Remove any remaining HTML tags (from the original script)
result = re.sub(r'<[^>]+>', '', test_html)
print("After removing HTML tags:")
print(repr(result))
print()

# The issue: <object> is treated as an HTML tag and everything until > is removed
# But in this case, there's no closing > for <object, so it might behave differently

# Let's test with the actual problematic pattern
test_html2 = '''<p>ArrayList&lt;ArrayList<object> &gt; array'''
result2 = re.sub(r'<[^>]+>', '', test_html2)
print("After removing HTML tags (with encoded brackets):")
print(repr(result2))
print()

# The real issue - after html.unescape, &lt; becomes <
unescaped = html.unescape(test_html2)
print("After html.unescape:")
print(repr(unescaped))
result3 = re.sub(r'<[^>]+>', '', unescaped)
print("After removing HTML tags:")
print(repr(result3))
