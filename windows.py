# _*_ coding : utf-8 _*_
import json
import re
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext
from PIL import Image, ImageTk

import requests

import utils
import htmlUtils


class ScrollFrame(tk.Frame):
    # 滑动窗口
    def __init__(self, parent):
        super().__init__(parent)  # create a frame (self)

        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")  # place canvas on self
        self.viewPort = tk.Frame(self.canvas,
                                 background="#ffffff")  # place a frame on the canvas, this frame will hold the child widgets
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)  # place a scrollbar on self
        self.canvas.configure(yscrollcommand=self.vsb.set)  # attach scrollbar action to scroll of canvas

        self.vsb.pack(side="right", fill="y")  # pack scrollbar to right of self
        self.canvas.pack(side="left", fill="both", expand=True)  # pack canvas to left of self and expand to fil
        self.canvas_window = self.canvas.create_window((4, 4), window=self.viewPort, anchor="nw",
                                                       # add view port frame to canvas
                                                       tags="self.viewPort")

        self.viewPort.bind("<Configure>",
                           self.onFrameConfigure)  # bind an event whenever the size of the viewPort frame changes.
        self.canvas.bind("<Configure>",
                         self.onCanvasConfigure)  # bind an event whenever the size of the canvas frame changes.

        self.viewPort.bind('<Enter>', self.onEnter)  # bind wheel events when the cursor enters the control
        self.viewPort.bind('<Leave>', self.onLeave)  # unbind wheel events when the cursorl leaves the control

        self.onFrameConfigure(
            None)  # perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox(
            "all"))  # whenever the size of the frame changes, alter the scroll region respectively.

    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window,
                               width=canvas_width)  # whenever the size of the canvas changes alter the window region respectively.

    def onMouseWheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def onEnter(self, event):
        self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)

    def onLeave(self, event):
        self.canvas.unbind_all("<MouseWheel>")


class Example(tk.Frame):
    # html页面展示
    def __init__(self, root, lableList):

        tk.Frame.__init__(self, root)
        self.scrollFrame = ScrollFrame(self)

        for i in range(len(lableList)):
            varLable = lableList[i]
            if varLable[0] == 0:
                tk.Label(self.scrollFrame.viewPort, text=varLable[1]).grid(row=i, column=0, sticky='w')
            if varLable[0] == 1:
                img = Image.open(varLable[1])
                global photo
                photo = ImageTk.PhotoImage(img)
                tk.Label(self.scrollFrame.viewPort, image=photo).grid(row=i, column=0, sticky='w')
            if varLable[0] == 2:
                LinkLabel(self.scrollFrame.viewPort, link=varLable[1]).grid(row=i, column=0, sticky='w')
        self.scrollFrame.pack(side="top", fill="both", expand=True)

    def printMsg(self, msg):
        print(msg)


class LinkLabel(tk.Label):
    # LinkLabel可以显示超链接，实现点击跳转
    def __init__(self, master, link, font=('宋体', 13), bg='#f0f0f0'):
        super().__init__(master, text=link, font=font, fg='blue', bg=bg)
        self.link = link
        self.bind('<Enter>', self._changecolor)
        self.bind('<Leave>', self._changecurcor)
        self.bind('<Button-1>', self._golink)
        self.isclick = False  # 未被点击

    def _changecolor(self, event):
        self['fg'] = '#D52BC4'  # 鼠标进入，改变为紫色
        self['cursor'] = 'hand2'

    def _changecurcor(self, event):
        if self.isclick == False:  # 如果链接未被点击，显示会蓝色
            self['fg'] = 'blue'
        self['cursor'] = 'xterm'

    def _golink(self, event):
        self.isclick = True  # 被链接点击后不再改变颜色
        print("link:", self.link)
        address, res_url = utils.get_url(self.link)
        if address == "":
            search_inPages(var_ip.get(),res_url)
        else:
            var_ip.set(self.link)
            address, url = utils.get_url(self.link)
            search_get(address, url)

def search_inPages(old_url,url):
    # 超链接页内跳转路由
    address,_ = utils.get_url(old_url)
    search_get(address, url)
    var_ip.set("http://"+address+"/"+url)


def search_get(address, url):
    # 发送get报文，提取html
    request, head = utils.request_get(address, url)
    request_data = requests.get('http://' + address + "/" + url)
    html = request_data.text
    re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
    var_html = re_cdata.sub('', html)
    var_html = re_script.sub('', var_html)  # 去掉SCRIPT
    var_html = re_style.sub('', var_html)  # 去掉style
    # 解析html
    my = htmlUtils.MyParser()
    # print(var_html)
    my.feed(var_html)


    Example(win1, my.lableList).place(x=60, y=420)

    # 交互记录
    comment_text.insert(INSERT, 'request:\r\n' + request)
    comment_text.insert(INSERT, 'response:\r\n' + head + '\r\n' + '-' * 20 + '\r\n')


def search_head(address, url):
    var_html = ""
    request_data, recv_data = utils.request_head(address, url)
    comment_text.insert(INSERT, 'request:\r\n' + request_data)
    comment_text.insert(INSERT, 'response:\r\n' + recv_data + '\r\n' + '-' * 20 + '\r\n')


def search():
    # print("search")
    addressURL = var_ip.get()
    address, url = utils.get_url(addressURL)
    comment = v.get()
    # get 命令
    if (comment == 1):
        search_get(address, url)
    # head 命令
    if (comment == 2):
        search_head(address, url)


if __name__ == '__main__':
    win1 = tk.Tk()  # 常见窗口对象
    win1.title('Browser')  # 添加窗体名称
    win1.geometry('1300x750+100+50')  # 设置窗体大小

    var_ip = tk.StringVar()
    Label(win1, text="网页地址：", font=('Arial', 14)).place(x=30, y=20)
    ip_entry = Entry(win1, show=None, textvariable=var_ip, font=('Arial', 14))
    ip_entry.place(x=140, y=20, width=350)

    Label(win1, text="命令类型：", font=('Arial', 14)).place(x=30, y=50)
    LANGS = [('GIT', 1), ('HEAD', 2), ]
    v = IntVar()
    v.set(1)
    for lang, num in LANGS:
        b = Radiobutton(win1, text=lang, variable=v, value=num)
        b.place(x=90 + num * 50, y=50)

    Button(win1, text="Connect Test", command=search).place(x=500, y=20)
    Label(win1, text="交互过程：", font=('Arial', 14)).place(x=30, y=80)
    comment_text = scrolledtext.ScrolledText(win1, width=65, height=15, undo=True, autoseparators=False,
                                             font=('Arial', 12))
    comment_text.place(x=60, y=110, width=1220)
    Label(win1, text="连接结果：", font=('Arial', 14)).place(x=30, y=390)

    win1.mainloop()  # 执行窗体
