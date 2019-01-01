# -*- coding: utf-8 -*-
# @Time    : 2018/12/28 5:06 PM
# @Author  : YindaZhou
# @Email   : zhouyd@mail.ustc.edu.cn
# @File    : master.py
# @Software: PyCharm Community Edition
'''
这是分布式队列计算系统的master程序，主要负责队列的维护和管理
'''
import queue
import time
from multiprocessing.managers import BaseManager

# 任务队列
# maxsize用来设置队列的最长长度
task_queue = queue.Queue(maxsize = 10)
# 结果队列
result_queue = queue.Queue(maxsize = 10)

class QueueManager(BaseManager):
    pass

QueueManager.register('task', callable=lambda: task_queue)
QueueManager.register('result', callable=lambda: result_queue)

manager = QueueManager(address=('', 5000),authkey=b'abc')
manager.start()

task = manager.task()
result = manager.result()

task_init = [0]
for i in range(10):
    task.put(task_init)

while(~result.full()):
    time.sleep(2)
    while (result.full()):
        temp = []
        print("now the result is ",result)
        # 将result的结果直接塞入task队列
        for i in range(10):
            temp.append(result.get())
        print(temp)
        for i in range(10):
            task.put(temp[0])
        break
manager.shutdown()
print("master exit")



