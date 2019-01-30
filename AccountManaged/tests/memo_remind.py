from email_class import *

def memo_remind():
    g = G_email()
    subject = 'memo_remind'
    content_text = input('请输入要提醒的事：')
    g.receive_account = '1931784039@qq.com'
    g.mail_content = {'subject': subject, 'content_text': content_text}
    clock_time = input('请设置发送的时间：xxxx.xx.xx xx:xx:xx')
    date = (int(clock_time[0:4]), int(clock_time[5:7]), int(clock_time[8:10]))
    time = (int(clock_time[11:13]), int(clock_time[14:16]), int(clock_time[17:19]))
    while True:
        if (TIME.localtime())[0:3] == date and (TIME.localtime())[3:6] == time:
            g.send__email()
            break
    return 

memo_remind()

# def print_receive_account():#显示接收成员的邮箱
#     with open('email_account.txt') as account_file:
#         account_list=[]
#         while True:
#             account=account_file.readline()
#             if account == '':
#                 break
#             account=account.rstrip()
#             account_list.append(account)
#     count = 1
#     for i in account_list:
#         print('%d:%s'%(count,i))
#         count+=1
#     return account_list

# def select_receive_account(account_list):#选择接收邮箱帐号

#     count=input('请输入要接收邮箱的序号，用逗号隔开')
#     count_list=count.split(',')
#     ac_list=[]
#     for i in count_list:
#         ac_list.append(account_list[int(i)-1])
#     print(ac_list)
#     return ac_list
