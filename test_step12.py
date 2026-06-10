import re

# Test if Step 12 removes placeholders
test_str = '<p>Some text \x00NBSP\x00 more text</p>'

# Step 12: Remove any remaining HTML tags
result = re.sub(r'<[^>]+>', '', test_str)

print(f'Before: {repr(test_str)}')
print(f'After Step 12: {repr(result)}')

# Step 13: Restore placeholders
result = result.replace('\x00LT\x00', '<').replace('\x00GT\x00', '>')
result = result.replace('\x00NBSP\x00', ' ')

print(f'After Step 13: {repr(result)}')