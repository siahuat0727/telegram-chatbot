# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib.request import urlopen
kind = 'politics'
base_url = "https://tw.news.yahoo.com/"
url = base_url + kind
html = urlopen(url).read().decode('utf-8')
soup = BeautifulSoup(html, features='lxml')
links = soup.find_all("a", {"class": "D(ib) Ov(h) Whs(nw) C($c-fuji-grey-l) C($c-fuji-blue-1-c):h Td(n) Fz(16px) Tov(e) Fw(700)"})
for link in links:
    print(link.get_text(), link['href'])
url = base_url + links[0]['href']
html = urlopen(url).read().decode('utf-8')
soup =  BeautifulSoup(html, features='lxml')
texts = soup.find_all("div", {'class': 'canvas-body Wow(bw) Cl(start) Mb(20px) Lh(1.7) Fz(18px) D(i)'})
print('url: ',url)
print(texts)
