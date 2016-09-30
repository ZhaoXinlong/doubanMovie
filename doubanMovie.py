# -*- coding: utf-8 -*-
#coding=UTF-8
"""
Created on Thu Sep 29 16:09:12 2016

@author: furfurfur
"""
import requests,random,time
from bs4 import BeautifulSoup
import string
import sys
import xlwt
from pandas import DataFrame

name_xls = 'doubanMovie.xls'

df = DataFrame({'biaoti':['Name','Year','Link to Douban']})

#DataFrame中默认是列，不是行；因此进行转置操作，输出到Excel时与习惯保持一致   
df = df.T

headers = {
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    }
basic_url_front='https://movie.douban.com/tag/IT?start='
basic_url_back='&type=T'

page_number = 16

print basic_url_front+basic_url_back
for k in range(page_number-1):
    r = requests.get(basic_url_front+str(20*k)+basic_url_back,headers=headers)
    print basic_url_front+str(20*k)+basic_url_back
    c = r.content
    b = BeautifulSoup(c)

    data_list = b.find('div',{'class':'article'})
    data_li = data_list.findAll('div',{'class':'pl2'})
    time.sleep(round(random.random(),2))

    for i in data_li:
        name = i.find('a').get_text()
        
        name = str(name).split('/')
        name = name[0]
        #print name
        link = i.find('a').attrs['href']
        #print link
        r_temp = requests.get(link,headers=headers)
        c_temp = r_temp.content
        #movie_cont = requests.get(link,headers=headers).content
        b_temp = BeautifulSoup(c_temp)
        #中英文名称
        try:
            name_new = b_temp.find('span',{'property':'v:itemreviewed'}).get_text()
        except AttributeError:
            name_new = None
        #name_new = str(name_new).split('(')
        #print name_new
        #评分        
        try:
            score = b_temp.find('strong',{'class','ll rating_num'}).get_text()
        except AttributeError:
            score = None
        print score
        #评价人数
        try:
            rating_poeple = b_temp.find('span',{'property','v:votes'}).get_text()
        except AttributeError:
            rating_poeple = None
        print rating_poeple
        #Daria: The Movie - Is It Fall Yet?没有年份。废了。
        #IT世代-改变未来的年轻一代   没有年份
        try:
            myDate =b_temp.find('span',{'class':'year'}).get_text()
        except AttributeError:
            myDate = None        
        #date = b_temp.find('span',{'class':'year'}).get_text()
        #date = date.replace('(','')
        #date = date.replace(')','')
        print myDate
        #pandas的dataframe存储数据
        l1 = [name_new,myDate,link]
        df_temp = DataFrame({'data':l1})
        df_temp = df_temp.T
        df = df.append(df_temp)
        
df = df.drop_duplicates()
df.to_excel(name_xls,sheet_name='TAG_IT',index = False)
        