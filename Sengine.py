# coding:utf8
import requests
import parsel
from threading import Thread, Lock
from queue import  Queue
from  time import  time,ctime
import  re
import sys
import argparse

baidu_headers={
       'Accept9': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Cookie': 'BD_UPN=12314753; BAIDUID=B9C663242EBFE646684C271051BFEA9E:FG=1; PSTM=1585744388; BIDUPSID=94FB3558C0BDAA06C330FDC42A453409; H_WISE_SIDS=139912_143932_143381_142018_144883_145118_141744_144419_144134_144472_144483_136861_144490_131246_144682_137749_138883_140259_141941_127969_144171_140066_144341_140593_142421_144607_144727_143922_144485_131423_100806_142206_107316_144306_143478_144966_142426_144534_143667_144333_144238_143853_142273_110085; MSA_WH=1141_666; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDUSS=RLMWhkcS1aZWRSVUtHY05wbnFja2xqZmJjZ0s4VjRwM3JjRlQzQTNmOUZTTjllRVFBQUFBJCQAAAAAAAAAAAEAAABhYeIxTElYTkhPTkcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEW7t15Fu7ded1; yjs_js_security_passport=d9a54629350d171585f4bd079e15e2b0d527848e_1589101657_js; delPer=0; BD_CK_SAM=1; PSINO=1; COOKIE_SESSION=11125_0_7_2_7_20_0_3_4_3_2_4_0_0_6_0_1589110468_0_1589121587%7C9%2388918_49_1589018226%7C9; ZD_ENTRY=baidu; BDRCVFR[C0p6oIjvx-c]=mbxnW11j9Dfmh7GuZR8mvqV; H_PS_PSSID=1463_31325_21110_31594_30841_31464_31322_30823_31164_22157; H_PS_645EC=ecec2k70KZZ5j0c3Qg7w5uVxJu8RsA1acZ7WKo%2Bq%2BO7eYcEW2gDIzOg8B0Y'
,'Host': 'www.baidu.com',
# 'Sec-Fetch-Mode':' navigate',
# 'Sec-Fetch-Site': 'none',
# 'Sec-Fetch-User': '?1',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
}
sogo_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Host": "www.sogou.com",
    "Cookie": "CXID=B5CF7A1E1028B814019DC2F4E110A9AB; SUID=C04829654B238B0A5ECFD8BF000E06B6; wuid=AAFYLJ58LwAAAAqLMVRc4QoAGwY=; ABTEST=0|1600484914|v17; SUV=1600484919760902; browerV=3; osV=1; pgv_pvi=1600874496; ssuid=9344371576; sw_uuid=9419120871; IPLOC=CN1100; SNUID=AF76B03DEEEB5EAB3C608AB7EEEA3EBE; ld=mZllllllll2KBgYLlllllVdZQIUlllllJ4VkSyllll6lllllpZlll5@@@@@@@@@@",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
}
bing_headers = {
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Sec-Fetch-Site': 'none',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-Dest': 'document',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Cookie': 'MUID=19E3D1CC85906B6722C8DFCF81906899; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=D47E325062A8462BB190665814E477F3&dmnchg=1; MUIDB=19E3D1CC85906B6722C8DFCF81906899; _SS=SID=13CCB5CDDCA46F492DFABA8FDD8A6EC7&bIm=496; _EDGE_S=mkt=zh-cn&SID=13CCB5CDDCA46F492DFABA8FDD8A6EC7; ipv6=hit=1599806393488&t=6; SRCHUSR=DOB=20200911&T=1599802808000; SRCHHPGUSR=CW=1920&CH=213&DPR=1&UTC=480&DM=0&HV=1599803528&WTS=63735399592'
}
headers={
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}

class MyThread(Thread):
    def __init__(self,qu):
        super(MyThread, self).__init__()
        self._queue = qu
    def run(self):
        lock.acquire()
        print("正在爬取中......")
        while not self._queue.empty():
            url = self._queue.get()
            # print(url)
            try:
                if "https://www.baidu.com/" in url:

                            self.crawl_baidu(url)

                elif "https://cn.bing.com/" in url:

                            self.crawl_bing(url)
                
                elif "https://www.sogou.com/" in url:

                            self.crawl_sogo(url)

            except Exception as err:
                            print(err)
        self.remove_duplicate()
        lock.release()

    def remove_duplicate(self): 
        f3 = open('url.txt', 'r')
        dates = f3.readlines()
        f3.close()
        with open('url.txt', 'w') as f:
            tmp_list = set(dates)
            for i in tmp_list:
                # print(i.strip())
                url = i.strip()
                print(url)
                f.write(url + "\n")
        f.close()
    def crawl_baidu(self,url):    
            f2 = open('url.txt', 'a+')
            response = requests.get(url, headers=baidu_headers, timeout=5)
            response.encoding = response.apparent_encoding
            sel = parsel.Selector(response.text)
            title3 = sel.xpath('//*[@data-click]')
            title2 = title3.xpath('./@href').getall()
            for i in title2:
                if 'link?url=' in i:  
                    try:
                        real_url = requests.get(i, headers=baidu_headers, timeout=3)
                        if real_url.status_code == 200:
                            real_url_index = real_url.url.split('/', -1)
                            urls = real_url_index[0] + "//" + real_url_index[2]
                            f2.write(urls + "\n")
                    except:
                        pass
            f2.write("\n---------------baidu-----------------\n")
            f2.close()   

    def crawl_sogo(self, url):            
            f2 = open('url.txt', 'a+')
            response = requests.get(url, headers=sogo_headers, timeout=5)
            response.encoding = response.apparent_encoding
            sel = parsel.Selector(response.text)
            url_href = sel.xpath('//h3/a/@href').extract() 
            for i in url_href:

                url_tmp = "https://www.sogou.com" + str(i)
                tmp_response = requests.get(url=url_tmp, headers=headers, timeout=6)  ## sogo做了两次跳转，需要爬取两次url结果才可得出真的。
                real_url_tmp = re.findall(r'URL=\'(.*?)\'', tmp_response.text, re.S)[0]
                real_url = real_url_tmp.split('/', -1)
                real_url = real_url[0] + "//" + real_url[2]  
                f2.write(real_url + '\n')
            f2.write("\n-------------crawl_sogo-----------\n")

            print("End for Sogo %s"%(ctime()))

    def crawl_bing(self,url):
            f = open('url.txt','a+')
            response = requests.get(url=url, headers=bing_headers)
            response.encoding = response.apparent_encoding
            sel = parsel.Selector(response.text)

            bing_title_url = sel.xpath('//h2/a/@href').extract()  
            
            url_list = list(set(bing_title_url))  
            for url_tmp in url_list:  
      
                url_index = url_tmp.split('/', -1)  
                urls = url_index[0] + "//" + url_index[2]


     
                f.write(urls + "\n")
            f.write("\n----------------------bing-----------------\n")
            f.close()
      


lock = Lock()
def main(wd, pages):
    thread_list = []
    thread_num = 50
    qu = Queue()

    for num_baidu in range(0, int(pages) * 10 + 10 + 1, 10):
        qu.put("https://www.baidu.com/s?wd=%s&pn=%s" % (wd, str(num_baidu)))

    for num_bing in range(1, int(pages) * 10, 10):
        qu.put("https://cn.bing.com/search?q=%s&first=%s" % (wd, num_bing))

    for num_sogo in range(1, int(pages) + 1, 1):
        qu.put("https://www.sogou.com/web?query=%s&page=%s" % (wd, num_sogo))

    for i in range(thread_num):
        thread_list.append(MyThread(qu))
    for t in thread_list:
        t.start()
    for q in thread_list:
        q.join()


if __name__ == '__main__':
    # log = b"""\xe5\x85\xac\xe4\xbc\x97\xe5\x8f\xb7:\xe4\xb8\x80\xe4\xbd\x8d\xe4\xb8\x8d\xe6\x84\xbf\xe9\x80\x8f\xe9\x9c\xb2\xe5\xa7\x93\xe5\x90\x8d\xe7\x9a\x84\xe7\x83\xad\xe5\xbf\x83\xe7\xbd\x91\xe5\x8f\x8b"""
    parser = argparse.ArgumentParser(description="公众号：一位不愿透露姓名的热心网友")
    parser.add_argument('-W', '--keyword', help='搜索的关键词 ', metavar='')
    parser.add_argument('-P', '--pages', metavar='', type=int, help='爬取的页面数 ')
    args = parser.parse_args()
    if len(sys.argv) < 2:
        print('请输入参数！')
        parser.print_help()
        print("Example: Sengine.py  -W \"site:baidu.com\" -P 10")
        sys.exit(-1)
    else:
        main(args.keyword, args.pages)
