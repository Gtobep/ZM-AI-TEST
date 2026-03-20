import sys

with open('e:/ClaudeCode/workspace/data_str.txt','r',encoding='utf-8') as f:
    DATA = f.read()
with open('e:/ClaudeCode/workspace/echarts.min.js','r',encoding='utf-8') as f:
    ECHARTS = f.read()

TEMPLATE = open('e:/ClaudeCode/workspace/template.html','r',encoding='utf-8').read()
HTML = TEMPLATE.replace('__ECHARTS__', ECHARTS).replace('__DATA__', DATA)

with open('e:/ClaudeCode/workspace/index.html','w',encoding='utf-8') as f:
    f.write(HTML)
print('Done, size:', round(len(HTML)/1024/1024,2), 'MB')
