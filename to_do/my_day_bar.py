from PyQt5.QtCore import QDate, QTime
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton
from habit.habit_bar import TextButton, CheckButton
import time,datetime
from habit.habit_bar import HabitBar

class DateLabel(QLabel):
    def __init__(self,parent):
        super().__init__()
        self.setParent(parent)
        self.init_ui()

    def init_ui(self):
        self.show()


class MyDayBar(HabitBar):

    def __init__(self, parent):
        super().__init__(parent)

        # 初始化ui
        self.init_child_ui()

    def init_child_ui(self):
        self.text_button.setObjectName('my_day_text_button')
        self.describe_label.setProperty('class','my_day_describe_font')

        self.text_button.h_height = 50
        self.text_button.h_width = 180

        self.h_describe_label_width = 100
        self.h_describe_label_height = 50

        self.text_button.resize(self.text_button.h_width,self.text_button.h_height)
        self.describe_label.resize(self.h_describe_label_width,self.h_describe_label_height)

        y_space = int((self.h_height-self.text_button.h_height)/2)
        x_space = int((self.h_width-self.text_button.h_width-self.h_describe_label_width-self.check_button.h_width)/4)

        self.describe_label.move(x_space,y_space)
        self.text_button.move(x_space*2+self.h_describe_label_width,y_space)

    def time_to_describe(self):
        if int(self.h_minute)<10:
            self.h_content = f'{self.h_hour}:0{int(self.h_minute)}'
        else:
            self.h_content = f'{self.h_hour}:{self.h_minute}'


    def refresh_info(self):
        self.time_to_describe()
        super().refresh_info()
