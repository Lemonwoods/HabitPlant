from os.path import abspath, dirname
from PyQt5.QtWidgets import QFrame,QLabel
from PyQt5.QtCore import QObject,QTimer
from PyQt5.Qt import pyqtSignal
import json
import datetime

#初始用户所拥有的金币数量
from gui.shadow import get_shadow_effect

INITIAL_GPLD_COIN=1000
PATH=dirname(dirname(abspath(__file__))) + "/data/gold_coin/gold_coin.json"

class GoldCoin(QObject):
    #定义一个数字改变信号
    _num_changed=pyqtSignal()
    # 基础属性
    amount = None
    temp_amount=None
    h_timer=None
    last_time=None

    def __init__(self):
        super().__init__()
        self.init_gold()

        #加载时更新一下信息
        self.update_amount()

        #添加时间计时器
        self.h_timer=QTimer()
        self.h_timer.timeout.connect(self.update_amount)
        self.h_timer.start(200000)

     #通过文件初始化金币 如果金币存在则载入 如果金币文件不存在则重新添加
    def init_gold(self):
        try:
            with open(PATH,'r') as fp:
                data=json.load(fp)
                self.amount=data["amount"]
                self.temp_amount=data["temp_amount"]
                self.last_time=data["last_time"]
        except IOError as e:
            self.amount = INITIAL_GPLD_COIN
            self.temp_amount=0
            self.last_time=datetime.date.today().day

    #每隔一天更新金币信息
    def update_amount(self):
        current_date_day = datetime.date.today().day
        if(current_date_day !=self.last_time):
            self.amount+=self.temp_amount
            self.temp_amount=0
            self._num_changed.emit()

    def increase_t_amount(self,increase):
        self.temp_amount+=increase
        self.save_data_in_file()

    def decrease_t_amount(self,decrease):
        self.temp_amount-=decrease
        self.save_data_in_file()

    def decrease_amount(self, decrease):
        if (decrease > self.amount):
            return False
        else:
            self.amount-=decrease
            self.num_changed()
            return True

    #数字更改发出信号 并且保存到文件
    def num_changed(self):
        self.save_data_in_file()
        self._num_changed.emit()


    def save_data_in_file(self):
        self.last_time=datetime.date.today().day
        data={
            "amount":self.amount,
            "temp_amount":self.temp_amount,
            "last_time":self.last_time
        }
        try:
            with  open(PATH,'w') as pf:
                    json.dump(data,pf)
        except IOError as e:
            pass


class GoldCoinBox(QFrame):
    #基本属性
    h_width=150
    h_height=60

    #控件的基本属性
    h_num_label_width=90
    h_num_label_height=60
    h_img_label_width=30
    h_img_label_height=45
    #基本控件
    h_gold_coin=None
    h_gold_coin_label=None
    h_img_label=None
    def __init__(self,parent,gold_coin):
        super(GoldCoinBox, self).__init__()
        self.setParent(parent)

        #基本控件初始化
        self.h_gold_coin=gold_coin
        self.h_gold_coin_label=QLabel(self)
        self.h_img_label=QLabel(self)

        #绑定信号(金币数字更改后 然后改变显示内容)
        self.h_gold_coin._num_changed.connect(self.refresh_num)

        self.init_ui()
        self.refresh_num()

    def refresh_num(self):
        self.h_gold_coin_label.setText(str(self.h_gold_coin.amount))

    def init_ui(self):
        self.setGraphicsEffect(get_shadow_effect(self))
        self.setObjectName("gold_coin_box")
        self.h_gold_coin_label.setObjectName("gold_coin_num_label")
        self.h_img_label.setObjectName("gold_coin_img_label")
        self.h_gold_coin_label.setProperty('class','gold_font')
        self.h_img_label.resize(self.h_img_label_width,self.h_img_label_height)

        self.h_gold_coin_label.resize(self.h_num_label_width, self.h_num_label_height)
        self.resize(self.h_width,self.h_height)

        self.h_gold_coin_label.move(60,0)
        self.h_img_label.move(10,10)

