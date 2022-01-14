from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QPushButton, QLabel,QMessageBox,QFrame
from PyQt5.Qt import pyqtSignal
from enum import IntEnum

from gui.shadow import get_shadow_effect
from main_window.list_box import ListBox
from functools import partial
from os.path import abspath, dirname
import json

class ItemType(IntEnum):
    plant=0
    fertilizer=1


class GoodImgFrame(QFrame):
    h_height=60
    h_width=60

    def __init__(self,parent):
        super(GoodImgFrame, self).__init__()
        self.setParent(parent)
        self.init_ui()

    #加载图片路径
    def load_img(self,img):
        self.setObjectName(img)

    def init_ui(self):
        self.setGraphicsEffect(get_shadow_effect(self))
        self.resize(self.h_width,self.h_height)


class GoodDescLabel(QLabel):
    h_width=130
    h_height=30
    def __init__(self,parent):
        super(GoodDescLabel, self).__init__()
        self.setParent(parent)
        self.init_ui()

    def assign_msg(self,price_or_num,describe,money_num):
        self.setText(price_or_num+':'+str(money_num)+'  '+describe)

    def init_ui(self):
        self.setObjectName("good_desc_label")
        self.setProperty('class','description_one')
        self.setAlignment(Qt.AlignCenter)
        self.resize(self.h_width,self.h_height)


class GoodTitleLable(QLabel):
    h_width=100
    h_height=30

    def __init__(self,parent):
        super(GoodTitleLable, self).__init__()
        self.setParent(parent)
        self.init_ui()

    def assign_msg(self,goodname):
        self.setText(goodname)

    def init_ui(self):
        self.setObjectName("good_title_label")
        self.setProperty('class','title_one')
        self.setAlignment(Qt.AlignCenter)
        self.setGraphicsEffect(get_shadow_effect(self))
        self.resize(self.h_width,self.h_height)


class ConfirmButton(QPushButton):
    h_width=60
    h_height=60

    def __init__(self,parent):
        super(ConfirmButton, self).__init__()
        self.setParent(parent)
        self.init_ui()

    def init_ui(self):
        self.setGraphicsEffect(get_shadow_effect(self))
        self.resize(self.h_width,self.h_height)


class Good(QFrame):
    space_left=35
    space_top=20
    two_label_space=10
    h_width=380
    h_height=100
    # 基础属性
    h_type=None
    h_name = None
    h_describe = None
    h_attribute=None
    h_img=None
    #基础控件
    h_img_frame=None
    h_desc_label=None
    h_title_label=None
    h_ok_button=None

    def __init__(self,parent):
        super(Good, self).__init__()
        self.setParent(parent)

        # 初始化组成控件
        self.h_img_frame = GoodImgFrame(self)
        self.h_desc_label = GoodDescLabel(self)
        self.h_title_label=GoodTitleLable(self)
        self.h_ok_button = ConfirmButton(self)

    #初始化公共信息
    def init_same_msg(self,img,name,describe,type,attribute=None):
        self.h_img=img
        self.h_name=name
        self.h_describe=describe
        self.h_type=type
        self.h_attribute=attribute

    def init_ui(self):
        self.resize(self.h_width,self.h_height)
        self.h_img_frame.move(self.space_left, self.space_top)
        self.h_title_label.move(self.h_img_frame.h_width+self.space_left+self.two_label_space*4,
                                self.space_top)
        self.h_desc_label.move(self.h_img_frame.h_width+self.space_left+self.two_label_space*3,
                               self.space_top+self.h_title_label.h_height+10)
        self.h_ok_button.move(self.h_img_frame.h_width+self.space_left+self.two_label_space*6+self.h_desc_label.h_width,
                              self.space_top)
        self.setWindowOpacity(1.0)
        self.setGraphicsEffect(get_shadow_effect(self))


class MallGood(Good):

    h_price=None
    _buy_signal = pyqtSignal([Good])  #定义购买信号（向背包发送已经购买的商品信息）

    def __init__(self,parent):
        super(MallGood, self).__init__(parent)
        self.init_ui()

    def init_mall_good(self,img,name,describe,price,type,attribute=None):#初始化商品信息
        super().init_same_msg(img,name,describe,type,attribute)
        self.h_price=price
        #初始化表面的信息
        self.h_img_frame.load_img(img)
        self.h_title_label.setText(name)
        self.h_desc_label.assign_msg('售价',describe, price)

    def init_ui(self):
        super().init_ui()
        self.h_ok_button.setObjectName("mall_good_buy_button")
        self.setObjectName("mall_good_frame")


class BagGood(Good):
    h_num=None
    use_signal = pyqtSignal([int])
    plant_use_signal = pyqtSignal([str])# 使用信号  发送属性以及数量
    def __init__(self, parent):
        super(BagGood, self).__init__(parent)
        self.init_ui()

    # 初始化物品信息
    def init_bag_good(self,img,name,describe,type,attribute=None,num=-1):
        super().init_same_msg(img,name,describe,type,attribute)
        self.h_num=num
        #初始化表面的信息
        self.h_img_frame.load_img(img)
        self.h_title_label.setText(self.h_name)
        self.h_desc_label.assign_msg('数量',self.h_describe, self.h_num)

    # 通过商店发送过来的good类型变量，添加购买的物品的信息
    def add_bag_good(self,good):
        super().init_same_msg(good.h_img, good.h_name, good.h_describe, good.h_type, good.h_attribute)
        self.h_num=1
        self.h_img_frame.load_img(self.h_img)
        self.h_title_label.setText(self.h_name)
        self.h_desc_label.assign_msg('数量：',self.h_describe, self.h_num)

    def update_num(self):
        self.h_desc_label.assign_msg('数量：',self.h_describe, self.h_num)

    def init_ui(self):
        super().init_ui()
        self.h_ok_button.setObjectName("bag_good_use_button")
        self.setObjectName("bag_good_frame")


class Bag(ListBox):
    PATH=dirname(dirname(abspath(__file__))) + "/data/mall_and_bag/bag.json"
    h_width=400
    h_height=None

    farm=None

    data_list=[]
    def __init__(self,parent,farm):
        super(Bag, self).__init__(parent,Good.h_width,Good.h_height)
        self.farm=farm
        self.h_height=Good.h_height*3+self.two_bar_space*3
        self.init_ui()
        self.load_data()

    def init_product(self):
        self.bar=BagGood(self)
        super().add()
        self.bar.init_bag_good(None,"肥料","无",None,None,100)
        self.bar_list.append(self.bar)

    def add_good(self,good):
        extence=False
        appoint_good=None
        for goods in self.bar_list:
            if(good.h_name==goods.h_name and good.h_describe==goods.h_describe):
                extence=True
                appoint_good=goods
                break

        if(not extence):
            self.bar=BagGood(self)
            super().add()
            self.bar.add_bag_good(good)#传递good属性赋值货物
            if(good.h_type==ItemType.plant):
                self.bar.plant_use_signal.connect(self.farm.grow_new_plant)
            elif(good.h_type==ItemType.fertilizer):
                self.bar.use_signal.connect(self.farm.fertilizer_button_clicked)
            self.bar.h_ok_button.clicked.connect(partial(self.run_out_and_deleted,self.bar))
            self.bar_list.append(self.bar)
        else:
           appoint_good.h_num+=1
           appoint_good.update_num()
        self.save_data()

    #用来加载文件时调用
    def add_bag_good(self,baggood):
        self.bar = baggood
        super().add()
        if (self.bar.h_type == ItemType.plant):
            self.bar.plant_use_signal.connect(self.farm.grow_new_plant)
        elif (self.bar.h_type == ItemType.fertilizer):
            self.bar.use_signal.connect(self.farm.fertilizer_button_clicked)
        self.bar.h_ok_button.clicked.connect(partial(self.run_out_and_deleted, self.bar))
        self.bar_list.append(self.bar)

    def run_out_and_deleted(self,good):
        if(good.h_type==ItemType.fertilizer):
            if(self.farm.plant.attr_dic["fertilize_wait_time"]==0):
                good.use_signal.emit(int(good.h_attribute))
            else:
                good.use_signal.emit(int(good.h_attribute))
                return
        elif(self.bar.h_type == ItemType.plant):
            good.plant_use_signal.emit(good.h_img)
        good.h_num-=1
        good.update_num()
        if(good.h_num==0):
            self.bar_list.remove(good)
            good.hide()
            del good
        self.referesh_list_box()
        self.save_data()

    def save_data(self):
        self.data_list.clear()
        for t in self.bar_list:
            data = {"img":t.h_img,
                    "name":t.h_name,
                    "describe":t.h_describe,
                    "type":int(t.h_type),
                    "attribute":t.h_attribute,
                    "num":t.h_num
                    }
            self.data_list.append(data)
        try:
            with open(self.PATH, 'w') as fp:
                json.dump(self.data_list,fp)
        except IOError as e:
            pass

    def load_data(self):
        try:
            with open(self.PATH,'r') as fp:
                self.data_list=json.load(fp)
            for data in self.data_list:
                baggood= BagGood(self)
                baggood.init_bag_good(data["img"],data["name"],data["describe"],data["type"],data["attribute"],data["num"])
                self.add_bag_good(baggood)

        except IOError as e:
            pass

    def init_ui(self):
        super(Bag, self).init_ui()
        self.resize(self.h_width,self.h_height)


class Mall(ListBox):
    _money_no_enough=pyqtSignal([str])
    PATH=dirname(dirname(abspath(__file__))) + "/data/mall_and_bag/mall.json"
    h_width=400
    h_height=None

    gold_coin=None

    data_list=[]
    def __init__(self, parent,glod_coin):
        super(Mall, self).__init__(parent,Good.h_width,Good.h_height)
        #获取金币实例
        self.gold_coin=glod_coin

        self.h_height=Good.h_height*3+self.two_bar_space*3
        self.init_goods()
        self.bind()
        self.init_ui()

    # 这里初始化商品信息
    def init_goods(self):

        #肥料
        self.bar=MallGood(self)
        super().add()
        self.bar.init_mall_good("fertilizer_one","普通肥料","普通肥料",50,ItemType.fertilizer,50)
        self.bar_list.append(self.bar)

        #
        self.bar=MallGood(self)
        super().add()
        self.bar.init_mall_good("fertilizer_two","高级肥料","高级肥料",100,ItemType.fertilizer,100)
        self.bar_list.append(self.bar)


        #植物
        self.bar=MallGood(self)
        super().add()
        self.bar.init_mall_good("plant_one","小叶藤","",200,ItemType.plant)
        self.bar_list.append(self.bar)

        #植物
        self.bar=MallGood(self)
        super().add()
        self.bar.init_mall_good("plant_two","绿芭蕉","",200,ItemType.plant)
        self.bar_list.append(self.bar)

    def  bind(self):
        for bar in self.bar_list:
            bar.h_ok_button.clicked.connect(partial(self.buy_good,bar))

    def buy_good(self,good):
        if(self.gold_coin.decrease_amount(good.h_price)):
              good._buy_signal.emit(good)
        else:
        #测试用 记得删除
            self._money_no_enough.emit("金币不足")
        #应该提示用户购买失败

    def init_ui(self):
        super(Mall, self).init_ui()
        # self.setObjectName("mall_good_list_box")
        self.resize(self.h_width,self.h_height)


class BagAndMall(QFrame):
    h_width=500
    h_height=500
    space_left=55
    space_top=30

    #窗口控件
    bag=None
    mall=None
    bag_button=None
    mall_button=None
    gold_coin=None
    farm=None

    def __init__(self, parent,gold_coin,farm):
        super(BagAndMall, self).__init__()
        self.setParent(parent)
        #初始化控件
        self.gold_coin=gold_coin
        self.farm=farm
        self.bag=Bag(self,farm)
        self.mall=Mall(self,self.gold_coin)
        self.bag_button=BagButton(self,self)
        self.mall_button=MallButton(self,self)

        # 这是背包滚动区域拖动文本联动滚动条
        self.scroll_bar = self.mall.verticalScrollBar()
        self.mall.installEventFilter(self)
        self.bag.installEventFilter(self)
        self.last_time_move = 0

        #绑定槽函数 初始化ui
        self.bind()
        self.init_ui()
        self.bag.hide()

    #绑定 购买商品发送信号 和背包中获取购买的商品信息槽函数
    def bind(self):
        for good in self.mall.bar_list:
           good._buy_signal.connect(self.bag.add_good)

    def init_ui(self):
        self.setGraphicsEffect(get_shadow_effect(self))
        self.setObjectName("bag_and_mall_frame")
        self.resize(self.h_width,self.h_height)

        #控件移动
        button_space_left=25
        button_space_down=25
        self.mall_button.move(button_space_left,
                              self.h_height-self.mall_button.h_height-button_space_down)
        self.bag_button.move(self.bag_button.h_width+button_space_left+10,
                             self.h_height-self.bag_button.h_height-button_space_down)

        self.bag.move(self.space_left,self.space_top)
        self.mall.move(self.space_left,self.space_top)

    def eventFilter(self, source, event):
           if event.type() == QEvent.MouseMove:
               if self.last_time_move == 0:
                   self.last_time_move = event.pos().y()
               distance = self.last_time_move - event.pos().y()
               self.scroll_bar.setValue(self.scroll_bar.value() + distance)
               self.last_time_move = event.pos().y()
           elif event.type() == QEvent.MouseButtonRelease:
               self.last_time_move = 0
           return QFrame.eventFilter(self, source, event)



class BagButton(QPushButton):
    h_width=70
    h_height=70

    mall_and_bag=None
    mall=None
    bag=None

    def __init__(self,parent,mall_and_bag):
        super(BagButton, self).__init__()
        self.setParent(parent)
        self.mall_and_bag=mall_and_bag
        self.mall=mall_and_bag.mall
        self.bag=mall_and_bag.bag
        self.bind()
        self.init_ui()

    def change(self):
        self.mall_and_bag.scroll_bar=self.bag.verticalScrollBar()
        self.mall_and_bag.last_time_move=0
        self.mall.hide()
        self.bag.show()

    def bind(self):
        self.clicked.connect(self.change)

    def init_ui(self):
        self.setObjectName("bag_button")
        self.resize(self.h_width,self.h_height)
        self.setGraphicsEffect(get_shadow_effect(self))


class MallButton(QPushButton):
    h_width = 70
    h_height = 70

    mall_and_bag=None
    mall=None
    bag=None

    def __init__(self,parent,mall_and_bag):
        super(MallButton, self).__init__()
        self.setParent(parent)
        self.mall_and_bag=mall_and_bag
        self.mall=mall_and_bag.mall
        self.bag=mall_and_bag.bag
        self.bind()
        self.init_ui()

    def change(self):
        self.mall_and_bag.scroll_bar=self.mall.verticalScrollBar()
        self.mall_and_bag.last_time_move=0
        self.mall.show()
        self.bag.hide()

    def bind(self):
        self.clicked.connect(self.change)

    def init_ui(self):
        self.setObjectName("mall_button")
        self.resize(self.h_width, self.h_height)
        self.setGraphicsEffect(get_shadow_effect(self))

