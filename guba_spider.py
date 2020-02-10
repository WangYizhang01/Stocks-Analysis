# -*- coding:UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import time
import re


def getHTMLText(url):
    """
    从url处获取html返回
    :param url:
    :return:
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36'}
    try:
        r = requests.get(url,headers=headers,timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def fillUnivList_comments(html):
    """
    爬取某一页上的发帖信息，以字典形式保存时间、地址、标题、内容，将所有字典保存在列表comment_result中并返回
    :param html:
    :return:
    """
    url_list = 'http://guba.eastmoney.com'
    comment_result = []
    soup = BeautifulSoup(html, "html.parser")

    for div in soup.find_all('div',attrs={'class':'articleh normal_post'}):
        try:
            time_ = div.find('span',attrs={'class':'l5 a5'}).string
            comment_url = url_list + div.find('a')['href']
            title = div.find('a')['title']
            comment = div.find('span',attrs={'class':'l3 a3'}).string
            comment_result.append({
                '时间': time_,
                '地址': comment_url,
                '标题': title,
                '内容': comment
            })
        except:
            continue
    return comment_result

def fillUnivList_news(html):
    """
    爬取某一页上的新闻信息，以字典形式保存时间、地址、标题，news_result中并返回
    :param html:
    :return:
    """
    news_result = []
    soup = BeautifulSoup(html, "html.parser")

    div = soup.find('div',attrs={'class':'datelist'})
    for a in div.find_all('a'):
        try:
            href = a['href']
            title = a.string
            match = re.search(r'\d{4}-\d{2}-\d{2}',href)

            news_result.append({
                "时间":match.group(0) if match else ' ',
                "地址":href,
                "标题":title
            })
        except:
            continue
    return news_result

def comments_spider(pages_num):
    """
    pages_num为需爬取的页数，本函数爬取前pages_num页的评论信息，并将其写入comments_result.json文件中，并返回评论条数
    :return:
    """
    url = 'http://guba.eastmoney.com/list,002415,f.html'
    url_fir = 'http://guba.eastmoney.com/list,002415,f_'

    html = getHTMLText(url)
    comment_result = fillUnivList_comments(html)

    for i in range(2,pages_num+1):
        if i > 0 and i%5 == 0:
            print("已爬取"+str(i)+'页的评论..')
        url_new = url_fir + str(i) + '.html'
        html_new = getHTMLText(url_new)
        comment_result += fillUnivList_comments(html_new)

    result = json.dumps(comment_result,ensure_ascii=False)
    with open('/Users/apple/PycharmProjects/untitled4/stock_analysis/comments_result.json', 'w') as f:
        f.write(result)

    return len(comment_result)

def news_spider(pages_num):
    """
    pages_num为需爬取的页数，本函数爬取前pages_num页的新闻信息，并将其写入news_result.json文件中，并返回新闻条数
    :param pages_num:
    :return:
    """
    news_result = []
    url = 'https://vip.stock.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol=sz002415&Page='
    for i in range(1,pages_num+1):
        if i > 0 and i%5 == 0:
            print("已爬取"+str(i)+'页的新闻....')
        url_new = url + str(i)
        html = getHTMLText(url_new)
        news_result += fillUnivList_news(html)

    result = json.dumps(news_result, ensure_ascii=False)
    with open('/Users/apple/PycharmProjects/untitled4/stock_analysis/news_result.json', 'w') as f:
        f.write(result)

    return len(news_result)


if __name__ == '__main__':

    print("----------程序开始-----------")
    print('\n',end='')
    start_time = time.time()

    len1 = comments_spider(1000)
    len2 = news_spider(40)
    print("共爬取" + str(len1) + "条评论。")
    print("共爬取" + str(len2) + "条新闻。")

    end_time = time.time()
    times = end_time - start_time
    print("运行时间：",times,"秒")
    print('\n',end='')
    print("----------程序结束-----------")