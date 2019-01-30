#coding=utf-8
#系统
import sys
import os
#pyqt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtCore, QtGui, QtWidgets


#获取顶层目录
top_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(top_dir)

#获取项目目录
parent_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_dir)

#自己的库
from tools import tools
from bin import zmail
from AccountManaged.tests.AutoResponse import *
from forms.Ui_untitled import *


class LoginThread(QThread):
    '''
        使用多线程UI技术
    '''
    # 定义日志显示信号
    Log_Signal = pyqtSignal(str,str)
    # 设置enabled 信号
    Set_enabled_Signal=pyqtSignal(bool)
    def __init__(self,parent=None,server=None):
        super().__init__(parent)
        self.server=server
        self.ui=parent
    def run(self):
        self.ui.logged_in = True
        self.Log_Signal.emit('登陆成功','green')
        self.ui.server=self.server
        # 功能区设置为可用状态
        self.ui.em_function_zone.setEnabled(True)
        self.ui.AutoResponse = AutoResponse(self.server)
        self.ui.em_login.setText('退出')
        self.Set_enabled_Signal.emit(False)
        if tools.check_POP_SMT(self.server):
            self.ui.logged_in = True
            self.Log_Signal.emit('登陆成功','green')
            self.ui.server=self.server
            # 功能区设置为可用状态
            self.ui.em_function_zone.setEnabled(True)
            self.ui.AutoResponse = AutoResponse(self.server)
            self.ui.em_login.setText('退出')
            self.Set_enabled_Signal.emit(False)
        else:
            self.Log_Signal.emit('登陆失败', 'red')

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        # super(MainWindow, self).__init__(parent)
        super().__init__(parent)
        self.setupUi(self)
        self.logged_in=False  #登陆状态默认为未登录
        self.em_function_zone.setEnabled(False) #功能框默认为不可用状态
        #控件的信号连接
        self.em_login.clicked.connect(self.login)#登陆按钮  
     

    def add_log_msg(self,info,color):
        """
        功能：用于将传递过来的info显示在QTextEdit上
        :info:需要显示的内容
        :index:显示的颜色
        :return:
        """
        display_info=self.em_log_msg
        if len(display_info.toPlainText())>256:
            display_info.setHtml("")

        text_style={
            'red':'DC143C',
            'orange':'FFA500',
            'yellow':'FFFF00',
            'green':'008000',
            'black':'000000',
            'blue':'0000FF',
            'purple':'800080'
        }
        text=self.em_log_msg.toHtml()+ '<div style="color:#'+text_style[color]+';">'+info+'</div>'
        display_info.setHtml(text)
        display_info.moveCursor(QTextCursor.End)

    def login(self):
        if self.logged_in==False:
            user=self.em_user.text()
            pwd=self.em_pwd.text()

            #构建服务端并验证账号
            self.add_log_msg('账号检测中……', 'orange')
            #为了防止界面卡死，这里使用了多线程加信号机制来登陆
            server=zmail.server(user,pwd,timeout=300)
            login_thread=LoginThread(self,server=server)#实例化多线程
            login_thread.Log_Signal.connect(self.add_log_msg)#注册日志显示信号
            login_thread.Set_enabled_Signal.connect(self.__set_login_enablee)#注册设置界面状态信号
            login_thread.start()#启动线程
        else:
            self.em_login.setText('登陆')
            self.__set_login_enablee(True)
            self.add_log_msg('退出成功', 'purple')
            #功能区设置为不可用
            self.em_function_zone.setEnabled(False)
            self.logged_in=False
    def __set_login_enablee(self,status):
        self.em_user.setEnabled(status)
        self.em_pwd.setEnabled(status)
    
    #用于设置进度条的值
    def set_progressBar(self,num):
        self.em_progressBar.setValue(num)
