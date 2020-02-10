import json
from snownlp import SnowNLP
import time


def union_by_date(news):
    """
    把列表news中日期相同的字典合并
    :param news:
    :return:
    """
    for i in range(len(news)-1):
        if news[i]['时间'] == news[i+1]['时间']:
            news[i+1]['地址'] = news[i+1]['地址'] + ' && ' + news[i]['地址']
            news[i+1]['标题'] = news[i+1]['标题'] + ' ' + news[i]['标题']
            news[i] = {}
        else:
            continue

    for j in range(len(news)-1,-1,-1):
        if not news[j]:
            news.pop(j)
    # 删除键-'地址'
    for dict in news:
        del dict['地址']
    # 倒置列表
    res = []
    for i in range(len(news)-1,-1,-1):
        res.append(news[i])
    return res

def senti_ana(news):
    """"
    利用SnowNLP分析每天新闻的情绪值，并增加到字典中
    """
    for dict in news:
        s = SnowNLP(dict['标题'])
        dict['情绪值'] = s.sentiments
    return news


if __name__ == '__main__':

    start_time = time.time()

    # 导入数据
    with open('news_result.json', 'r', encoding='utf-8') as f:
        news = json.load(f)

    result = senti_ana(union_by_date(news))
    # 将添加了情绪值的新闻数据保存到comments_new.json中
    json_ = json.dumps(result, ensure_ascii=False)
    with open('/Users/apple/PycharmProjects/untitled4/stock_analysis/news_add_sentiments.json', 'w') as f:
        f.write(json_)

    end_time = time.time()
    times = end_time - start_time
    print("运行时间：",times,"秒")