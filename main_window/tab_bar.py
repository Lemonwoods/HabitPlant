from PyQt5.QtWidgets import QWidget, QFrame, QPushButton, QGridLayout
from gui.shadow import get_shadow_effect


class TabButton(QPushButton):

    h_height = 70
    h_width = 70

    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)
        self.resize(self.h_width, self.h_height)
        self.show()

        self.init_ui()

    def init_ui(self):
        self.setGraphicsEffect(get_shadow_effect(self))



class TabBar(QFrame):
    h_width = 800
    h_height = 90

    to_do_button = None
    habit_button = None
    plant_button = None
    medal_button = None

    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)
        self.resize(self.h_width, self.h_height)

        # 初始化三个tab的按钮
        self.to_do_button = TabButton(self)
        self.habit_button = TabButton(self)
        self.plant_button = TabButton(self)
        self.medal_button = TabButton(self)

        # 初始化ui
        self.init_ui()

    def init_ui(self):
        self.setGraphicsEffect(get_shadow_effect(self))

        self.show()

        # 设定id
        self.to_do_button.setObjectName('tab_bar_to_do_button')
        self.habit_button.setObjectName('tab_bar_habit_button')
        self.plant_button.setObjectName('tab_bar_plant_button')
        self.medal_button.setObjectName('tab_bar_medal_button')
        self.setObjectName('tab_bar')

        # 调整布局
        self.move_to_center()

    def move_to_center(self):
        button_height = self.to_do_button.h_height
        button_width = self.to_do_button.h_width

        vertical_space = int((self.h_height-button_height)/2)
        horizontal_space = int((self.h_width-4*button_width)/8)

        self.to_do_button.move(horizontal_space, vertical_space)
        self.habit_button.move(horizontal_space*3+button_width, vertical_space)
        self.plant_button.move(horizontal_space * 5 + button_width * 2, vertical_space)
        self.medal_button.move(horizontal_space*7+button_width*3,vertical_space)