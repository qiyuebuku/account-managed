import zmail
import os,sys
#获取上级目录
parent_dir = os.path.dirname(os.path.dirname(__file__))
#获取当前目录
current_dir=os.path.dirname(__file__)
sys.path.append(parent_dir)
from tools import tools
import time

import os

# mail_content={
#     'subject':'测试sdfsdf',
#     'content':'我来试一下sdfdsfdsfdsfdsfdsfdsfdsfdsf',
# }

mail = {
    'from':'1194681498@qq.com',
    'subject': 'Success!',  # Anything you want.
    'content_text': 'This messsdfsdfdsfsdfage from zmail!',  # Anything you want.
    # 'attachments': [r'D:\bj\account managed\AccountManaged\tests\1.txt',r'D:\bj\account managed\bin\1.html'],  # Absolute path will be better.
}

def com_time(fun):
    def func():
        start_time=time.time()
        fun()
        print('程序执行所用时间%s'%(time.time()-start_time))
    return func


server=zmail.server('1194681498@qq.com','uudapucsczddichh')
@com_time
def f1():
    run_count=0
    while True:
        try:
            mail=server.get_latest()
            print(mail['ID'])
            run_count+=1
        except :
            print('执行次数：%s'%run_count)
            server=zmail.server('1194681498@qq.com','uudapucsczddichh')

@com_time
def f2():
    run_count=0
    while True:
        try:
            count=server.stat()
            print(count)
            run_count+=1
        except :
            print('执行次数：%s'%run_count)
            break

# def process():
#     PID=os.fork()

# zmail.show(mail)

# server.send_mail(['253862251@qq.com'],mail)
# print(tools.check_POP_SMT(server))


f1()


