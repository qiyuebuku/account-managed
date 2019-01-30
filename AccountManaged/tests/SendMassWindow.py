from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox,QListWidget,QListWidgetItem, QStatusBar,  QMenuBar,QMenu,QAction,QLineEdit,QStyle,QFormLayout,   QVBoxLayout,QWidget,QApplication ,QHBoxLayout, QPushButton,QGridLayout,QLabel

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import threading
import zmail
import time
from AccountManaged.tests.email_class import *
# from account.AccountManaged.tests.email_class import *





class Clock_Send_Thread(QThread):
    # 定义日志显示信号
    Log_Signal = pyqtSignal(str,str)
    def __init__(self,config,cls):
        super().__init__()
        self.config=config #发送信息
        self.cls=cls
        self.server=cls.server#获取serve
        self.flag=True#是否开启定时发送
        print(config['timing_time'])
    

    def run(self):
        while True:
            if not self.flag:
                break
            print('定时发送启动')
            g = G_email(self.server)
            g.receive_account=self.config['recipient'].split(',')
            del self.config['recipient']
            if self.config['attachment_paths'] == []:
                del self.config['attachment_paths']
            if self.config['text_type']=='text':
                self.config['content_text'] = self.config['content']
            else:
                self.config['content_html'] = self.config['content']
            del self.config['content']
            g.mail_content=self.config
            s=self.config['timing_time'].split(':')
            g.clocking_send(s[0],s[1])
    def stop(self):
        self.flag=False

class Send_Thread(QThread):
    # 定义日志显示信号
    Log_Signal = pyqtSignal(str,str)
    def __init__(self,config,cls):
        super().__init__()
        self.config=config
        self.cls=cls
        self.server=cls.server#获取serve
    def run(self):
        self.Log_Signal.emit('ssssss','red')
        g = G_email(self.server)
        g.receive_account=self.config['recipient'].split(',')
        del self.config['recipient']
        if self.config['attachment_paths'] == []:
            del self.config['attachment_paths']
        if self.config['text_type']=='text':
            self.config['content_text'] = self.config['content']
        else:
            self.config['content_html'] = self.config['content']
        del self.config['content']
        g.mail_content=self.config
        g.send__email()

class Send_Window(object):
    def __init__(self,cls):
        super().__init__()
        self.cls=cls

        
        self.clock_status=False #是否开启定时发送

        self.reply_status=False #自动回复标志初始化为关

        cls.em_mass_attachment.clicked.connect(self.check)#单击附件时选中某一个选项
        #创建右键菜单
        # 必须将ContextMenuPolicy设置为Qt.CustomContextMenu
        # 否则无法使用customContextMenuRequested信号
        self.cls.setContextMenuPolicy(Qt.CustomContextMenu)

        # 创建QMenu
        cls.em_mass_contextMenu = QMenu()
        cls.em_mass_actionA = cls.em_mass_contextMenu.addAction(QIcon("images/0.png"), u'|  删除')
        # 显示菜单
        cls.customContextMenuRequested.connect(self.showContextMenu)
        #点击删除menu
        cls.em_mass_contextMenu.triggered[QAction].connect(self.remove)


        cls.em_mass_import_file_recipients.clicked.connect(self.__read_recipient)#关联群发接收者邮箱按钮
        cls.em_mass_import_file_content.clicked.connect(self.__read_content)#群发导入内容按钮
        cls.em_mass_add_attachment.clicked.connect(self.__add_attachment)#群发添加附件安丘
        cls.em_mass_send.clicked.connect(self.__send_email)#立即发送按钮
        cls.em_mass_clock_send.clicked.connect(self.__clock_send)#定时发送按钮


    def __read_recipient(self):
        self.cls.add_log_msg('读取群发目标','blue')
        file_path,is_ok=QFileDialog.getOpenFileName(self.cls,'添加群发目标','./')
        if is_ok:
            print(file_path,is_ok,sep='\n')
            with open(file_path,'r',encoding='utf-8') as f:
                recipient=f.read()
            self.cls.em_mass_recipients.setText(recipient)
        else:
            self.cls.add_log_msg('取消添加','red')


    def __read_content(self):
        self.cls.add_log_msg('添加正文','blue')
        file_path,is_ok=QFileDialog.getOpenFileName(self.cls,'添加正文','./')
        if is_ok:
            print(file_path,is_ok,sep='\n')
            with open(file_path,'r',encoding='utf-8') as f:
                content=f.read()
            self.cls.em_mass_content.setText(content)
        else:
            self.cls.add_log_msg('取消添加','red')

    def __add_attachment(self):
        self.cls.add_log_msg('添加附件','blue')
        file_paths,is_ok=QFileDialog.getOpenFileNames(self.cls,'添加附件','./')
        if is_ok:
            self.cls.em_mass_attachment.addItems(file_paths)
        else:
            self.cls.add_log_msg('取消添加附件','red')

    def __send_email(self):
        cls=self.cls
        if not self.check_send_conditions(cls):
                return
        recipient=cls.em_mass_recipients.text()
        subject=cls.em_mass_subject.text()
        text_type='text' if cls.em_mass_text.isChecked() else 'html'
        content=cls.em_mass_content.toPlainText() if text_type=='text' else cls.em_mass_content.toHtml()
        attachment_paths=self.get_attachment_text(cls)
        config={
            'recipient':recipient,
            'subject':subject,
            'content':content,
            'text_type':text_type,
            'attachment_paths':attachment_paths
        }
        self.reply_status=True
        print(config)
        # self.set_mass_enabled(False)

        self.send_thread=Send_Thread(config,cls)
        self.send_thread.Log_Signal.connect(cls.add_log_msg)#注册日志显示信号
        self.send_thread.start()
        cls.add_log_msg('正在自动自动群发','black')

    def __clock_send(self):
        cls=self.cls
        if self.clock_status:
            #使能立即发送按钮
            cls.em_mass_send.setEnabled(True)
            cls.add_log_msg('关闭定时发送','blue')
            self.clock_send_thread.stop()
            cls.em_mass_clock_send.setText('开启定时发送')
            self.clock_status=False
            self.set_clock_enalble(self.clock_status,cls)
        else:
            if not self.check_send_conditions(cls):
                return
            #使能立即发送按钮
            cls.em_mass_send.setEnabled(False)
            #群发目标
            recipient=cls.em_mass_recipients.text()
            #邮件主题
            subject=cls.em_mass_subject.text()
            #正文类型
            text_type='text' if cls.em_mass_text.isChecked() else 'html'
            #正文内容
            content=cls.em_mass_content.toPlainText() if text_type=='text' else cls.em_mass_content.toHtml()
            #附件路径
            attachment_paths=self.get_attachment_text(cls)
            #定时时间
            timing_time=cls.em_mass_clock.text()
            #是否每天发送
            is_every_day=cls.em_mass_evday.isChecked()
           
            config={
                    'timing_time':timing_time,
                    'is_every_day':is_every_day,
                    'recipient':recipient,
                    'subject':subject,
                    'content':content,
                    'text_type':text_type,
                    'attachment_paths':attachment_paths
                    }
            print(config)
            self.clock_send_thread=Clock_Send_Thread(config,cls)
            self.clock_send_thread.Log_Signal.connect(cls.add_log_msg)#注册日志显示信号
            self.clock_send_thread.start()


            cls.add_log_msg('开启定时发送','blue')
            cls.em_mass_clock_send.setText('关闭定时发送')
            self.clock_status=True
            self.set_clock_enalble(self.clock_status,cls)


    def check_send_conditions(self,cls):
        content_length=len(cls.em_mass_content.toPlainText())
        recipient_length=len(cls.em_mass_recipients.text())
      
        if not content_length:
            cls.add_log_msg('正文内容不能为空！！！','red')
            return False
        if not recipient_length:
            cls.add_log_msg('群发目标不得为空！！！','red')
            return False
        return True

    def set_clock_enalble(self,status,cls):
        cls.em_mass_clock.setEnabled(status)
        cls.label.setEnabled(status)
        cls.em_mass_evday.setEnabled(status)
       





    def __set_recipients_enabled(self):
        cls=self.cls
        is_reply_all=cls.em_mass_reply_all.isChecked()
        cls.em_mass_recipients.setEnabled(not is_reply_all)
        cls.em_mass_import_file_recipient.setEnabled(not is_reply_all)



    def check(self,index):
        '''
        获取当前选中的时第几行
        '''
        r=index.row()
        self.f=r
        print(r)

    def get_attachment_text(self,cls):
         #获取子项的个数
        item_count=cls.em_mass_attachment.count() 
        attachment_paths=[]
        for row in range(item_count):
            attachment_paths.append(cls.em_mass_attachment.item(row).text())
        return attachment_paths

    def showContextMenu(self):
        print('send')
        cls=self.cls
        #如果有选中项，则显示显示菜单
        items=cls.em_mass_attachment.selectedIndexes()
        if items:
          cls.em_mass_contextMenu.show()
          cls.em_mass_contextMenu.exec_(QCursor.pos())  # 在鼠标位置显示
    def remove(self,qAction):
        cls=self.cls
        #self.view.takeItem(self.f)#删除行(实际上是断开了与list的联系)

        #注意：removeItemWidget(self, QListWidgetItem)  # 移除一个Item，无返回值
        #注意：takeItem(self, int)  # 切断一个Item与List的联系，返回该Item
        cls.em_mass_attachment.removeItemWidget(cls.em_mass_attachment.takeItem(self.f))  #删除
    def set_mass_enabled(self,status):
        cls=self.cls
        cls.em_mass_add_attachment.setEnabled(status)
        cls.em_mass_import_file_content.setEnabled(status)
        cls.em_mass_import_file_recipients.setEnabled(status)
        cls.em_mass_recipients.setEnabled(status)
        cls.em_mass_subject.setEnabled(status)
        cls.em_mass_content.setEnabled(status)
        cls.em_mass_attachment.setEnabled(status)
        cls.em_mass_html.setEnabled(status)
        cls.em_mass_text.setEnabled(status)




    def __del__(self):
        print('析构方法被调用')
        if self.reply_status:
            print('自动回复线程被关闭')
            self.mass_reply_thread.stop()

  




  


    
