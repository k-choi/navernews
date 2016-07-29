import re
import requests
import json
from lxml import html
from datetime import datetime, timedelta
from collections import defaultdict
import threading
import time
import sys


# batch running of threads
def batch_run(l_threads, n_batch=100):
    n = len(l_threads)
    l_running = []
    while len(l_threads) > 0 or len(l_running) > 0:
        time.sleep(0.2)
        for thread in l_running:
            if not thread.isAlive():
                l_running.remove(thread)
        n_running = len(l_running)
        if n_running < n_batch and len(l_threads) > 0:
            n_new = min(n_batch - n_running, len(l_threads))
            l_running += l_threads[:n_new]
            for thread in l_threads[:n_new]:
                thread.start()
            l_threads = l_threads[n_new:]
        n_finished = n - len(l_threads) - len(l_running)
        sys.stdout.write('\r')
        sys.stdout.write('%d/%d %.2f%%' % (n_finished, n, float(n_finished)/n*100))
        sys.stdout.flush()
    sys.stdout.write('\n')
    sys.stdout.flush()


class KeyDefaultDict(defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret


def get_component_id(str_sid1):
    url = 'http://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=%s#&date=%s 00:00:00&page=1' \
          % (str_sid1, '2016-01-01')
    req = requests.get(url, timeout=1)
    tree = html.fromstring(req.content)
    str_component_id = tree.xpath('//*[@id="mainNewsComponentId"]/@name')[0]
    return str_component_id


d_componentId = KeyDefaultDict(get_component_id)


# download one article
def download_news(url):
    req = requests.request('GET', url)
    tree_news = html.fromstring(req.content)
    title = tree_news.xpath('//*[@id="articleTitle"]/text()')[0]
    # Note: /text() fails to retrieve content of some articles.
    l_para = [x for x in [x.strip() for x in tree_news.xpath('//*[@id="articleBodyContents"]/text()')] if x != '']
    textv1 = "\r\n".join(l_para)
    # Version 2: changed to //text(). problem is that it doesn't filter out ads.
    l_para = [x for x in [x.strip() for x in tree_news.xpath('//*[@id="articleBodyContents"]//text()')] if x != '']
    textv2 = "\r\n".join(l_para)
    str_time = tree_news.xpath('//span[@class="t11"]/text()')[0]
    str_time = str_time.replace(' ', '_').replace(':', '_').replace('-', '_')
    article = {'title': title, 'textv1': textv1, 'textv2': textv2, 'time': str_time}
    m = re.search('sid1=(\d+)&oid=(\d+)&aid=(\d+)', url)
    article_id = {'sid1': m.group(1), 'oid': m.group(2), 'aid': m.group(3)}
    return article, article_id


# threaded version with str_sid1 and str_date as input
def get_all_news_hrefs(str_sid1, str_date):
    def get_article_url(x):  # x: item in the itemList
        return "http://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=%s&oid=%s&aid=%s" \
               % (str_sid1, x['officeId'], x['articleId'])

    def add_news_href_for_compid_page(news_href_, query_string_, i_page):
        url = 'http://news.naver.com/main/mainNews.nhn?%s&page=%d' % (query_string_, i_page)
        res_ = requests.get(url)
        data_new = json.loads(res_.text)
        news_href_ += [get_article_url(x) for x in data_new['itemList']]

    str_component_id = d_componentId[str_sid1]
    url_pattern = 'http://news.naver.com/main/mainNews.nhn?componentId=%s&date=%s 00:00:00'
    res = requests.get(url_pattern % (str_component_id, str_date))
    data = json.loads(res.text)

    news_href = [get_article_url(j) for j in data['itemList']]
    n_pages = int(data['pagerInfo']['totalPages'])
    l_threads = []
    query_string = data['pagerInfo']['queryString']
    for i in range(2, n_pages + 1):
        l_threads.append(
            threading.Thread(target=add_news_href_for_compid_page, args=(news_href, query_string, i)))
    for thread in l_threads:
        thread.start()
    for thread in l_threads:
        thread.join()
    return news_href


# callback version, default callback: print article id
def download_news_from_urls(news_href, callback=None):
    def default_callback(_, article_id):
        print article_id

    def download_thread(url):
        try:
            article, article_id = download_news(url)
            callback(article, article_id)
        except:
            print "error for %s" % url

    if callback is None:
        callback = default_callback
    n = len(news_href)
    l_threads = [threading.Thread(target=download_thread, args=[news_href[i]]) for i in range(n)]
    batch_run(l_threads)


def download_naver_news_date_range(str_sid1, dt_org, dt_end, callback=None):
    max_threads = 5
    pool_sema = threading.BoundedSemaphore(value=max_threads)
    dic_news_href = {}

    def get_news_href_sid_date_threaded(str_sid1_, str_date_):
        pool_sema.acquire()
        news_href = get_all_news_hrefs(str_sid1_, str_date_)
        dic_news_href[(str_sid1_, str_date_)] = news_href
        pool_sema.release()

    dic_news_href_threads = {}
    dt = dt_org
    while dt > dt_end:
        dt -= timedelta(days=1)
        str_date = datetime.strftime(dt, '%Y-%m-%d')
        dic_news_href_threads[str_date] = \
            threading.Thread(target=get_news_href_sid_date_threaded, args=(str_sid1, str_date))
        dic_news_href_threads[str_date].start()
    dt = dt_org
    while dt > dt_end:
        dt -= timedelta(days=1)
        str_date = datetime.strftime(dt, '%Y-%m-%d')
        print str_date
        dic_news_href_threads[str_date].join()
        download_news_from_urls(dic_news_href[(str_sid1, str_date)], callback)
