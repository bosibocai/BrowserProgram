# _*_ coding:utf-8 _*_
from html.parser import HTMLParser
import requests

def get_image_name(url):
    strList = url.split('/')

    img_type=strList[-1].split('.')[-1]
    print(img_type)
    return strList[-1],img_type
    
def save_img(url):
    res = requests.get(url)
    name,img_type=get_image_name(url)
    img_path = ""
    if(img_type=='jpg'):
        img_path = './img/'+name
        with open(img_path, 'wb') as f:
            f.write(res.content)
    return img_path
    

class MyParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.lableList=[]
    
    def handle_data(self, data):
        data1 = data.strip()
        if(data1 != ''):
            self.lableList.append((0,data))
            # print(data)
            
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name,value in attrs:
                if name == 'href':
                    self.lableList.append((2,value))
                    print('a: ',value)
        if tag == 'img':
            for name,value in attrs:
                if name == 'src':
                    img_path = save_img(value)
                    if(img_path!=""):
                        self.lableList.append((1,img_path))
                        print('img: ',value)
        
# my = MyParser()
# my.feed(htmlStr)
# save_img('http://cn.razerzone.com/assets/2022-touts/CN_touts-2022-JD_03.jpg')
