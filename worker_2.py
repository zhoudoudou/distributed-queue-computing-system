# -*- coding: utf-8 -*-
# @Time    : 2018/12/29 7:04 PM
# @Author  : YindaZhou
# @Email   : zhouyd@mail.ustc.edu.cn
# @File    : worker_2.py
# @Software: PyCharm Community Edition

from multiprocessing.managers import BaseManager
import numpy as np
import time


class QueueManager(BaseManager):
    pass

QueueManager.register("task")
QueueManager.register("result")
# 本代码在本地机器上测试（一台电脑），因此server的地址写成"127.0.0.1"
# 不过你的work_1.py和work_2.py的代码实在同一局域网的不同机器上，此处请写manager.py运行的机器IP地址
server_addr = "127.0.0.1"#
print("connecting to server %s" % server_addr)
worker = QueueManager(address=(server_addr, 5000), authkey=b'abc')
worker.connect()
print("conneted succeed")
task = worker.task()
result = worker.result()


while(1):
    while(task.empty()):# 判断任务队列中是否还有未执行的任务
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