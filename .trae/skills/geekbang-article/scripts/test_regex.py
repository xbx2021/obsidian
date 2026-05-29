import re

# Test HTML with the special comment
html_content = '''<p>第一段内容</p><!-- [[[read_end]]] --><p>第二段内容</p><p>第三段内容</p>'''

# Current regex (problematic)
result1 = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)
print("After removing HTML comments (current):")
print(repr(result1))
print()

# The issue is that the regex is correct, but let me check the actual content
html_with_nested = '''<p>第一段</p><!-- comment --><p>第二段</p><!-- [[[read_end]]] --><p>第三段</p>'''
result2 = re.sub(r'<!--.*?-->', '', html_with_nested, flags=re.DOTALL)
print("After removing HTML comments (multiple comments):")
print(repr(result2))
