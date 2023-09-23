# -*- coding: utf-8 -*-
# 定位信息集成
import socket  # 导入socket模块
import time # 导入time模块
import re   # 导入re模块，用于正则表达式匹配
# server 接收端，电脑端监测
# 设置服务器默认端口号
PORT = 8000
# 创建一个套接字socket对象，用于进行通讯
# socket.AF_INET 指明使用INET地址集，进行网间通讯
# socket.SOCK_DGRAM 指明使用数据协议，即使用传输层的udp协议
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = ("172.20.10.10", PORT)  
server_socket.bind(address)  # 为服务器绑定一个固定的地址，ip和端口
server_socket.settimeout(10)  #设置一个时间提示，如果10秒钟没接到数据进行提示

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from matplotlib.animation import FuncAnimation

# 安装支持中文的TrueType字体，并设置为默认字体, 修复中文乱码BUG
plt.rcParams['font.sans-serif'] = ['SimHei']  # 例如，使用中文仿宋字体

field_w=750
field_h=468

# 加载足球场图像
soccer_field = mpimg.imread('soccer_field.jpg')

# 创建一个实时绘制的图像窗口
fig, ax = plt.subplots()
# 设置足球场图像的坐标范围
ax.imshow(soccer_field, extent=[0, field_w, 0, field_h])  
blue_scatter = ax.scatter([], [], c='blue', label='蓝点')
red_scatter = ax.scatter([], [], c='red', label='红点')
ax.set_title("实时坐标绘制")
ax.set_xlabel("X轴")
ax.set_ylabel("Y轴")


# 更新散点坐标的回调函数
def update(i):
    try:  
        now = time.time()  #获取当前时间
                        # 接收客户端传来的数据 recvfrom接收客户端的数据，默认是阻塞的，直到有客户端传来数据
                        # recvfrom 参数的意义，表示最大能接收多少数据，单位是字节
                        # recvfrom返回值说明
                        # receive_data表示接受到的传来的数据,是bytes类型
                        # client  表示传来数据的客户端的身份信息，客户端的ip和端口，元组
        receive_data, client = server_socket.recvfrom(1024)
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now))) #以指定格式显示时间
        print("来自客户端%s,发送的%s\n" % (client, receive_data))  #打印接收的内容

        msg_decode = receive_data.decode()
        s = re.split(r'[;,\s]\s*',msg_decode)
        robot_id = s[0]
        robot_x, robot_y = s[1], s[2]
        print(f"机器人编号是{robot_id}, 位置是({robot_x}, {robot_y})")

        if robot_id == '0':
            blue_scatter.set_offsets(np.array([[robot_x, robot_y]]))
        if robot_id == '1':
            red_scatter.set_offsets(np.array([[robot_x, robot_y]]))
        
    except socket.timeout:  #如果10秒钟没有接收数据进行提示（打印 "time out"）
        print("time out")


# 使用FuncAnimation实时更新散点坐标
ani = FuncAnimation(fig, update, interval=1000)  # 每1000毫秒更新一次
plt.show()