import re
import requests
from scrapy import Selector
import unicodedata


headers = {
        'Cookie': 'bid=h_7m-JvTKR0; __gads=ID=fde61ed40e1b8559:T=1601735726:S=ALNI_Ma1BLMVhcNsQrm8sQQr3rNA6LF11g; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1602327248%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DK8RtefrXWKrvUsHZM5_D652aPXruDGN1ibhxJjOgHleaAXkfB5kBvqIT9qTfKNyY%26wd%3D%26eqid%3De8d6d645000c9596000000045f8192cc%22%5D; _pk_id.100001.4cf6=c36482012b1cfb02.1602327248.1.1602327248.1602327248.; _pk_ses.100001.4cf6=*; ap_v=0,6.0; __utma=30149280.980966996.1602327248.1602327248.1602327248.1; __utmb=30149280.0.10.1602327248; __utmc=30149280; __utmz=30149280.1602327248.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=223695111.1313248410.1602327248.1602327248.1602327248.1; __utmb=223695111.0.10.1602327248; __utmc=223695111; __utmz=223695111.1602327248.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __yadk_uid=ewxpFSttmq0dUAtnFmzIxHhLJoP0wcze',
        'Host': 'movie.douban.com',
        'Pragma': 'no-cache',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    }
url = 'https://movie.douban.com/subject/1291561/'
response = requests.get(url=url,headers=headers)
html = response.text
# print(response.text)
selector = Selector(response)
name = selector.xpath('//*[@property="v:genre"]/text()').extract()
# name = re.findall('<span property="v:summary" class="">(.*?)</span>',html,re.S)
# name = "".join(name)
name = str(name)
# name = ''.join(name.split())
# name = name.replace(r"\n\u3000\u3000","").replace(r"\n","").replace(r"<br/>","").replace("[","").replace("]","")
# name = "".join(name)
name = name.replace("[","").replace("]","")
print(name)