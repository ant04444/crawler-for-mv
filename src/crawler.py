# coding: utf-8

import requests
from BeautifulSoup import BeautifulSoup
import concurrent.futures
import Queue
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def download_page(url):
    print url, "processing"

    r = requests.get(url)
    content = r.content.decode('gbk')

    q.put({"url": url, "content": content})


def parse():
    while True:
        try:
            page = q.get()
            page_url = page["url"]
            page_content = page["content"]

            soup = BeautifulSoup(page_content)
            title = soup.find("title").text
            print "title:", title

            if title.lower().find(keyword.lower()) != -1:
                if soup.find("div", attrs={'class': 't_l'}).findAll("div")[4].find("a").text == u"日韩原版高清MV":
                    is_target = True
                else:
                    is_target = False
                    write_result("{}: {}".format(title.encode("utf8"), page_url))
            else:
                is_target = False

            if is_target:
                print page_url, "is the target!!"
                write_result("{}: {}".format(title.encode("utf8"), page_url))
        except Exception, e:
            print page_url, "error", e


def write_result(record):
    result_file = open(result_file_path, "a")
    result_file.write('{}\r\n'.format(record))
    result_file.close()


def clear_file():
    import os
    if os.path.exists(result_file_path):
        os.remove(result_file_path)


# def process(url_id):
#     try:
#         target_url = base_url + str(url_id)
#         print target_url, "processing"
#         content = download_page(target_url)
#
#         if is_target(content):
#             print target_url, "is the target!!"
#             write_result(target_url)
#
#         # time.sleep(0.01)
#     except Exception, e:
#         print Exception, ":", e
# keyword = "sistar"
# keyword = "少女时代"
# keyword = "F(x)"
keyword = "Kara"

q = Queue.Queue()
result_file_path = "g:/result-{}.log".format(keyword)
clear_file()

download_e = concurrent.futures.ThreadPoolExecutor(max_workers=9)
base_url = "http://www.zhuyin.com/v/"
for i in range(1, 2577):
    download_e.submit(download_page, base_url + str(i))

parse_e = concurrent.futures.ThreadPoolExecutor(max_workers=9)
for i in range(0, 9):
    parse_e.submit(parse)


