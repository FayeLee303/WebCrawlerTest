from urllib.request import urlopen
import re
from bs4 import BeautifulSoup

html = urlopen("https://morvanzhou.github.io/static/scraping/basic-structure.html").read().decode('utf-8')
print(html)
# 使用正则表达式
# res = re.findall(r"<title>(.+?)</title>",html)
# print("\nPage title is:", res[0])
# res = re.findall(r"<p>(.+?)</p>",html, flags=re.DOTALL) # 选取多行
# print("\nPage paragraph is:", res[0])
# res = re.findall(r'href="(.*?)"',html)
# print("\nAll links:", res)

# 使用bs
# soup = BeautifulSoup(html, features='lxml')
soup = BeautifulSoup(html, features='html.parser')
print(soup.h1)
print(soup.p)
all_href = soup.find_all('a') # 找到所有的a标签
all_href = [l['href'] for l in all_href]    # 找soup里的东西的href的值，相当于字典
print('\n',all_href)    # 打印页面所有的链接

# 使用bs解析CSS
html = urlopen("https://morvanzhou.github.io/static/scraping/list.html").read().decode('utf-8')
# print(html)
soup = BeautifulSoup(html, features='html.parser')
month = soup.find_all('li',{'class':'month'})
for m in month:
    print(m.get_text())
    # print(m)
jan = soup.find('ul',{'class':'jan'}) # jan是一个soup对象
print(jan)
d_jan = jan.find_all('li')  # 对jan还可以用find
for d in d_jan:
    print(d.get_text())

html = urlopen("https://morvanzhou.github.io/static/scraping/table.html").read().decode('utf-8')
# print(html)
soup = BeautifulSoup(html, features='html.parser')
img_links = soup.find_all('img',{'src':re.compile('.*?\.jpg')})     # 正则表达式匹配jpg
for link in img_links:
    print(link['src'])