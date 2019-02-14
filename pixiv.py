# -*- coding:utf-8 -*-
import os
import json
import random
import requests
import datetime
import time
import urllib.request

day = datetime.date.today()
def main():
    start = time.time()
    for page in range(1, 11, 1):
        url = 'https://www.pixiv.pro/ranking.php?mode=daily&p=' + str(page) + '&format=json'
        try:
            response = requests.get(url)
            resp = response.json()
            for pidid in range(0,50,1):
                if '初音ミク' in str(resp['contents'][pidid]):
                    title = resp['contents'][pidid]['title']
                    date = resp['contents'][pidid]['date']
                    pid = resp['contents'][pidid]['illust_id']
                    width = resp['contents'][pidid]['width']
                    height = resp['contents'][pidid]['height']
                    rank = resp['contents'][pidid]['rank']
                    url = resp['contents'][pidid]['url']
                    y = url.split('/')[7]
                    mo = url.split('/')[8]
                    d = url.split('/')[9]
                    h = url.split('/')[10]
                    mi = url.split('/')[11]
                    s = url.split('/')[12]
                    pagecount = resp['contents'][pidid]['illust_page_count']
                    print('----------------------------')
                    print('日榜排名:',rank)
                    print('标题:',title)
                    print('上传时间:',date)
                    print('图片ID:',pid)
                    print('分辨率:',width,'x',height)
                    print('--------------')
                    print('正在下载...')
                    for pageid in range(0,10,1):
                    	imgurl = 'https://i.pximg.pixiv.pro/img-original/img/' + str(y) + '/' + str(mo) + '/' + str(d) + '/' + str(h) + '/' + str(mi) + '/' + str(s) + '/' + str(pid) + '_p' + str(pageid) + '.png'
                    	r = requests.get(imgurl)
                    	if r.status_code !=200:
                    		imgurl = 'https://i.pximg.pixiv.pro/img-original/img/' + str(y) + '/' + str(mo) + '/' + str(d) + '/' + str(h) + '/' + str(mi) + '/' + str(s) + '/' + str(pid) + '_p' + str(pageid) + '.jpg'
                    		f = requests.get(imgurl)
                    		if f.status_code == 200:
                    			if os.path.exists(str(day)):
                    				with open(str(day) + "/" + str(pid) + "_p" + str(pageid) + ".jpg", "wb") as code:
                    					code.write(f.content)
                    			else:
                    				os.mkdir(str(day))
                    				with open(str(day) + "/" + str(pid) + "_p" + str(pageid) + ".jpg", "wb") as code:
                    					code.write(f.content)

                    				#print('下载完毕！')
                    	else:
                    		if os.path.exists(str(day)):
                    			with open(str(day) + "/" + str(pid) + "_p" + str(pageid) + ".png", "wb") as code:
                    				code.write(r.content)
                    		else:
                    			os.mkdir(str(day))
                    			with open(str(day) + "/" + str(pid) + "_p" + str(pageid) + ".png", "wb") as code:
                    				code.write(r.content)

                    			#print('下载完毕！')
            #time.sleep(1)
        except:
            pass


if __name__ == '__main__':
    main()
