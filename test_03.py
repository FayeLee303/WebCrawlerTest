"""
加载网页的请求类型：get,post,head等
post:账号登陆，搜索内容，上传图片，上传文件，往服务器传数据
    post给服务器发送个性化请求，例如发送账号密码，服务器返回一个有个人信息的HTML
get：正常打开网页，不往服务器传数据
"""
import requests
import webbrowser

# get
param = {'wd':'python'}     # 搜索keyword
r = requests.get("http://www.baidu.com/s",params = param)     # 合成url
print(r.url)
# webbrowser.open(r.url)

# post 模拟提交
data = {'firstname':'faye','lastname':'lee'}    # 要提交的数据，是form形式的
# 这个网址不是提交页面的网址，是把信息提交给这个网址，在浏览器里查看元素看到
# 提交有页面的网址是http://pythonscraping.com/pages/files/form.html
# r是post返回的数据
r = requests.post("http://pythonscraping.com/pages/files/processing.php",data= data)
print(r.text)

# 上传图片的网址是http://pythonscraping.com/files/form2.html
# choose file” 按键链接的 <input> 是一个叫 uploadFile 的名字. 放入 python 的字典当一个 “key”
# 使用 open 打开一个图片文件, 当做要上传的文件
file = {'uploadFile': open('/home/faye/桌面/t.jpg', 'rb')}
r = requests.post('http://pythonscraping.com/pages/files/processing2.php', files=file)
print(r.text)

# 模拟登陆的网址http://pythonscraping.com/pages/cookies/login.html
# 为了登陆账号，浏览器做了
# 1使用post方法登陆url可以在查看元素里看到
# 2post的时候使用用户输入的formdata里的数据
# 3生成cookies
"""
打开网页的时候每个页面是不连续的没有关联的
使用cookies保存之前浏览过的信息，然后传递给下一个页面在下一个页面就还是登陆状态了
用 requests.post + payload 的用户信息发给网页, 返回的 r 里面会有生成的 cookies 信息. 
接着请求去登录后的页面时, 使用 request.get, 并将之前的 cookies 传入到 get 请求. 
这样就能已登录的名义访问 get 的页面了.
"""
pyload = {'username':'faye','password':'password'}
r = requests.post('http://pythonscraping.com/pages/cookies/welcome.php',data=pyload)
print(r.cookies.get_dict())
r = requests.get('http://pythonscraping.com/pages/cookies/login.html',cookies=r.cookies)
print(r.text)
# 每次传递cookies很麻烦，使用session在会话里自动传递cookies
# session是有生命周期的
session = requests.Session()    # 创建session
pyload = {'username':'faye','password':'password'}
r = session.post('http://pythonscraping.com/pages/cookies/welcome.php',data=pyload)
print(r.cookies.get_dict())
r = session.get("http://pythonscraping.com/pages/cookies/login.html")
print(r.text)

