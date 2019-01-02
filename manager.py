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
# 以上两个队列，之后会以"task"和"result"的别名，在整个局域网内共享
# 只要与主机进行连接，便可随时对这两个列表进行操作，且列表是绝对干净的

class QueueManager(BaseManager):
    pass
# 将任务队列task_queue和result_queue进行注册，并分别取名为task和result
# 并将其暴露在局域网内
QueueManager.register('task', callable=lambda: task_queue)
QueueManager.register('result', callable=lambda: result_queue)
manager = QueueManager(address=('', 5000),authkey=b'abc')
manager.start()
task = manager.task()
result = manager.result()

# 这里我们设计了一个非常简单的例子来进行我们的验证和理解我们的计算系统
# 我们的任务是，初始化10个list，每个list的里面有一个0值[0]（我们将其定义为任务,共计10个)
# 我们利用局域网的上的计算设备(本例两台),分别对这个10个list进行进行+1操作
#
#
task_init = [0] #初始化单个任务
# 将其循环塞入任务队列中，从而形成具有10个待执行任务的任务队列
# 此时因为任务队列（task）的里面的任务尚未被执行，因此结果队列（result）为空
for i in range(10):
    task.put(task_init)


while(~result.full()):# 检测结果队列队列是否满，结果队列如果full的话，说明所有任务已经处理完毕
    time.sleep(2)
    while (result.full()): # 如果结果队列满了，说明任务队列已经处理完毕，我们可以对结果队列进行一些处理，从而生成新的任务
        temp = []
        print("now the result is ",result)
        # 实际中，我们可能会在结果队列的基础上，做一定的操作，再生成新的任务队列
        # 此处为了简化，直接将结果队列，一一弹出，塞入任务队列
        for i in range(10):
            temp.append(result.get())
        print(temp)
        for i in range(10):
            task.put(temp[0])
        break
manager.shutdown()
print("master exit")



