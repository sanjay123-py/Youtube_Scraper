import os
import re
import time
import json
import urllib.request
import requests
import ast
import urllib3
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request as urq
from flask import jsonify
from selenium.webdriver.common.by import By
from pytube import YouTube
from flask import Flask ,render_template,request
import mysql.connector as conn
import pymongo
import pydrive
app=Flask(__name__)
def scroll_to_end(wd):
    wd.execute_script("window.scrollTo(0, document.body.scrollHeight || document.documentElement.scrollHeight);")
    time.sleep(2)
@app.route('/')
def video_selection(channel_name):
    # content=''
    # with webdriver.Chrome('./chromedriver') as wd:
    #     path='https://www.youtube.com/results?search_query='
    #     wd.get(path+"+".join(channel_name.split()))
    #     content=wd.page_source.encode('utf-8').strip()


    wd=webdriver.Chrome(executable_path='./chromedriver')
    path = 'https://www.youtube.com/results?search_query='
    wd.get(path+"+".join(channel_name.split()))
    time.sleep(1)
    content=wd.page_source.encode('utf-8').strip()
    bscontent=BeautifulSoup(content,'lxml')
    ret=bscontent.find(text=re.compile('responseContext.*'))
    js1=json.loads(ret[20:].replace(';',''))
    channel_home_page="https://www.youtube.com"+js1['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['channelRenderer']['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']+'/videos'
    wd.get(channel_home_page)
    time.sleep(2)
    scroll_to_end(wd)

    home_page_content=wd.page_source.encode('utf-8').strip()
    home_bs_content=BeautifulSoup(home_page_content,'lxml')
    anchor_title=home_bs_content.find_all('a',id='video-title')
    title=[]
    for i in anchor_title:
        title.append(i.text)

    views_content=home_bs_content.find_all('span',class_="style-scope ytd-grid-video-renderer")
    views=[]
    time1=[]
    for i in range(0,len(views_content)):
        if(i%2==0):views.append(views_content[i].text)
        else:time1.append(views_content[i].text)
    individual_video_link=[]
    comment_per_videos = []
    likes_per_video=[]
    len_comment = []
    for link in anchor_title:
        individual_video_link.append(link['href'])
        full_link_dup=[]
    for link in individual_video_link[:10]:
        comment=[]
        full_link=f'https://www.youtube.com/{link}'
        full_link_dup.append(full_link)
        wd.get(full_link)
        time.sleep(3)
        wd.execute_script('window.scrollTo(0,500);')
        time.sleep(2)
        req_content=wd.page_source.encode('utf-8').strip()
        req_bs_content=BeautifulSoup(req_content,'lxml')
        req_like=req_bs_content.select("#top-level-buttons-computed #text")
        req_comment=req_bs_content.select('#content #content-text')
        len_comment.append(len(req_comment))
        time.sleep(1)
        try:
            likes_per_video.append(req_like[0].text)
            comment=[x.text for x in req_comment]
            comment_per_videos.append(comment)
        except:
            pass
    connection=conn.connect(host='localhost',user='root',passwd='daisy2017',db='Youtube')
    cursor=connection.cursor()
    for video_link,video_title,view,post_date,likes,length in zip(full_link_dup,title[:10],views[:10],time1[:10],likes_per_video[:10],len_comment[:10]):
        cursor.execute("insert into youtube_data values(%s,%s,%s,%s,%s,%s,%s);",(str(channel_name),video_link,str(video_title),str(view),str(post_date),likes,length))
        connection.commit()
# video_selection('krish naik')





'''DOWNLOAD SECTION'''
#
# def download_video(path):
#     try:
#         yt=YouTube(path)
#         # # yt.streams.first().download()
#         # for i,j in enumerate(yt.streams):
#         #     print(i,j)
#         mp4files=yt.streams.filter(file_extension='mp4')
#         print(mp4files.get_by_resolution("720p"))
#     except Exception as e:
#         print(e)

# download_video('https://www.youtube.com/watch?v=dPARXQO8dkw')

#
# if __name__ =='__main__':
#     app.run(port=5001)
#


def image_download(image_links,channel_name):
    if(not os.path.exists('./images')):
        os.makedirs("./images")
    target_path=os.path.join('./images',"_".join(channel_name.lower().split(' ')))
    if(not os.path.exists(target_path)):
        os.makedirs(target_path)
    for i,j in enumerate(image_links,len(image_links)):
        image_content=requests.get(str(j)).content
        f=open(os.path.join(target_path+'/'+"_"+str(i)+'.jpg'),'wb')
        f.write(image_content)




# x=dup()
# print(len(x))
# for i in x:
#     print(i)

















# js1=json.loads(x[20:].replace(';',''))
# print(js1['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['channelRenderer']['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url'])
# print(js1['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['channelRenderer']['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url'])
'''year gap between my education for financial reasons, 
and was scared I won't get offers on campus, I didn't, but I got good at programming in 6 months,
 going from discrete maths all the way to comp coding. Confident I can crack any job I'm in my 7th sem, 
 no on campus offers but offcampus 17 lpa, all self study , 
 free moocs some tough books and selfless mentors like you'''
#sample code
'''
content1=[]
while(True):
    if(len(content1<1):
        wd.get('')
        content = wd.page_source.encode('utf-8').strip()
        bs=BeautifulSoup(content,'lxml')
        res=bs.select("#content")
        time.sleep(10)
        content1.append(res);
'''

wd = webdriver.Chrome(executable_path='./chromedriver')
wd.get('https://www.youtube.com/user/krishnaik06/videos')
content=wd.page_source.encode('utf-8')
bscontent=BeautifulSoup(content,'lxml')
time.sleep(2)
scroll_to_end(wd)
scrap_content=wd.find_elements(By.XPATH,'//*[@id="dismissible"]/ytd-thumbnail/a/yt-img-shadow/img')
# scrap_content=bscontent.select("#dismissible #thumbnail #img")
time.sleep(4)
for i in scrap_content:
    print(i.get_attribute('src'))
wd.close()