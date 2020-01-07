# -*- coding: utf-8 -*-
'''
获取"B站2019最美夜晚":弹幕/评论相关信息
'''
import requests
from retrying import retry
import pandas as pd
import json

#获取url
def get_url(url):
    pass

#获取info
@retry(stop_max_attempt_number=3)
def get_info(url):
    headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'
            }
    response=requests.get(url, headers=headers, timeout=10)
    html=response.content.decode()
    info = json.loads(html)
    return info

#解析info
def analysis_info(url):
    info = get_info(url)
    #获取该节目下弹幕数
    comment_num = info['data']['page']['acount']
    #获取该节目-->该页评论下的评论信息
    sex_list = []
    comment_list = []
    for i in info['data']['replies']:
        sex = i['member']['sex']
        comment = i['content']['message']
        sex_list.append(sex)
        comment_list.append(comment)
    return comment_num, sex_list, comment_list

#获取所有信息
def get_all_info(url_start):
    num = eval(url_start)[1] + 1
    url_st = eval(url_start)[0]
    sex_all_list = []
    comment_all_list = []
    for i in range(1, num):
        print(i)
        url = url_st.format(i)
        comment_num, sex_list, comment_list = analysis_info(url)
        sex_all_list.extend(sex_list)
        comment_all_list.extend(comment_list)
    result_data = {'comment_num':comment_num, 'sex':sex_all_list, 'comment':comment_all_list}
    return result_data

def main():
    df_bilibili = pd.read_excel('bilibili.xlsx')
    df_bilibili['url_start'] = df_bilibili['url_start'].apply(get_all_info)
    df_bilibili.to_csv('data/bilibili_data.csv' ,encoding='utf-8', index=False)


if __name__ == '__main__':
    main()
    
    