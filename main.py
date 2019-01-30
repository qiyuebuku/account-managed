#coding=utf-8
import sys
import os

from PyQt5.QtWidgets import QApplication, QMainWindow
# from forms.untitled import *
#
#
# class Window(QMainWindow, Ui_MainWindow):
#     def __init__(self, parent=None):
#         super(Window, self).__init__(parent)
#         self.setupUi(self)
# from AccountManaged.tests.BaseWindow import Window
from AccountManaged.tests.MainWindow import MainWindow
from AccountManaged.tests.AutoReplyWindow import Auto_Window
from AccountManaged.tests.SendMassWindow import Send_Window


if __name__ == '__main__':
    '''
        使用继承：
            原因分析：
                1.随着功能增加，无疑会提高代码耦合率
                2.主类的代码变得杂乱不堪，我都不忍直视了
            解决方案：
                1.为界面显示模块增添更多的工具模块，但代码的迁移将会是一件很麻烦的事情，
                我讨厌麻烦，而且随着功能的增添，即使添加再多的工具函数都是杯水车薪。
                2.使用继承的方式，按功能将界面代码分成几个类，各自的类负责格则的功能迭代，
                主类只负责主界面上的内容，和整个界面的绘制，而剩下的功能类都要继承与界面主类：“
                MainWindow”，所有的一切功能都要在这个类的基础上进行构建。    
    '''
    app = QApplication(sys.argv)
    widget = MainWindow()
    auto_window=Auto_Window(widget)
    send_window=Send_Window(widget)
    widget.show()
    widget.setWindowTitle("账号托管平台 By：柒月&&刑乐")                 
    widget.em_user.setText('1194681498@qq.com')
    widget.em_pwd.setText('uudapucsczddichh')
    widget.set_progressBar(20)
    widget.add_log_msg('请先登录!!!','red')
    sys.exit(app.exec_())