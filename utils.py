# _*_ coding:utf-8 _*_
# 输入、补全URL
import socket
import re
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk


def get_url(url):
    urlSplit = url.split('://')
    content = url.split('://')[1]
    contentList = content.split('/')
    host = contentList[0]
    res_url = '/'.join(contentList[1:])
    print(host)
    print(res_url)
    return host, res_url

def request_get(url):
    address,res_url = get_url(url)
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((address,80))

    request_line = 'GET /'+res_url +' HTTP/1.1\r\n'
    request_headers = 'Host: ' + address + '\r\n'
    request_data = request_line + 'Connection: keep-alive\r\n' + request_headers + 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.56\r\n' + '\r\n'

    print(request_data)
    tcp_socket.send(request_data.encode('utf-8'))

    recv_data = tcp_socket.recv(102400)
    recv_data = recv_data.decode()
    # print(recv_data)
    index = recv_data.find('\r\n\r\n')       # 找到消息头与消息体分割的地方
    head = recv_data[:index]
    body = recv_data[index+4:]
    # print(head)
    # print(body)
    tcp_socket.close()
    return request_data, head, body

def request_head(url):
    address,res_url = get_url(url)
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((address,80))

    request_line = 'HEAD /'+res_url +' HTTP/1.1\r\n'
    request_headers = 'Host:' + address + '\r\n'
    request_data = request_line + 'Connection: close\r\n' + request_headers + 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.56\r\n' + '\r\n'

    tcp_socket.send(request_data.encode('utf-8'))

    recv_data = tcp_socket.recv(10240)
    recv_data = recv_data.decode()
    # print(recv_data)
    tcp_socket.close()
    return request_data, recv_data

# get_url("https://blog.csdn.net/")
# request_get('http://cn.razerzone.com/assets/2022-home/CN_homepage-2022-pokemon(1).jpg')
# request_head('www.jianshu.com')

# class ScrollFrame(tk.Frame):
#     def __init__(self, parent):
#         super().__init__(parent) # create a frame (self)
#
#         self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")          #place canvas on self
#         self.viewPort = tk.Frame(self.canvas, background="#ffffff")                    #place a frame on the canvas, this frame will hold the child widgets
#         self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview) #place a scrollbar on self
#         self.canvas.configure(yscrollcommand=self.vsb.set)                          #attach scrollbar action to scroll of canvas
#
#         self.vsb.pack(side="right", fill="y")                                       #pack scrollbar to right of self
#         self.canvas.pack(side="left", fill="both", expand=True)                     #pack canvas to left of self and expand to fil
#         self.canvas_window = self.canvas.create_window((4,4), window=self.viewPort, anchor="nw",            #add view port frame to canvas
#                                   tags="self.viewPort")
#
#         self.viewPort.bind("<Configure>", self.onFrameConfigure)                       #bind an event whenever the size of the viewPort frame changes.
#         self.canvas.bind("<Configure>", self.onCanvasConfigure)                       #bind an event whenever the size of the canvas frame changes.
#
#         self.viewPort.bind('<Enter>', self.onEnter)                                 # bind wheel events when the cursor enters the control
#         self.viewPort.bind('<Leave>', self.onLeave)                                 # unbind wheel events when the cursorl leaves the control
#
#         self.onFrameConfigure(None)                                                 #perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize
#
#     def onFrameConfigure(self, event):
#         '''Reset the scroll region to encompass the inner frame'''
#         self.canvas.configure(scrollregion=self.canvas.bbox("all"))                 #whenever the size of the frame changes, alter the scroll region respectively.
#
#     def onCanvasConfigure(self, event):
#         '''Reset the canvas window to encompass inner frame when required'''
#         canvas_width = event.width
#         self.canvas.itemconfig(self.canvas_window, width = canvas_width)            #whenever the size of the canvas changes alter the window region respectively.
#
#     def onMouseWheel(self, event):                                                  # cross platform scroll wheel event
#         # if platform.system() == 'Windows':
#         self.canvas.yview_scroll(int(-1* (event.delta/120)), "units")
#         # elif platform.system() == 'Darwin':
#         #     self.canvas.yview_scroll(int(-1 * event.delta), "units")
#         # else:
#         #     if event.num == 4:
#         #         self.canvas.yview_scroll( -1, "units" )
#         #     elif event.num == 5:
#         #         self.canvas.yview_scroll( 1, "units" )
#
#     def onEnter(self, event):                                                       # bind wheel events when the cursor enters the control
#         # if platform.system() == 'Linux':
#         #     self.canvas.bind_all("<Button-4>", self.onMouseWheel)
#         #     self.canvas.bind_all("<Button-5>", self.onMouseWheel)
#         # else:
#         self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)
#
#     def onLeave(self, event):                                                       # unbind wheel events when the cursorl leaves the control
#         # if platform.system() == 'Linux':
#         #     self.canvas.unbind_all("<Button-4>")
#         #     self.canvas.unbind_all("<Button-5>")
#         # else:
#         self.canvas.unbind_all("<MouseWheel>")
#
# class Example(tk.Frame):
#     def __init__(self, root,lableList):
#
#         tk.Frame.__init__(self, root)
#         self.scrollFrame = ScrollFrame(self) # add a new scrollable frame.
#
#         # Now add some controls to the scrollframe.
#         # NOTE: the child controls are added to the view port (scrollFrame.viewPort, NOT scrollframe itself)
#         # for row in range(10):
#         #     a = row
#         #     tk.Label(self.scrollFrame.viewPort, text="%s" % row).grid(row=row, column=0)
#
#         for i in range(len(lableList)):
#             varLable = lableList[i]
#             if (varLable[0]==0):
#                 tk.Label(self.scrollFrame.viewPort, text=varLable[1]).grid(row=i,column=0,sticky='w')
#             if (varLable[0]==1):
#                 img = Image.open(varLable[1])
#                 global photo
#                 photo = ImageTk.PhotoImage(img)
#                 tk.Label(self.scrollFrame.viewPort, image=photo).grid(row=i,column=0,sticky='w')
#             if (varLable[0] == 2):
#                 LinkLabel(self.scrollFrame.viewPort, link=varLable[1]).grid(row=i,column=0,sticky='w')
#         self.scrollFrame.pack(side="top", fill="both", expand=True)
#
#     def printMsg(self, msg):
#         print(msg)
#
#
# class LinkLabel(Label):
#     # LinkLabel可以显示超链接
#     def __init__(self, master, link, font=('宋体', 13), bg='#f0f0f0'):
#         super().__init__(master, text=link, font=font, fg='blue', bg=bg)
#         self.link = link
#         self.bind('<Enter>', self._changecolor)
#         self.bind('<Leave>', self._changecurcor)
#         self.bind('<Button-1>', self._golink)
#         self.isclick = False  # 未被点击
#
#     def _changecolor(self, event):
#         self['fg'] = '#D52BC4'  # 鼠标进入，改变为紫色
#         self['cursor'] = 'hand2'
#
#     def _changecurcor(self, event):
#         if self.isclick == False:  # 如果链接未被点击，显示会蓝色
#             self['fg'] = 'blue'
#         self['cursor'] = 'xterm'
#
#     def _golink(self, event):
#         self.isclick = True  # 被链接点击后不再改变颜色
#         print("link:",self.link)
#         return self.link
