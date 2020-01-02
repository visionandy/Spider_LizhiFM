# -*- coding:utf-8 -*- 
import re
import urllib.request
import requests
from bs4 import BeautifulSoup
import os
import time
global_download_path='/mnt/hdd/dataset/audio/lizhi/'

def get_request_fun(url):

    free_proxy = {'http':'39.106.223.134:80'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    }
    headers['User-Agent']='Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)'
    try:
        html = requests.get(url=url,stream=True,verify=False, headers=headers,proxies=free_proxy)
    except:
        import IPython
        IPython.embed()
        html=None
        print('something goes wrong')
    return html

# _ud.mp3:超高清; _hd.mp3:高清; _sd.m4a:低清

def get_music_lizhifm(url):
    id = url.rsplit('/', 1)[1]
    url = 'http://www.lizhi.fm/media/url/{}'.format(id)
    headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    }
    #html = requests.get(url, headers=headers).json()
    html=get_request_fun(url).json()

    # print(html)
    if html['data']:
      mp3_url = html['data']['url']
      return mp3_url
    else:
      print("!!!"+html['msg'])
      return None
    
def download_each_item(article_url,mp3_save_path):
  downloadurl = get_music_lizhifm(article_url)
  urlList = []
  title=mp3_save_path.split('/')[-1]
  print(title+'  is downloading')

  try:
    if downloadurl and not os.path.exists(mp3_save_path) :
      urllib.request.urlretrieve(downloadurl,mp3_save_path )
  except:
      print('somethnig goes wrong')
  print(title+' download is completed')




def  download_each_page(page_url):
  userId ='1708890' #re.findall('(/[0-9]{7}/)',startUrl)[0]
  page = get_request_fun(page_url)
  bs = BeautifulSoup(page.content, features='lxml')
  all_articles=bs.find_all("a", {"class":"clearfix js-play-data audio-list-item"})
  for item_inf in all_articles:
      title = item_inf["title"]
      mp3_save_path=global_download_path+userId+'/'+title+'.mp3'
      if os.path.exists(mp3_save_path):
        print(mp3_save_path+' already exists')
        continue
      # import IPython
      # IPython.embed()
      article_url='https://www.lizhi.fm'+item_inf["href"]
      download_each_item(article_url,mp3_save_path)  
      time.sleep(5)



def downloadFromPage(startUrl):
  #page = requests.get(startUrl)

  userId ='1708890' #re.findall('(/[0-9]{7}/)',startUrl)[0]
  file_save_path=download_path+userId+'/'
  page = get_request_fun(startUrl)
  bs = BeautifulSoup(page.content, features='lxml')
  title = bs.select(".audioName")[0].text
  mp3_save_path=file_save_path+title+'.mp3'
  print(title+' is downloading')

  import IPython
  IPython.embed()

  if not os.path.exists(file_save_path):
    os.makedirs(file_save_path)

  downloadurl = get_music_lizhifm(startUrl)
  urlList = []
  if downloadurl and not os.path.exists(mp3_save_path) :
    urllib.request.urlretrieve(downloadurl,mp3_save_path )

  print(title+' download is completed')

  # get next url
  for link in bs.findAll('a'):
      url = link.get('href')
      downloadableUrl = re.findall('(^[0-9]{19}$)', url)
      if downloadableUrl:
        urlList.append(downloadableUrl[0])
  #import IPython
  #IPython.embed()
  time.sleep(1)
  if(len(urlList) == 2):
    nextUrl = 'https://www.lizhi.fm'+userId+urlList[1]
    print('nextUrl: ' + nextUrl)
    downloadFromPage(nextUrl)
  else:
    print('urlList length error:'+ urlList)
    #import IPython
    #IPython.embed()
    return


if __name__ == '__main__':
    print('*' * 30 + 'ready to download' + '*' * 30)
    for page_id in range(1,100):
      url ='https://www.lizhi.fm/user/2544758401649219116/p/'+str(page_id)+'.html' #input('[请输入初始下载链接]:')
      download_each_page(url)
