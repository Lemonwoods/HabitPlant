from  PyQt5.QtWidgets import QScrollArea,QFrame

class ListBox(QScrollArea):

    l_width = None
    l_height = None

    #两个bar之间空隙
    two_bar_space=20
    #bar距离左边的空隙
    bar_space_right=30
    bar_space_left=5

    edit_window = None

    def __init__(self, parent,bar_width,bar_height,edit_window=None):
        super(ListBox, self).__init__()

        self.setParent(parent)
        # 为scrollArea添加 widget
        self.scrollarea_widget_contents = QFrame(self)
        self.setWidget(self.scrollarea_widget_contents)
        self.edit_window = edit_window

      #创建按钮列表以及信息
        self.bar=None
        self.bar_list=[]
        self.bar_width=bar_width
        self.bar_height=bar_height

        #初始化界面
        # self.init_ui()

    #只负责添加button时，界面的变化，如果需要其他功能请在子类中重载并且扩写该函数
    def add(self):#添加button控件--槽函数
        self.bar.setParent(self.scrollarea_widget_contents)
        if(len(self.bar_list)==0):
            self.bar.move(self.bar_space_left, 0)
        else:
            self.bar.move(self.bar_space_left, self.bar_height * (len(self.bar_list)) + self.two_bar_space*(len(self.bar_list)))
        self.scrollarea_widget_contents.resize(self.bar_width + self.bar_space_right, self.bar_height * (len(self.bar_list) + 1) + self.two_bar_space * (len(self.bar_list) + 1))#实时变化
        # 后面添加的控件需要show 才能显示
        # self.bar.show()

    #取消按钮绑定的槽函数（这些是最基本功能 如果功能需要扩展 请在子类中重载该函数 并且扩写）
    def cancle(self):
        if(self.bar not in self.bar_list):
            self.bar.hide()
            try:
                del self.bar
            except:
                pass
            self.scrollarea_widget_contents.resize(self.bar_width + self.bar_space_right, self.bar_height * (len(self.bar_list)) + self.two_bar_space * (len(self.bar_list)))
            # self.edit_window.cancel_button.clicked.disconnect(self.cancle)
            # self.edit_window.save_button.clicked.disconnect(self.saved)

    #保存按钮联系的函数（这些是最基本功能 如果功能需要扩展 请在子类中重载该函数 并且扩写）
    def saved(self):
           self.bar_list.append(self.bar)
           # self.edit_window.save_button.clicked.disconnect(self.saved)
           # self.edit_window.cancel_button.clicked.disconnect(self.cancle)

    #删除按钮联系的函数（这些是最基本功能 如果功能需要扩展 请在子类中重载该函数 并且扩写）
    def delete(self):
        for button in self.bar_list:
            if (button.h_is_delete):
                button.hide()
                self.bar_list.remove(button)
                del button
                break
        self.referesh_list_box()

    def referesh_list_box(self):
        i = 0  # 记录button索引的
        for button in self.bar_list:
            if (i == 0):
                button.move(self.bar_space_left, 0)
            else:
                button.move(self.bar_space_left, self.bar_height * i + self.two_bar_space * i)
            button.show()
            i += 1
        self.scrollarea_widget_contents.resize(self.bar_width + self.bar_space_right,
                                               self.bar_height * (len(self.bar_list)) + self.two_bar_space * (len(self.bar_list)))

    def all_hide(self):
        for button in self.bar_list:
            button.hide()

    def init_ui(self):
        self.setObjectName("list_box")
        self.scrollarea_widget_contents.setObjectName("list_box_frame")
        self.l_width = self.bar_width+self.bar_space_right
        self.l_height = self.bar_height*3+self.two_bar_space*3
        self.resize(self.l_width,self.l_height)
        # self.setFrameShape(QFrame.NoFrame)
        # 去除滚动条
        self.setStyleSheet(
            "#list_box QScrollBar{"
            "max-width:0px;"
            "}"
        )
