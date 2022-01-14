from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QPushButton, QFrame, QLabel

from gui.shadow import get_shadow_effect
from plant.farm import Farm
from plant.mall import BagAndMall
from plant.gold_coin import GoldCoinBox
from main_window.tab_widget import TabWidget

class PlantWidget(TabWidget):
    # 基础控件
    h_farm = None
    h_bag_and_mall = None
    h_gold_coin=None
    h_gold_coin_box=None
    h_message_box = None
    h_message_label = None

    def __init__(self,parent,gold_coin):
        super().__init__(parent)

        # 初始化控件
        self.h_gold_coin=gold_coin
        self.h_farm = Farm(self)
        self.h_bag_and_mall = BagAndMall(self,self.h_gold_coin,self.h_farm)
        self.h_gold_coin_box=GoldCoinBox(self,self.h_gold_coin)
        self.h_message_box = MessageBox(self)
        self.h_message_label = QLabel(self)

        # 初始化ui
        self.init_ui()

        # 信号连接
        self.h_farm.water_wait.connect(self.h_message_box.wake_up)
        self.h_farm.fertilizer_wait.connect(self.h_message_box.wake_up)
        self.h_bag_and_mall.mall._money_no_enough.connect(self.h_message_box.wake_up)

    def init_ui(self):
        self.setObjectName('plant_widget')
        self.h_farm.move(50,50)
        self.h_bag_and_mall.move(650,50)
        self.h_gold_coin_box.move(950,460)
        self.h_message_label.setGeometry(130, 400, 300, 50)
        self.h_message_label.setProperty("class", "description_one")
        self.h_message_label.setText("注意，种植新植物会覆盖当前植物哦")

        self.show()
        self.resize(self.parent().width(), self.parent().height())


# 消息弹出框
class MessageBox(QPushButton):

    message_text = None
    width = 200
    high = 40

    def __init__(self, parent):
        super().__init__(parent)

        self.init_ui()

    def init_ui(self):
        self.setGraphicsEffect(get_shadow_effect(self))

        self.hide()
        self.resize(self.width, self.high)
        self.setObjectName('plant_bubble')
        self.setProperty('class','bubble_font')
        self.move(150,54)


    def wake_up(self, text):
        self.setText(text)
        self.show()
        QTimer.singleShot(3000, self.close)