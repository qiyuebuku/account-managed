from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox,QListWidget,QListWidgetItem, QStatusBar,  QMenuBar,QMenu,QAction,QLineEdit,QStyle,QFormLayout,   QVBoxLayout,QWidget,QApplication ,QHBoxLayout, QPushButton,QGridLayout,QLabel

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import threading
import zmail
import time



class Auto_Response_Thread(QThread):   #继承父类threading.Thread
     # 定义日志显示信号
    Log_Signal = pyqtSignal(str,str)
    def __init__(self,config,cls):
        super().__init__()
        self.flag=True
        # print(config)
        self.config=config
        self.cls=cls
        self.user=cls.em_user.text()
        self.pwd=cls.em_pwd.text()
        # self.server=zmail.server(self.user,self.pwd)          

    #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
    def run(self):   
        server=zmail.server(self.user,self.pwd)  
        mail_count=server.stat()[0]
        last_count=mail_count    
        server=zmail.server(self.user,self.pwd)
        while True:
            print('--------------------------')
            if self.flag==False:
                break
            email_address_list=[]
            try:
                current_count=server.stat()[0]
            except:
                print('出现异常，重新登录')
                server=zmail.server(self.user,self.pwd)
            if current_count>last_count:
                if not self.config['is_reply_all']:
                    for i in range(last_count+1,current_count+1):
                        mail=server.get_mail(i)
                        From=mail['From']
                        start=From.find("<")+1
                        end=From.find(">")
                        from_email=[From[start:end]] 
                        print(from_email)
                        print(self.config['recipient'].split(","))
                        s1=set(from_email)
                        s2=set(self.config['recipient'].split(","))
                        print(s1,s2,sep='\n')
                        print(list(s1 & s2))
                        self.Log_Signal.emit('接收到来自%s的消息：%s'
                        %(
                            from_email,
                            mail['subject']),
                            'purple'
                            )                    
                        email_address_list.append("".join(list(s1 & s2)))
                    self.send_email(email_address_list,server)                    
                else:
                    for i in range(last_count+1,current_count+1):
                        mail=server.get_mail(i)
                        From=mail['From']
                        start=From.find("<")+1
                        end=From.find(">")

                        self.Log_Signal.emit('接收到来自%s的消息：%s'
                        %(
                            From[start:end],
                            mail['subject']),
                            'purple'
                            )
                        email_address_list.append(From[start:end])                        

                    self.send_email(email_address_list,server)
            last_count=current_count
            time.sleep(1)
    def stop(self):
        self.flag=False


    def send_email(self,email_address_list,server):
        config=self.config
        mail = {
        'subject': config['subject'],  # Anything you want.
        'content_html' if config['text_type']=='html' else 'content_text' : config['content'],  # Anything you want.
        }
        if len(config['attachment_paths']):
            mail['attachments']=config['attachment_paths'] 
        self.Log_Signal.emit('自动回复消息到%s'%''.join(email_address_list),'purple')
        server.send_mail(email_address_list,mail)





class Auto_Window(object):
    def __init__(self,cls):
        super().__init__()
        self.cls=cls
        cls.set_progressBar(20)

        #是否开启自动回复
        self.auto_reply_thread=None

        self.reply_status=False #自动回复标志初始化为关

        cls.em_auto_attachment.clicked.connect(self.check)#单击附件时选中某一个选项

        #创建右键菜单
        # 必须将ContextMenuPolicy设置为Qt.CustomContextMenu
        # 否则无法使用customContextMenuRequested信号
        self.cls.setContextMenuPolicy(Qt.CustomContextMenu)


        # 创建QMenu
        cls.em_auto_contextMenu = QMenu()
        cls.em_auto_actionA = cls.em_auto_contextMenu.addAction(QIcon("images/0.png"), u'|  删除')

        # 显示菜单
        cls.customContextMenuRequested.connect(self.showContextMenu)

        #点击删除menu
        cls.em_auto_contextMenu.triggered[QAction].connect(self.remove)



        cls.em_auto_add_attachment.clicked.connect(self.__add_attachment)
        cls.em_auto_import_file_content.clicked.connect(self.__read_content)
        cls.em_auto_import_file_recipient.clicked.connect(self.__read_recipient)
        cls.em_auto_start_reply.clicked.connect(self.__start_reply)
        cls.em_auto_reply_all.clicked.connect(self.__set_recipients_enabled)

    def __add_attachment(self):
        self.cls.add_log_msg('添加附件','blue')
        file_paths,is_ok=QFileDialog.getOpenFileNames(self.cls,'添加附件','./')
        if is_ok:
            self.cls.em_auto_attachment.addItems(file_paths)
        else:
            self.cls.add_log_msg('取消添加附件','red')

    def __read_content(self):
        self.cls.add_log_msg('添加正文','blue')
        file_path,is_ok=QFileDialog.getOpenFileName(self.cls,'添加正文','./')
        if is_ok:
            print(file_path,is_ok,sep='\n')
            with open(file_path,'r',encoding='utf-8') as f:
                content=f.read()
            self.cls.em_auto_content.setText(content)
        else:
            self.cls.add_log_msg('取消添加','red')


    def __read_recipient(self):
        self.cls.add_log_msg('读取特定回复者','blue')
        file_path,is_ok=QFileDialog.getOpenFileName(self.cls,'添加自动回复目标','./')
        if is_ok:
            print(file_path,is_ok,sep='\n')
            with open(file_path,'r',encoding='utf-8') as f:
                recipient=f.read()
            self.cls.em_auto_recipients.setText(recipient)
        else:
            self.cls.add_log_msg('取消添加','red')

    def __start_reply(self):
        cls=self.cls

        if self.reply_status:
            self.auto_reply_thread.stop()
            self.reply_status=False
            self.set_auto_enabled(True)
            cls.add_log_msg('关闭自动回复','red')
            cls.em_auto_start_reply.setText('开启自动回复')

        else:
            if not len(cls.em_auto_content.toPlainText()):
                cls.add_log_msg('正文内容不能为空！！！','red')
            recipient=cls.em_auto_recipients.text()
            subject=cls.em_auto_subject.text()
            text_type='text' if cls.em_auto_text.isChecked() else 'html'
            content=cls.em_auto_content.toPlainText() if text_type=='text' else cls.em_auto_content.toHtml()
            is_reply_all=cls.em_auto_reply_all.isChecked()
            attachment_paths=self.get_attachment_text(cls)
            
            config={
                'recipient':recipient,
                'subject':subject,
                'content':content,
                'text_type':text_type,
                'is_reply_all':is_reply_all,
                'attachment_paths':attachment_paths
            }
            self.reply_status=True
            self.set_auto_enabled(False)
            self.auto_reply_thread=Auto_Response_Thread(config,cls)
            self.auto_reply_thread.Log_Signal.connect(cls.add_log_msg)#注册日志显示信号
            self.auto_reply_thread.start()
            cls.em_auto_start_reply.setText('关闭自动回复')
            cls.add_log_msg('开启自动回复','black')

          



            

    def __set_recipients_enabled(self):
        cls=self.cls
        is_reply_all=cls.em_auto_reply_all.isChecked()
        cls.em_auto_recipients.setEnabled(not is_reply_all)
        cls.em_auto_import_file_recipient.setEnabled(not is_reply_all)

    def check(self,index):
        '''
        获取当前选中的时第几行
        '''
        r=index.row()
        self.f=r
        print(r)

    def get_attachment_text(self,cls):
         #获取子项的个数
        item_count=cls.em_auto_attachment.count() 
        attachment_paths=[]
        for row in range(item_count):
            attachment_paths.append(cls.em_auto_attachment.item(row).text())
        return attachment_paths

    def showContextMenu(self):
        print('auto')
        cls=self.cls
        #如果有选中项，则显示显示菜单
        items=cls.em_auto_attachment.selectedIndexes()
        if items:
          cls.em_auto_contextMenu.show()
          cls.em_auto_contextMenu.exec_(QCursor.pos())  # 在鼠标位置显示
    def remove(self,qAction):
        cls=self.cls
        #self.view.takeItem(self.f)#删除行(实际上是断开了与list的联系)

        #注意：removeItemWidget(self, QListWidgetItem)  # 移除一个Item，无返回值
        #注意：takeItem(self, int)  # 切断一个Item与List的联系，返回该Item
        cls.em_auto_attachment.removeItemWidget(cls.em_auto_attachment.takeItem(self.f))  #删除
    def set_auto_enabled(self,status):
        cls=self.cls
        cls.em_auto_add_attachment.setEnabled(status)
        cls.em_auto_import_file_content.setEnabled(status)
        cls.em_auto_import_file_recipient.setEnabled(status)
        cls.em_auto_reply_all.setEnabled(status)
        cls.em_auto_recipients.setEnabled(status)
        cls.em_auto_subject.setEnabled(status)
        cls.em_auto_content.setEnabled(status)
        cls.em_auto_attachment.setEnabled(status)
        cls.em_auto_html.setEnabled(status)
        cls.em_auto_text.setEnabled(status)




    def __del__(self):
        print('析构方法被调用')
        if self.reply_status:
            print('自动回复线程被关闭')
            self.auto_reply_thread.stop()




        

# window=Window()
