# -*- coding: utf-8 -*-
'''
处理获取的数据
'''
import pandas as pd
import jieba

#处理整体
def deal_data(url_start):
    return eval(url_start)

#处理弹幕（组合弹幕再jieba分词）
def deal_comment(comment):
    comment_str = '。'.join(comment)#弹幕列表变字符串
    comment = jieba.lcut(comment_str)#jieba分词
    comment = ' '.join(comment)#再组合成以空格分割的字符串
    return comment

def get_data():
    bilibili_data = pd.read_csv('bilibili_data.csv', encoding='utf-8').reset_index(drop=False)
    bilibili_data['url_start'] = bilibili_data['url_start'].apply(deal_data)
    bilibili_data.columns=['index','chapter', 'program', 'bilibili_data']
    data = pd.DataFrame(bilibili_data['bilibili_data'].to_list()).reset_index(drop=False)
    data['comment'] = data['comment'].apply(deal_comment)
    bilibili_data = pd.merge(bilibili_data, data, how='left', on='index')
    bilibili_data = bilibili_data[['chapter', 'program', 'comment', 'comment_num', 'sex']]
    bilibili_data.to_csv('data/bilibili_all_data.csv' ,encoding='utf-8', index=False)

#计算整体数据
def calculation_whole(bilibili_all_data):
    #获得制作整体词云数据
    whole_comment = bilibili_all_data['comment'].to_list()
    whole_comment_str = ' '.join(whole_comment)
    with open('data/whole_comment.txt', 'w', encoding='utf-8') as f:
        f.write(whole_comment_str)
    #整体性别占比
    whole_sex = bilibili_all_data['sex']
    whole_sex_list = []
    for sex in whole_sex:
        whole_sex_list.extend(eval(sex))
    df_whole_sex = pd.DataFrame([whole_sex_list]).T
    df_whole_sex.columns = ['whole_sex']
    df_whole_sex['num'] = 1
    df_whole_sex = df_whole_sex.groupby('whole_sex').sum().reset_index(drop=False)
    df_whole_sex.to_csv('data/whole_sex.csv', encoding='utf-8', index=False)
    print(df_whole_sex)
    return df_whole_sex
    
#计算节目关注度排行
def follow_rank(bilibili_all_data):
    df_follow_data = bilibili_all_data[['chapter', 'program', 'comment_num']]
    df_follow_rank = df_follow_data.sort_values(by=['comment_num'], ascending=False).reset_index(drop=True)
    df_follow_rank['rank'] = df_follow_rank['comment_num'].rank(ascending=False)
    df_follow_rank.to_csv('data/follow_rank.csv', encoding='utf-8', index=False)
    print(df_follow_rank)
    return df_follow_rank

#计算最受关注的节目数据
def most_concerned(bilibili_all_data):
    most_concerned_data = bilibili_all_data.loc[18,:]
    #制作词云数据
    most_comment_str = most_concerned_data['comment']
    with open('data/most_comment.txt', 'w', encoding='utf-8') as f:
        f.write(most_comment_str)
    #性别占比数据
    most_sex = eval(most_concerned_data['sex'])
    df_most_sex = pd.DataFrame([most_sex]).T
    df_most_sex.columns = ['most_sex']
    df_most_sex['num'] = 1
    df_most_sex = df_most_sex.groupby('most_sex').sum().reset_index(drop=False)
    df_most_sex.to_csv('data/most_sex.csv', encoding='utf-8', index=False)
    print(df_most_sex)
    return df_most_sex
    
if __name__ == '__main__':
    #清洗数据
    #get_data()
    bilibili_all_data = pd.read_csv('data/bilibili_all_data.csv', encoding='utf-8')
    print(bilibili_all_data['comment_num'].sum())
    #计算获得整体数据
    #df_whole_sex = calculation_whole(bilibili_all_data)
    #计算获得最受欢迎的节目数据
    #df_follow_rank = follow_rank(bilibili_all_data)
    #计算最受关注的节目数据
    #df_most_sex = most_concerned(bilibili_all_data)
    