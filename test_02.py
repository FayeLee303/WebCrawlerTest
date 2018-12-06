from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import random

base_url = "https://baike.baidu.com"    # 起始页
# 将 /item/... 的网页都放在 his 中, 做一个备案, 记录浏览过的网页
his = ["/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB/5162711"]

# 选择在his的最后一个子url打印标题和url
# 打印出来现在正在哪张网页上, 网页的名字
# -1是读取列表末尾的最后一个元素！
url = base_url + his[-1]
html = urlopen(url).read().decode('utf-8')  # 用utf-8解码
soup = BeautifulSoup(html, features='html.parser')
# find返回找到的第一个h1,find_all是返回找到的所有的
print(soup.find('h1').get_text(), '    url: ', his[-1])
# 网络爬虫     url:  /item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB/5162711
# 先分析网页的结构，所有的子链接都href的标签，里面有%所以可以使用正则匹配
# 在这个网页上找所有符合要求的 /item/ 网址
sub_urls = soup.find_all("a",
                         {
                             "target":"_blank",
                             "href":re.compile("/item/(%.{2})+$")
                         })
# print(sub_urls)
if len(sub_urls) != 0:
    # 如果找到的子链接不为空，就随机把子链接里的一个加到his列表里
    # 这些过滤后的网页中随机选一个当做下一个要爬的网页
    his.append(random.sample(sub_urls,1)[0]['href'])
else:
    # 如果当前页面的子链接为空，就退出这个页面，到下一个页面去找
    # 就往回跳一个网页, 回到之前的网页中再随机抽一个网页做同样的事
    his.pop()
print(his)


# 使用循环来在网页间爬虫
# his是一个栈，用记录浏览过的网页，这里给定一个初始网页
his = ["/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB/5162711"]
for i in range(20):
    url = base_url + his[-1]    # url是his的最后一个网页，就是当前网页
    html = urlopen(url).read().decode('utf-8')   # 打开网页并用utf-8解码
    soup = BeautifulSoup(html, features='html.parser')  # 根据规则把当前网页包装成soup对象
    print(i,soup.find('h1').get_text(),' url:',his[-1]) # 打印当前轮数，当前网页的标题，当前网页网址
    # 找当前网页的子链接
    sub_urls = soup.find_all("a",
                             {
                                 "target":"_blank",
                                 "href":re.compile("/item/(%.{2})+$")
                             })
    if len(sub_urls) != 0:
        # 如果当前页面的子链接不为空，从过滤后的网页中随机选一个当做下一个要爬的网页
        his.append(random.sample(sub_urls,1)[0]['href'])
    else:
        # 否则把当前网页出栈，到下一个网页里爬虫
        his.pop()

