# -*- coding: utf-8 -*-
# @Time    : 2018/12/29 7:04 PM
# @Author  : YindaZhou
# @Email   : zhouyd@mail.ustc.edu.cn
# @File    : worker_1.py
# @Software: PyCharm Community Edition


from multiprocessing.managers import BaseManager
import numpy as np
import time

class QueueManager(BaseManager):
    pass

QueueManager.register("task")
QueueManager.register("result")

server_addr = "127.0.0.1"
print("connecting to server %s" % server_addr)
m = QueueManager(address=(server_addr, 5000), authkey=b'abc')
m.connect()
print("conneted succeed")

task = m.task()
result = m.result()
while(1):
    while(task.empty()):
        time.sleep(1)
    time.sleep(np.random.rand())
    # 从任务队列中去任务
    # 对list进行处理
    share_list = task.get()
    share_list[0] += 1
    print("Complete a calculation task")
    # 处理完毕
    # 将处理后的结果塞进结果队列
    result.put(share_list)