from PyQt5 import QtGui

from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout,QFrame
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer, pyqtSignal, QSize, QRectF, Qt
import datetime
import json

from gui.shadow import get_shadow_effect


class Plant(QPushButton):
    # 基础属性
    attr_dic ={
        "water":50,
        "fertilizer":50,
        "grow":0,
        "health":0,
        "water_wait_time":0,
        "fertilize_wait_time":0,
        "name":'plant_one',
        "reap":"False"
    }

    h_height = 300
    h_width = 300

    # 图片路径
    image_path_root = 'data/ui/plant_image/'

    # timer
    refresh_image_timer = None

    def __init__(self, parent ):
        super().__init__()
        self.setParent(parent)

        # timer
        self.refresh_image_timer = QTimer()
        self.refresh_image_timer.timeout.connect(self.refresh_image)
        self.refresh_image_timer.start(0.5*1000)

        self.init_ui()

    def init_ui(self):
        self.show()
        self.resize(self.h_width, self.h_height)

    def image_path_generator(self):
        path = str(self.attr_dic["name"])+'/'
        num = 0
        if self.attr_dic['grow'] <=30:
            num = 1
        elif self.attr_dic['grow'] <=60:
            num = 2
        elif self.attr_dic['grow'] <100:
            num = 3
        else:
            num = 4

        return self.image_path_root + path + str(num) + '.png'

    def refresh_image(self):
        image_path = self.image_path_generator()
        image_icon = QIcon(image_path)
        self.setIcon(image_icon)
        self.setIconSize(QSize(self.h_width,self.h_height))


class Farm(QFrame):
    # 基础属性
    h_height = 540
    h_width = 800

    bg_width = 400
    bg_height = 500

    # 信号
    add_medal = pyqtSignal(str)
    water_wait = pyqtSignal(str)
    fertilizer_wait = pyqtSignal(str)

    # 控件
    back_ground = None
    plant = None
    operation_bar = None
    plant_info = None

    # 日期结算的时间控制
    last_refresh_health_and_grow_date = None
    last_refresh_water_time = None
    last_refresh_fertilizer_time = None
    last_refresh_water_and_fertilize_wait_time = None

    # 定时器
    refresh_status_timer = None
    get_sys_time_timer = None
    check_water_and_fertilizer = None

    # 属性配置
    water_amount =30 # 此数据项定义了一次浇水的浇水量
    water_wait_time = 30*60 # 此数据项定义了一次浇水的等待时间 单位 秒
    fertilize_wait_time = 30*60 # 此数据项定义了一次施肥之后的等待时间 单位 秒
    water_decrease = 80 # 此属性表示每过多少秒，水的值下降1
    fertilize_decrease = 100 # 此属性表示每过多少秒，肥料的值下降1

    loss_health_amount = 1 # 此属性代表当水或者肥降为0时，生命值的损失速度
    loss_health_time_interval = 5 # 此属性代表当水或者肥降为0时，每过多少分钟，会损失生命值
    grow_amount = 10 # 此属性表示当全部完成时，每天增长多少的生命值
    health_increase_amount = 10 # 此属性表示当任务全部完成时，生命值增长多少
    health_decrease_amount = 20 # 此属性表示当任务没有全部完成时，生命值减少多少

    # 文件地址
    attr_file_path = 'data/attr/farm_attr.json'

    # 自定义信号
    lose_health = pyqtSignal()

    statistic_control = None

    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)

        # 初始化控件
        self.back_ground = QFrame(self)
        self.plant = Plant(self)
        self.operation_bar = OperationBar(self)
        self.plant_info = PlantInfo(self)

        # 初始化ui
        self.init_ui()

        # 从文件读取参数
        farm_attr_file = open(self.attr_file_path)
        farm_attr_file_json = json.load(farm_attr_file)

        self.last_refresh_water_and_fertilize_wait_time = farm_attr_file_json['last_refresh_water_and_fertilize_wait_time']
        self.last_refresh_health_and_grow_date = farm_attr_file_json['last_refresh_health_and_grow_date']
        self.last_refresh_water_time = farm_attr_file_json['last_refresh_water_time']
        self.last_refresh_fertilizer_time = farm_attr_file_json['last_refresh_fertilizer_time']

        if farm_attr_file_json['is_first_time'] == 'True':
            self.first_time_init_refresh_time()

        self.plant.attr_dic =  farm_attr_file_json['plant_attr']

        farm_attr_file.close()

        # 初始化timer
        self.refresh_status_timer = QTimer()
        self.refresh_status_timer.timeout.connect(self.refresh_status)
        self.refresh_status_timer.start(0.3*1000)

        self.get_sys_time_timer = QTimer()
        self.get_sys_time_timer.timeout.connect(self.get_sys_time)
        self.get_sys_time_timer.start(0.3*1000)

        self.check_water_and_fertilizer = QTimer()
        self.check_water_and_fertilizer.timeout.connect(self.check_water_and_fertilizer_def)
        self.check_water_and_fertilizer.start(5*60*1000)

        # 信号绑定
        self.operation_bar.water_button.clicked.connect(self.water_button_clicked)
        # self.operation_bar.fertilizer_button.clicked.connect(self.fertilizer_button_clicked)

    def init_ui(self):
        self.setGraphicsEffect(get_shadow_effect(self))
        # 设定id
        self.back_ground.setObjectName('plant_widget_farm')
        self.plant.setObjectName('plant_widget_farm_plant')

        self.resize(self.h_width, self.h_height)
        self.back_ground.resize(self.bg_width, self.bg_height)
        self.show()

        # 控件布局
        # y_space = int((self.h_height-self.plant.h_height-self.operation_bar.h_height)/3)
        # x_space_plant = int((self.h_width-self.plant.h_width-self.plant_info.h_width)/2)
        # x_space_operation_bar = int((2*x_space_plant+self.plant.h_width-self.operation_bar.h_width)/2)

        # self.plant.move(x_space_plant,y_space)
        # self.operation_bar.move(x_space_operation_bar, y_space+self.plant.h_height)
        # self.plant_info.move(x_space_plant*2+self.plant.h_width,y_space)

        self.plant.move(50,50)
        self.operation_bar.move(140,380)
        self.plant_info.move(450,0)

        # 刷新数值
        self.refresh_plant_info()

    def first_time_init_refresh_time(self):
        self.last_refresh_health_and_grow_date = self.date_to_dic(datetime.date.today())
        self.last_refresh_fertilizer_time = self.datetime_to_dic(datetime.datetime.now())
        self.last_refresh_water_time = self.datetime_to_dic(datetime.datetime.now())
        self.last_refresh_water_and_fertilize_wait_time = self.datetime_to_dic(datetime.datetime.now())

    def check_water_and_fertilizer_def(self):
        if self.plant.attr_dic['water']==0 or self.plant.attr_dic['fertilizer']==0:
            self.lose_health.emit()

    def get_sys_time(self):
        self.get_current_time_and_analyze()
        self.write_into_json()

    def write_into_json(self):
        dic = {
              "is_first_time":"False",
              "last_refresh_health_and_grow_date": self.last_refresh_health_and_grow_date,
              "last_refresh_water_time": self.last_refresh_water_time,
              "last_refresh_fertilizer_time": self.last_refresh_fertilizer_time,
              "last_refresh_water_and_fertilize_wait_time": self.last_refresh_water_and_fertilize_wait_time,
              "plant_attr":self.plant.attr_dic
            }

        json_dic = json.dumps(dic)

        file = open(self.attr_file_path,'w')
        file.write(json_dic)
        file.close()

    def water_the_plant(self):
        # self.plant.water += 5
        # self.plant.grow_number += 10
        pass

    def fertilize_the_plant(self, num):
        # self.plant.fertilizer += num
        # self.plant.grow_number += 5
        pass

    def decrease_health(self):
        # self.plant.health -= 5
        pass

    def refresh_water_waiting_time(self):
        pass

    def refresh_fertilize_waiting_time(self):
        pass

    def decrease_water(self):
        # self.plant.water -= 5
        pass

    def decrease_fertilizer(self):
        # self.plant.fertilizer -= 5
        pass

    def water_button_clicked(self):
        if self.plant.attr_dic['water_wait_time'] ==0:
            self.plant.attr_dic['water']+=self.water_amount
            self.plant.attr_dic['water_wait_time'] = self.water_wait_time
        else:
            self.water_wait.emit(f'请在{(self.plant.attr_dic["water_wait_time"]//60)+1}分钟后再浇水')

    def fertilizer_button_clicked(self, fertilizer_amount):
        if self.plant.attr_dic['fertilize_wait_time'] == 0:
            self.plant.attr_dic['fertilizer'] += fertilizer_amount
            self.plant.attr_dic['fertilize_wait_time'] = self.fertilize_wait_time
        else:
            self.fertilizer_wait.emit(f'请在{(self.plant.attr_dic["fertilize_wait_time"] // 60) + 1}分钟后再施肥')

    def refresh_plant_info(self):
        for key, value in self.plant_info.info_bar_dic.items():
            value.set_status_number(self.plant.attr_dic[key])

        self.plant_info.refresh_info_paint()

    def refresh_status(self):
        self.refresh_plant_info()

        if self.plant.attr_dic['grow'] == 100:
            self.plant_have_grown_up()

    def date_to_dic(self, date):
        dic = {}
        dic['year'] = date.year
        dic['month'] = date.month
        dic['day'] = date.day
        return dic

    def datetime_to_dic(self,datetime):
        dic = self.date_to_dic(datetime)
        dic['hour'] = datetime.hour
        dic['minute'] = datetime.minute
        dic['second'] = datetime.second
        return dic

    def dic_to_date(self,dic):
        return datetime.date(dic['year'],dic['month'],dic['day'])

    def dic_to_datetime(self,dic):
        return datetime.datetime(dic['year'],dic['month'],dic['day'],dic['hour'],dic['minute'],dic['second'])

    def get_current_time_and_analyze(self):

        # 获取系统时间与日期
        current_datetime = datetime.datetime.now()
        current_date = datetime.date.today()

        # 处理生命值和经验值刷新
        day_diff = current_date.__sub__(self.dic_to_date(self.last_refresh_health_and_grow_date)).days

        if day_diff>=1:
            try:
                self.refresh_health_and_grow(self.statistic_control.is_last_time_all_finished,day_diff)
                self.last_refresh_health_and_grow_date = self.date_to_dic(current_date)
            except:
                pass


        # 处理水和肥料的刷新
        seconds_diff = (current_datetime - self.dic_to_datetime(self.last_refresh_water_and_fertilize_wait_time)).seconds
        water_decrease_amount = seconds_diff/(self.water_decrease)
        fertilize_decrease_amount = seconds_diff/(self.fertilize_decrease)
        wait_time = seconds_diff # 此项在测试完成后更改为分钟

        if water_decrease_amount>0:
            self.refresh_water_value(water_decrease_amount)
            self.last_refresh_water_time = self.datetime_to_dic(current_datetime)

        if fertilize_decrease_amount>0:
            self.refresh_fertilize_value(fertilize_decrease_amount)
            self.last_refresh_fertilizer_time = self.datetime_to_dic(current_datetime)

        if wait_time >=1:
            self.refresh_water_and_fertilize_wait_time(wait_time)
            self.last_refresh_water_and_fertilize_wait_time = self.datetime_to_dic(current_datetime)

    def refresh_health_and_grow(self, is_finished , days_diff):
        if is_finished:
            self.plant.attr_dic['grow']+=self.grow_amount
            self.plant.attr_dic['health'] += self.health_increase_amount

        self.plant.attr_dic['grow']-=(days_diff-1)*self.health_decrease_amount


        if self.plant.attr_dic['grow'] >=100:
            self.plant.attr_dic['grow'] = 100

        if self.plant.attr_dic['health'] >=100:
            self.plant.attr_dic['health'] = 100
        elif self.plant.attr_dic['health'] <= 0:
            self.plant.attr_dic['health'] = 0

    def refresh_water_value(self, decrease_amount):
        if self.plant.attr_dic['water'] >= decrease_amount:
            self.plant.attr_dic['water']-=decrease_amount
        else:
            self.plant.attr_dic['water'] = 0

    def refresh_fertilize_value(self, decrease_amount):
        if self.plant.attr_dic['fertilizer'] >= decrease_amount:
            self.plant.attr_dic['fertilizer']-=decrease_amount
        else:
            self.plant.attr_dic['fertilizer'] = 0

    def refresh_water_and_fertilize_wait_time(self, decrease_amount):
        if self.plant.attr_dic['water_wait_time'] >= decrease_amount:
            self.plant.attr_dic['water_wait_time'] -= decrease_amount
        else:
            self.plant.attr_dic['water_wait_time'] = 0

        if self.plant.attr_dic['fertilize_wait_time'] >= decrease_amount:
            self.plant.attr_dic['fertilize_wait_time'] -= decrease_amount
        else:
            self.plant.attr_dic['fertilize_wait_time'] = 0

    def grow_new_plant(self,plant_name):
        self.plant.attr_dic = {
            "water": 50,
            "fertilizer": 50,
            "grow": 0,
            "health": 100,
            "water_wait_time": 0,
            "fertilize_wait_time": 0,
            "name":plant_name,
            "reap":"False"
        }

    def plant_have_grown_up(self):
        if self.plant.attr_dic['reap'] == "False":
            self.add_medal.emit(self.plant.attr_dic['name'])
            self.plant.attr_dic['reap'] = "True"


class PlantInfo(QFrame):

    # 基础属性
    h_width = 100
    h_height = 500

    # 基础控件
    water_bar = None
    fertilizer_bar = None
    grow_bar = None
    health_bar = None
    water_wait_time_bar = None
    fertilize_wait_time_bar = None

    # dic
    info_bar_dic = {}

    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)

        # 初始化控件
        self.water_bar = InfoButton(self,'water',100)
        self.fertilizer_bar = InfoButton(self,'fertilizer',100)
        self.grow_bar = InfoButton(self,'grow',100)
        self.health_bar = InfoButton(self,'health',100)
        self.water_wait_time_bar = InfoButton(self,'water_wait',30*60)
        self.fertilize_wait_time_bar = InfoButton(self,'fertilizer_wait',30*60)

        self.info_bar_dic['water'] = self.water_bar
        self.info_bar_dic['fertilizer'] = self.fertilizer_bar
        self.info_bar_dic['grow'] = self.grow_bar
        self.info_bar_dic['health'] = self.health_bar
        self.info_bar_dic['water_wait_time'] = self.water_wait_time_bar
        self.info_bar_dic['fertilize_wait_time'] = self.fertilize_wait_time_bar

        # 初始化ui
        self.init_ui()

    def init_ui(self):
        self.setGraphicsEffect(get_shadow_effect(self))

        # 设定id
        self.setObjectName('plant_widget_farm_plant_info_widget')
        self.water_bar.icon_label.setObjectName('plant_widget_farm_plant_info_water')
        self.fertilizer_bar.icon_label.setObjectName('plant_widget_farm_plant_info_fertilizer')
        self.grow_bar.icon_label.setObjectName('plant_widget_farm_plant_info_grow')
        self.health_bar.icon_label.setObjectName('plant_widget_farm_plant_info_health')
        self.water_wait_time_bar.icon_label.setObjectName('plant_widget_farm_plant_info_water_wait')
        self.fertilize_wait_time_bar.icon_label.setObjectName('plant_widget_farm_plant_info_fertilizer_wait')

        self.resize(self.h_width, self.h_height)
        # 创建垂直布局
        # v_box = QVBoxLayout()
        # # 将控件放入布局
        # v_box.addWidget(self.water_bar)
        # v_box.addWidget(self.fertilizer_bar)
        # v_box.addWidget(self.grow_bar)
        # v_box.addWidget(self.health_bar)
        # v_box.addWidget(self.water_wait_time_bar)
        # v_box.addWidget(self.fertilize_wait_time_bar)
        #
        # # 布局生效
        # self.setLayout(v_box)
        # self.show()

        y_space = int((self.h_height-self.water_bar.h_height*6)/7)
        x_space = int((self.h_width-self.water_bar.h_width)/2)

        self.water_bar.move(x_space,y_space)
        self.fertilizer_bar.move(x_space,y_space*2+self.water_bar.h_height)
        self.grow_bar.move(x_space, y_space * 3 + self.water_bar.h_height*2)
        self.health_bar.move(x_space, y_space * 4 + self.water_bar.h_height*3)
        self.water_wait_time_bar.move(x_space, y_space * 5 + self.water_bar.h_height * 4)
        self.fertilize_wait_time_bar.move(x_space, y_space * 6 + self.water_bar.h_height * 5)

    def refresh_info_paint(self):
        for key, value in self.info_bar_dic.items():
            value.refresh_status()


class InfoButton(QWidget):
    # 基础属性
    status_name = None
    status_number = None
    statue_full_number = 100

    h_width = 70
    h_height = 70

    radius = None

    icon_width = 60
    icon_height = 60

    # 基础控件
    icon_label = None

    def __init__(self,parent,status_name,status_full_number):
        super().__init__()
        self.setParent(parent)

        # 初始化控件
        self.icon_label = QLabel(self)

        # 初始化属性
        self.status_name = status_name
        self.statue_full_number = status_full_number

        # 初始化ui
        self.init_ui()

    def init_ui(self):
        self.setGraphicsEffect(get_shadow_effect(self))
        self.show()
        self.resize(self.h_width, self.h_height)

        # 设置边框 测试使用

        # 调整控件样式 布局
        self.icon_label.resize(self.icon_width, self.icon_height)
        self.icon_label.show()

        x_space = int((self.h_width-self.icon_width)/2)
        y_space = int((self.h_height-self.icon_height)/2)
        self.icon_label.move(x_space, y_space)

    def decrease_status_number(self,decrease):
        pass

    def refresh_status(self):
        # print(f'刷新绘图函数被调用，当前状态的名称为：{self.status_name},当前的数值为：{self.status_number}')


        brush = QBrush()
        pen = QPen()
        painter = QPainter(self)

        # 抗锯齿
        painter.setRenderHint(QPainter.Antialiasing)


        # 设置brush and pen的颜色
        brush.setStyle(Qt.SolidPattern)

        if self.status_name == 'water':
            brush.setColor(QColor(102,158,255))
        elif self.status_name == 'fertilizer':
            brush.setColor(QColor(129, 81, 28))
        elif self.status_name == 'grow':
            brush.setColor(QColor(70,187,142))
        elif self.status_name == 'health':
            brush.setColor(QColor(228,45,75))
        elif self.status_name == 'water_wait':
            brush.setColor(QColor(248,228,81))
        else:
            brush.setColor(QColor(248,152,32))

        pen.setColor(QColor(255,255,255,0))

        painter.setBrush(brush)
        painter.setPen(pen)


        # 定义矩形
        rect = QRectF(0,0,self.h_width,self.h_height)
        startAngle = 90*16
        spanAngle = int(360*16*(self.status_number/self.statue_full_number))

        painter.drawPie(rect,startAngle,spanAngle)

    def set_status_number(self,status_number):
        self.status_number = status_number
        self.update()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        self.refresh_status()


class OperationBar(QWidget):
    # 基础属性
    h_height = 110
    h_width = 110

    h_button_width = 70
    h_button_height = 70

    # 基础控件
    water_button = None

    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)

        # 初始化控件
        self.water_button = QPushButton(self)
        self.water_button.setGraphicsEffect(get_shadow_effect(self))
        # self.fertilizer_button = QPushButton(self)

        # 初始化ui
        self.init_ui()

    def init_ui(self):
        # 设定id
        self.setObjectName('plant_widget_farm_operation_bar')
        self.water_button.setObjectName('plant_widget_farm_operation_bar_water_button')

        self.show()
        self.resize(self.h_width, self.h_height)

        # 调整控件ui
        self.water_button.resize(self.h_button_width, self.h_button_height)
        # self.fertilizer_button.resize(self.h_button_width, self.h_button_height)
        self.water_button.show()
        # self.fertilizer_button.show()

        # 调整布局
        x_space = int((self.h_width-self.h_button_width)/2)
        y_space = int((self.h_height-self.h_button_height)/2)

        self.water_button.move(x_space,y_space)
        # self.fertilizer_button.move(x_space*2+self.h_button_width,y_space)