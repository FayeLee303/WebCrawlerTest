import os
from urllib.request import urlretrieve
import requests
from bs4 import BeautifulSoup

"""
下载图片
找到图片所在网页，图的位置在html里的信息
需要补全图片的网址=网页网址/图片位置
"""

# 使用urlretrieve下载文件
# 特点：下载完才能保存
os.makedirs('./imgs',exist_ok=True)
img_url = "https://morvanzhou.github.io/static/img/description/learning_step_flowchart.png"
urlretrieve(img_url,'./imgs/image1.png')

# 使用requestes下载文件
# 特点：下载一点保存一点，一个 chunk 一个 chunk 的下载.

r = requests.get(img_url)
# 二进制的方式写入文件
with open('./imgs/image2.png','wb') as f:
    f.write(r.content)
r = requests.get(img_url,stream=True)    # 流加载
# 使用 r.iter_content(chunk_size) 来控制每个 chunk 的大小,
# 然后在文件中写入这个 chunk 大小的数据
with open('./imgs/image3.png','wb') as f:
    # 每次加载32个字节保存32个字节
    for chunk in r.iter_content(chunk_size=32):
        f.write(chunk)

# 爬取国家地理网站的图片http://www.ngchina.com.cn/animals/
# 首先查看页面的源码元素，分析图片存在什么标签里
"""
<ul class="img_list">
<li class="mod_w">
<div class="imgs cf">
<a href="/animals/facts/8938.html"><img src="http://image.ngchina.com.cn/2018/1205/20181205110937940.jpg"></a>
</div>
</li>
<li class="mod_w">
<div class="imgs cf">
<a href="/animals/facts/8937.html"><img src="http://image.ngchina.com.cn/2018/1204/20181204123620776.jpg"></a>
</div>
</li>
<li class="mod_w">
<div class="imgs cf">
<a href="/animals/protection/8936.html"><img src="http://image.ngchina.com.cn/2018/1203/20181203025110562.jpg"></a>
</div>
</li>
</ul>
"""
# 先找带有 img_list 的这种 <ul>, 然后在 <ul> 里面找 <img>.
url = "http://www.ngchina.com.cn/animals/"
html = requests.get(url).text
soup = BeautifulSoup(html,features='html.parser')
img_url_all = soup.find_all('ul',{'class':'img_list'})
for ul in img_url_all:
    imgs = ul.find_all('img')
    for img in imgs:
        img_url = img['src'] # 根据src取到图片的地址
        r = requests.get(img_url,stream=True)
        image_name = img_url.split('/')[-1]
        with open('./img/%s'%image_name,'wb') as f:
            for chunk in r.iter_content(chunk_size=32):
                f.write(chunk)
        print('Saved%s'%image_name)

