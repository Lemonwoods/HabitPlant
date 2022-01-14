import time

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QPushButton, QWidget,QFrame,QLabel
from gui.shadow import get_shadow_effect


class CheckButton(QPushButton):

    h_width = 60
    h_height = 60

    # 图片路径
    check_path = 'data/ui/habit_widget/check_button/check.png'
    uncheck_path = 'data/ui/habit_widget/check_button/uncheck/png'

    # 用于隐藏打钩的label
    hide_label = None

    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)
        self.resize(self.h_width, self.h_height)
        self.show()

        # 初始化控件
        self.hide_label = QLabel()
        self.hide_label.setParent(self)

        # 连接信号
        self.clicked.connect(self.refresh_check_status)

        # 初始化ui
        self.init_ui()

    def init_ui(self):
        self.setGraphicsEffect(get_shadow_effect(self))

        self.hide_label.setObjectName('check_button_hide_label')
        self.hide_label.resize(40,40)
        self.hide_label.move(int((self.h_width-self.hide_label.width())/2),int((self.h_height-self.hide_label.height())/2))

    def move_to_center(self):
        distance = self.parent().h_height - self.h_height
        distance = int(distance/2)

        x_pos = int(self.parent().h_width - distance - self.h_width)

        self.move(x_pos, distance)

    def refresh_check_icon(self):
        if self.parent().h_is_finished:
            self.hide_label.hide()
        else:
            self.hide_label.show()

    def refresh_check_status(self):
        if self.parent().h_is_finished == True:
            self.parent().h_is_finished = False
            self.refresh_check_icon()
            # self.setText('F')
        else:
            self.parent().h_is_finished = True
            self.refresh_check_icon()
            # self.setText('T')


class TextButton(QPushButton):

    h_width = 270
    h_height = 50

    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)
        self.resize(self.h_width, self.h_height)
        self.show()

    def move_to_center(self):
        distance = self.parent().h_height - self.h_height
        distance = int(distance/2)
        self.move(distance,distance)


class HabitBar(QFrame):

    h_width = 400
    h_height = 100

    h_describe_label_height = 15
    h_describe_label_width = 220

    # 属性字段
    h_title = None
    h_content = None
    h_tag = None
    h_times = None
    h_is_delete=False
    h_is_finished=False

    h_year = None
    h_month = None
    h_day = None
    h_hour = None
    h_minute = None

    h_week = {
        "Mon": False,
        "Tue": False,
        "Wen": False,
        "Thur": False,
        "Fri": False,
        "Sat": False,
        "Sun": False}

    # 基础控件
    check_button = None
    text_button = None
    describe_label = None

    # 创建时间
    create_date = {
        "year": None,
        "month": None,
        "day": None,
    }
    # 创建时间，同时作为id
    create_time = None

    def __init__(self,parent):
        super().__init__()
        self.setParent(parent)
        self.check_button = CheckButton(self)
        self.text_button = TextButton(self)
        self.describe_label = QLabel(self)

        self.create_date["year"] = QDate().currentDate().year()
        self.create_date["month"] = QDate().currentDate().month()
        self.create_date["day"] = QDate().currentDate().day()

        self.create_time = time.time()


        # 初始化ui
        self.init_ui()

    def init_ui(self):

        self.setGraphicsEffect(get_shadow_effect(self))

        # 设定id
        self.setObjectName('habit_bar')
        self.check_button.setObjectName('habit_bar_check_button')
        self.text_button.setObjectName('habit_bar_text_button')
        self.describe_label.setObjectName('habit_bar_describe_label')

        self.text_button.setProperty('class','title_one')
        self.describe_label.setProperty('class','description_one')

        # 调整布局与大小
        self.describe_label.show()
        self.describe_label.resize(self.h_describe_label_width,self.h_describe_label_height)


        self.resize(self.h_width, self.h_height)
        self.check_button.move_to_center()

        # 调整text_button 和 describe_label的布局
        y_space = int((self.h_height-self.text_button.h_height-self.h_describe_label_height)/3)
        x_space = int((self.h_width-self.text_button.h_width-self.check_button.h_width)/3)
        self.text_button.move(x_space,y_space)
        self.describe_label.move(x_space,y_space*2+self.text_button.h_height)

    def refresh_info(self):
        self.text_button.setText(self.h_title)
        self.describe_label.setText(self.h_content)
        self.check_button.refresh_check_icon()