import json
from snownlp import SnowNLP
import time

def union_by_date(comments):
    """
    把列表comments中日期相同的字典合并
    :param comments:
    :return:
    """
    for i in range(len(comments)-1):
        if comments[i]['时间'][:5] == comments[i+1]['时间'][:5]:
            comments[i+1]['时间'] = comments[i+1]['时间'][:5]
            comments[i+1]['地址'] = comments[i+1]['地址'] + ' && ' + comments[i]['地址']
            comments[i+1]['标题'] = comments[i+1]['标题'] + ' ' + comments[i]['标题']
            try:
                comments[i+1]['内容'] = comments[i+1]['内容'] + ' ' + comments[i]['内容']
            except:
                if isinstance(comments[i+1]['内容'],str):
                    pass
                else:
                    comments[i+1]['内容'] = comments[i]['内容']
            comments[i] = {}
        else:
            comments[i]['时间'] = comments[i]['时间'][:5]

    for j in range(len(comments)-1,-1,-1):
        if not comments[j]:
            comments.pop(j)

    for dict in comments:
        del dict['地址']
        del dict['内容']

    return comments

def time_add_year(comments):
    """
    给列表comments中的字典的时间增加年份，并按照时间顺序排序
    :param comments:
    :return:
    """
    year = 2020
    count = 0
    for i in range(len(comments)):
        if comments[i]['时间'] != '01-01':
            comments[i]['时间'] = str(year-count) + '-' + comments[i]['时间']
        else:
            comments[i]['时间'] = str(year-count) + '-' + comments[i]['时间']
            count += 1

    res = []
    for i in range(len(comments)-1,-1,-1):
        res.append(comments[i])
    return res

def senti_ana(comments):
    """"
    利用SnowNLP分析每天评论的情绪值，并增加到字典中
    """
    for dict in comments:
        s = SnowNLP(dict['标题'])
        dict['情绪值'] = s.sentiments
    return comments


if __name__ == '__main__':

    start_time = time.time()

    # 导入数据
    with open('comments_result.json', 'r', encoding='utf-8') as f:
        comments = json.load(f)

    comments_new = time_add_year(union_by_date(comments))
    # 将处理好的评论数据保存到comments_new.json中
    # json_1 = json.dumps(comments_new, ensure_ascii=False)
    # with open('/Users/apple/PycharmProjects/untitled4/stock_analysis/comments_new.json', 'w') as f:
    #     f.write(json_1)

    com_add_senti = senti_ana(comments_new)
    # 将添加了情绪值的评论数据保存到comments_new.json中
    json_2 = json.dumps(comments_new, ensure_ascii=False)
    with open('/Users/apple/PycharmProjects/untitled4/stock_analysis/comments_add_sentiments.json', 'w') as f:
        f.write(json_2)

    end_time = time.time()
    times = end_time - start_time
    print("运行时间：",times,"秒")