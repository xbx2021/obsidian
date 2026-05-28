import html
import re

def detect_language(code):
    if re.search(r'\bstd::\b|\bclass\s+\w+\s*\{|\bpublic:\b|\bprivate:\b|\b~[A-Za-z_]+\s*\(|std::mutex', code):
        return 'cpp'
    elif re.search(r'\bfunc\s+\w+\s*\(|\bpackage\s+\w+|\bimport\s+\(|bdefer\s+|\bnil\b|\bmake\s*\(', code):
        return 'go'
    elif re.search(r'\b#include\s*<|\bmalloc\s*\(|\bfree\s*\(|\bfprintf\s*\(|\bFILE\s*\*|\berrno\b', code):
        return 'c'
    elif re.search(r'\bpublic\s+class\s+|\bpublic\s+static\s+void\s+main|\bSystem\.out\.', code):
        return 'java'
    elif re.search(r'\bdef\s+\w+\s*\(|\bimport\s+\w+|\bprint\s*\(|\bTrue\b|\bFalse\b|\bNone\b', code):
        return 'python'
    else:
        return ''

def html_to_markdown(html_content):
    print(f"Input length: {len(html_content)}")
    
    step1 = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)
    print(f"After removing comments: {len(step1)}")
    
    step2 = html.unescape(step1)
    print(f"After unescaping: {len(step2)}")
    
    def process_code_block(match):
        code = match.group(1)
        lang = detect_language(code)
        return f'\n``` {lang}\n{code}\n```\n'
    
    step3 = re.sub(r'<pre\s*[^>]*><code\s*[^>]*>(.*?)</code></pre>', process_code_block, step2, flags=re.DOTALL)
    print(f"After pre/code block processing: {len(step3)}")
    
    step4 = re.sub(r'<pre\s*[^>]*>(.*?)</pre>', process_code_block, step3, flags=re.DOTALL)
    print(f"After pre block processing: {len(step4)}")
    
    step5 = re.sub(r'<code\s*[^>]*>(.*?)</code>', r'`\1`', step4, flags=re.DOTALL)
    print(f"After code tag processing: {len(step5)}")
    
    step6 = re.sub(r'<h1[^>]*>(.*?)</h1>', r'\n# \1\n', step5, flags=re.DOTALL)
    print(f"After h1 processing: {len(step6)}")
    
    step7 = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\n## \1\n', step6, flags=re.DOTALL)
    print(f"After h2 processing: {len(step7)}")
    
    step8 = re.sub(r'<h3[^>]*>(.*?)</h3>', r'\n### \1\n', step7, flags=re.DOTALL)
    print(f"After h3 processing: {len(step8)}")
    
    step9 = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', step8, flags=re.DOTALL)
    print(f"After strong processing: {len(step9)}")
    
    step10 = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', step9, flags=re.DOTALL)
    print(f"After b processing: {len(step10)}")
    
    step11 = re.sub(r'<span[^>]*>(.*?)</span>', r'\1', step10, flags=re.DOTALL)
    print(f"After span processing: {len(step11)}")
    
    step12 = re.sub(r'<li>\s*<p>(.*?)</p>\s*</li>', r'\n- \1', step11, flags=re.DOTALL)
    print(f"After li/p processing: {len(step12)}")
    
    step13 = re.sub(r'<li>(.*?)</li>', r'\n- \1', step12, flags=re.DOTALL)
    print(f"After li processing: {len(step13)}")
    
    step14 = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', step13, flags=re.DOTALL)
    print(f"After p processing: {len(step14)}")
    
    step15 = re.sub(r'</?(ul|ol)\s*[^>]*>', '', step14, flags=re.DOTALL)
    print(f"After ul/ol processing: {len(step15)}")
    
    step16 = re.sub(r'</?br\s*/?>', '\n', step15)
    print(f"After br processing: {len(step16)}")
    
    step17 = re.sub(r'<img\s+[^>]*?src\s*=\s*["\']([^"\']+)["\'][^>]*?>', r'![](\1)', step16, flags=re.DOTALL)
    print(f"After img processing: {len(step17)}")
    
    step18 = re.sub(r'<a\s+([^>]*?)href\s*=\s*["\']([^"\']*)["\']([^>]*?)>(.*?)</a>', r'[\4](\2)', step17, flags=re.DOTALL)
    print(f"After a processing: {len(step18)}")
    
    step19 = re.sub(r'<[^>]+>', '', step18)
    print(f"After removing remaining tags: {len(step19)}")
    
    step20 = re.sub(r'\n{3,}', '\n\n', step19)
    print(f"After reducing newlines: {len(step20)}")
    
    result = step20.strip()
    print(f"Final result length: {len(result)}")
    
    return result

# Test with a sample content
test_content = """<p>上一节，我们讲了复杂度的大O表示法和几个分析技巧，还举了一些常见复杂度分析的例子，比如O(1)、O(logn)、O(n)、O(nlogn)复杂度分析。掌握了这些内容，对于复杂度分析这个知识点，你已经可以到及格线了。但是，我想你肯定不会满足于此。</p><p>今天我会继续给你讲四个复杂度分析方面的知识点，<strong><span class="orange">最好情况时间复杂度</span></strong>（best case time complexity）、<strong><span class="orange">最坏情况时间复杂度</span></strong>（worst case time complexity）、<strong><span class="orange">平均情况时间复杂度</span></strong>（average case time complexity）、<strong><span class="orange">均摊时间复杂度</span></strong>（amortized time complexity）。如果这几个概念你都能掌握，那对你来说，复杂度分析这部分内容就没什么大问题了。</p><h2>最好、最坏情况时间复杂度</h2><p>上一节我举的分析复杂度的例子都很简单，今天我们来看一个稍微复杂的。你可以用我上节教你的分析技巧，自己先试着分析一下这段代码的时间复杂度。</p><pre><code>// n表示数组array的长度
int find(int[] array, int n, int x) {
  int i = 0;
  int pos = -1;
  for (; i &lt; n; ++i) {
    if (array[i] == x) pos = i;
  }
  return pos;
}
</code></pre><p>你应该可以看出来，这段代码要实现的功能是，在一个无序的数组（array）中，查找变量x出现的位置。如果没有找到，就返回-1。按照上节课讲的分析方法，这段代码的复杂度是O(n)，其中，n代表数组的长度。</p><!-- [[[read_end]]] --><p>我们在数组中查找一个数据，并不需要每次都把整个数组都遍历一遍，因为有可能中途找到就可以提前结束循环了。但是，这段代码写得不够高效。我们可以这样优化一下这段查找代码。</p><pre><code>// n表示数组array的长度
int find(int[] array, int n, int x) {
  int i = 0;
  int pos = -1;
  for (; i &lt; n; ++i) {
    if (array[i] == x) {
       pos = i;
       break;
    }
  }
  return pos;
}
</code></pre><p>这个时候，问题就来了。我们优化完之后，这段代码的时间复杂度还是O(n)吗？很显然，咱们上一节讲的分析方法，解决不了这个问题。</p>"""

result = html_to_markdown(test_content)
print("\n--- Output preview ---")
print(result[:500])
