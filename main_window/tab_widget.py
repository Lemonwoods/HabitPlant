'''
作为每一个页面的基类
'''


from PyQt5.QtWidgets import QWidget,QFrame


class TabWidget(QFrame):
    # 基础属性
    h_width = None
    h_height = None

    def __init__(self,parent):
        super().__init__()
        self.setParent(parent)

        # 初始化ui
        self.init_ui_parent()


    def resize_to_home_window(self):
        self.h_height = self.parent().h_height
        self.h_width = self.parent().h_width
        self.resize(self.h_width, self.h_height)

    def init_ui_parent(self):
        self.resize_to_home_window()