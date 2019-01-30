# class postbox
import threading
import zmail
import sys
import os
import time
import random
#获取上级目录
parent_dir = os.path.dirname(os.path.dirname(__file__))
#获取当前目录
current_dir=os.path.dirname(__file__)
sys.path.append(parent_dir)
from tools import tools



class Auto_Response_Thread(threading.Thread):   #继承父类threading.Thread
    def __init__(self,config,server):
        super().__init__()
        self.flag=True
        print(config)
        self.config=config
        self.server=server

    #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
    def run(self):   
        mail_count=self.server.stat()[0]
        last_count=mail_count   
        
        while True:
            if self.flag==False:
                break
            current_count=self.server.stat()[0]
            if current_count>last_count:
                email_address_list=[]
                for i in range(last_count+1,current_count+1):
                    mail=self.server.get_mail(i)
                    zmail.show(mail)
                    print(type(mail['From']))
                    From=mail['From']
                    start=From.find("<")+1
                    end=From.find(">")
                    email_address_list.append(From[start:end])
                self.send_email(email_address_list)
            last_count=current_count
            time.sleep(3)
    def stop(self):
        self.flag=False


    def send_email(self,email_address_list):
        subject,content=self.read_email()  
        mail = {
        'subject': subject,  # Anything you want.
        'content_text' if self.config[1]==1 else 'content_html' : content,  # Anything you want.
        }
        self.server.send_mail(email_address_list,mail)

    def read_email(self):
        # with open(self.config[2],'r',encoding='utf8') as f:
        with open(self.config[2],'r',encoding='utf8') as f:

            subject=f.readline()
            content=f.read()
            print(subject,content,sep='\n')
        return subject,content
        




class AutoResponse(object):
    def __init__(self, server, config_path=parent_dir+'/config/auto_response.ini'):
        self.server = server
        self.config_path = config_path
        self.current_config=None

    def start_auto_Response(self):
        #判断配置文件是否存在
        if tools.isfile(self.config_path):
            auto_configs=tools.read_config(self.config_path)
            print('你的配置文件如下')
            for index,data in enumerate(auto_configs):
                print(index,data.split('|')[0])
            index=int(input('请选择配置文件->'))
            config=auto_configs[index].split("|")
            auto_thread=Auto_Response_Thread(config,self.server)
            print('自动回复模式已经打开')
            auto_thread.start()
            # auto_thread.stop()
        else:
            print('你没有添加任何自动回复配置，请添加配置文件')
            self.add_auto_config()
            self.start_auto_Response()

    def add_auto_config(self):
        info = []
        while True:
            self.__show_menu()
            text_type = input('请选择自动回复的文本类型(结束添加，请输入q/Q)->')
            if text_type == 'q' or text_type=='Q':
                #如果用户选择停止添加，保存用户输入的内容到文件
                tools.write_config(self.config_path, info)
                break
            file_path = input('请输入文件所在路径(绝对路径)->')
            #获取文件名
            file_name=tools.get_fielname(file_path)
            if tools.isfile(file_path):
                #将用户输入按照元组的形式添加到列表里面
                info.append((file_name,text_type,file_path))
            else:
                print('输入内容有误，请重新输入！！')

    def __show_menu(self):
        print('''
                输入“1”：普通文本类型
                输入“2”：HTML文本类型
            ''')
    

if __name__ == "__main__":
    server = zmail.server('1194681498@qq.com', 'uudapucsczddichh')
#
#     # print(mail)
#     # print('账号检测……')
#     # if tools.check_POP_SMT(server):
#     #     print('账号未开启pop或者SMT功能')
#     #     exit()
#     # mailbox_info = server.stat()
#     # print('邮件数量%s，邮件大小：%s' % (mailbox_info[0], mailbox_info[1]))
    auto = AutoResponse(server)
    auto.add_auto_config()

    auto.start_auto_Response()

    # choose=
    # for k,v in mail.items():
    #     print(k,v)
    # print('''
    #         邮箱托管专区

    #     输入"1" ：邮件群发设置
    #     输入"2" ：自动回复设置
    #     输入"3) ：扩展功能设置
    #     输入"4) ：天气预报设置
    #     输入"5) ：特别关心设置
    #     输入"6) ：备忘提醒设置
    # ''')
