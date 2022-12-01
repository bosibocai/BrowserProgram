# _*_ coding : utf-8 _*_
# 输入、补全URL
import socket
import re
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk


def get_url(url):
    urlSplit = url.split('://')
    if len(urlSplit) > 1:
        content = urlSplit[1]
        contentList = content.split('/')
        host = contentList[0]
        res_url = '/'.join(contentList[1:])
        print(host)
        print(res_url)
        return host, res_url
    else:
        return "", url[1:]

def request_get(address,res_url):
    # address,res_url = get_url(url)
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((address,80))

    request_line = 'GET /'+res_url +' HTTP/1.1\r\n'
    request_headers = 'Host: ' + address + '\r\n'
    request_data = request_line + 'Connection: keep-alive\r\n' + request_headers + 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.56\r\n' + '\r\n'

    print(request_data)
    # tcp_socket.send(request_data.encode('utf-8'))
    tcp_socket.send(request_data.encode())

    recv_data = tcp_socket.recv(102400)
    recv_data = recv_data.decode()
    # print(recv_data)
    index = recv_data.find('\r\n\r\n')       # 找到消息头与消息体分割的地方
    head = recv_data[:index]
    body = recv_data[index+4:]
    # print(head)
    # print(body)
    tcp_socket.close()
    return request_data, head

def request_head(address,res_url):
    # address,res_url = get_url(url)
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((address,80))

    request_line = 'HEAD /'+res_url +' HTTP/1.1\r\n'
    request_headers = 'Host:' + address + '\r\n'
    request_data = request_line + 'Connection: close\r\n' + request_headers + 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.56\r\n' + '\r\n'

    tcp_socket.send(request_data.encode())

    recv_data = tcp_socket.recv(10240)
    recv_data = recv_data.decode()
    # print(recv_data)
    tcp_socket.close()
    return request_data, recv_data

