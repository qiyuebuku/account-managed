# 创建一个email对象，通过接口获取它的内容和邮件信息然后发送出去
import time
class G_email():

    def __init__(self,server):
        self.__mail_content={}
        self.__receive_account=[]
        self.server=server


    @property 
    def mail_content(self):
        '''getter'''
        return self.__mail_content

    @mail_content.setter  
    def mail_content(self,email_dict):
        '''setter'''
        self.__mail_content=email_dict   

    @property
    def receive_account(self):
        '''getter'''
        return self.__receive_account

    @receive_account.setter
    def receive_account(self,account_list):
        '''setter'''
        self.__receive_account=account_list

    def send__email(self):

        self.server.send_mail(self.__receive_account,self.__mail_content)
    
    def clocking_send(self,m=00,n=00):
        while True:
            c=time.localtime()
            time.sleep((int(m)-c[3])*3600+(int(n)-c[4])*60)
            self.send__email()
            return

    def everyday_send(self,flag=False):
        while True:
            if not flag:
                time.sleep(86400)
                self.send__email()
                return

