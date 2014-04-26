#coding:utf-8
'''
Created on 2014年3月20日

@author: ZSH
'''
import urllib.request
import json
from bs4 import BeautifulSoup
import os
import time

 
def get_data(code):
    codestr = str(code)
    d1 =[]#一个列表存一条记录
    for year in range(1990,2015):
        yearstr = str(year)
        for season in range(1,5):
            jidu = str(season)
            url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/'+codestr+'.phtml?year='+yearstr+'&jidu='+jidu
            rsp = urllib.request.urlopen(url)
            html = rsp.read()
            soup = BeautifulSoup(html, from_encoding = 'GB2312')
            tablesoup = soup.find_all('table', attrs = {'id':'FundHoldSharesTable'}) 
            try:
                rows = tablesoup[0].findAll('tr')
            except:
                continue
            for row in rows[2:]:
                data = row.findAll('td')               
                d2 = {}
                d2['stock_id'] = code
                d2['release_date'] = data[0].get_text(strip = True)
                d2['open'] = data[1].get_text(strip = True);
                d2['high'] = data[2].get_text(strip = True);
                d2['close'] = data[3].get_text(strip = True);
                d2['low'] = data[4].get_text(strip = True);
                d2['volume'] = data[5].get_text(strip = True);
                d2['amount'] = data[6].get_text(strip = True);
                d1.append(d2);
    encodejson = open('DATA/' + code+'.json','w')
    encodejson.write(json.dumps(d1,indent=2,ensure_ascii = False))
#     encodejson.write(strfile)

def get_stocklist():
    stockf = open('DATA/log/stockid.txt','r')
    stocklist = []
    for ln in stockf.readlines():
        stocklist.append(ln.strip('\n'))
    return stocklist

if __name__ =='__main__':
    stocklist = get_stocklist()
    newpath = 'DATA/ '
    logpath = 'DATA/log/ '
    os.makedirs(newpath,exist_ok = True)
    os.makedirs(logpath,exist_ok = True)
    logtxt = open(logpath +'log.txt','w')
    for i in range(0,len(stocklist)):
        get_data(stocklist[i])
        stri = str(i)
        strlen = str(len(stocklist))
        print('已完成'+strlen+'条数据中的'+stri+'条！')
        print(time.strftime('%X',time.localtime() ))
        logtxt.write('已完成'+strlen+'条数据中的'+stri+'条！\n')
        logtxt.write(time.strftime('%X',time.localtime() ))
     


