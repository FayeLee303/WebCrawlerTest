"""
分布式爬虫，多进程更有效抓取网页
一个网页理由多个url，使用多进程同时下载这些url，得到url的html开始分析
将网页里还没有爬过的url整理在一起，交给多线程，重复这个过程
"""
import multiprocessing as mp
import time
from urllib.request import urlopen, urljoin
from bs4 import BeautifulSoup
import re

base_url = "https://morvanzhou.github.io/"
if base_url != "http://127.0.0.1:4000/":
    restricted_crawl = True
else:
    restricted_crawl = False

# 爬取网页
def crawl(url):
    response = urlopen(url)
    return response.read().decode('utf-8') # 返回解码的网页

# 解析网页
def parse(html):
    soup = BeautifulSoup(html,features='html.parser')
    urls = soup.find_all('a',
                         {'herf':re.compile('^/.+?$')})
    title = soup.find('h1').get_text().strip()
    # 去重
    # 去掉爬到的重复的网址
    page_urls =set([urljoin(base_url,url['herf'])for url in urls])
    url = soup.find('meta',
                    {'property':'og:url'})['content']
    return title,page_urls,url

# 不使用多线程的方式
# 定义两个 set, 用来搜集爬过的网页和没爬过的
unseen = set([base_url])
seen = set()
count, t1 = 1,time.time()
while len(unseen)!=0: # 还有东西没爬
    if restricted_crawl and len(seen)>20:
        break
    print('\nDistributed Crawing...')
    # 对unseen里的每个网页作爬取存到htmls
    htmls = [crawl(url)for url in unseen]

    print('\nDistributed Parsing...')
    # 对html作解析
    results = [parse(html)for html in htmls]

    print('\nAnalysing...')
    # 把unseen最上面的放到seen里，把unseen清空
    seen.update(unseen)
    unseen.clear()

    for title,page_urls,url in results:
        print(count,title,url)
        count +=1
        # page_urls - seen剩下是没爬取的
        # 居然可以用减法
        unseen.update(page_urls - seen)
print('t1:%.1f s'%(time.time()-t1))

# 使用多线程的方式
pool = mp.Pool(4)
count, t2 = 1,time.time()
while len(unseen)!=0: # 还有东西没爬
    if restricted_crawl and len(seen)>20:
        break
    print('\nDistributed Crawing...')
    # 对unseen里的每个网页作爬取存到htmls
    # htmls = [crawl(url)for url in unseen]
    # 使用多进程，把对每个网页的爬取过程分给多个进程做
    crawl_jobs = [pool.apply_async(crawl,args=(url,))for url in unseen]
    htmls = [i.get()for i in crawl_jobs]

    print('\nDistributed Parsing...')
    # 对html作解析
    # results = [parse(html)for html in htmls]
    # 使用多进程，把对每个网页的解析过程分给多个进程做
    parse_jobs = [pool.apply_async(parse,args=(html,))for html in htmls]
    results = [j.get()for j in parse_jobs]

    print('\nAnalysing...')
    # 把unseen最上面的放到seen里，把unseen清空
    seen.update(unseen)
    unseen.clear()

    for title,page_urls,url in results:
        print(count,title,url)
        count +=1
        # page_urls - seen剩下是没爬取的
        # 居然可以用减法
        unseen.update(page_urls - seen)
print('t2:%.1f s'%(time.time()-t2))
