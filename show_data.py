# -*- coding: utf-8 -*-
'''
用于可视化数据
1、词云用python生成
2、其他图表使用power bi生成
'''
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

#生成整体弹幕词云
def wordcloud(file_path, img_path, save_path):
    words = open(file_path,'r',encoding='utf-8').read()
    #图片样式
    cloud_mask = np.array(Image.open(img_path))
    #绘制图云
    wordcloud = WordCloud(
                    background_color="white",#背景颜色
                    font_path='simhei.ttf',#字体
                    mask=cloud_mask,#图像
                    width=2000,
                    height=1000,
                   ).generate(words)
    #提取图片的色彩
    image_colors = ImageColorGenerator(cloud_mask)
     #词云展示，参数为：匹配原图色彩
    plt.imshow(wordcloud.recolor(color_func=image_colors))
    plt.axis("off")
    #保存词云
    wordcloud.to_file(save_path)

if __name__ == '__main__':
    #总体词云
    #wordcloud('data/whole_comment.txt', 'data/whole_img.jpeg', 'data/whole.png')
    
    #最受关注的节目词云
    wordcloud('data/most_comment.txt', 'data/whole_img.jpeg', 'data/most.png')
    #其他图表使用power bi做
    


