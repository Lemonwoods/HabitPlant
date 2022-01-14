from PyQt5.QtWidgets import QFrame,QScrollArea,QLabel,QWidget
from PyQt5.QtCore import QEvent,Qt
from PyQt5.QtGui import QPainter, QBrush, QColor,QPen
from PyQt5.Qt import pyqtSignal
from os.path import abspath, dirname
import json

from gui.shadow import get_shadow_effect

week_info_list = ['一', '二', '三', '四', '五', '六', '七']
num_info_list=[30,25,20,15,10,5,0]


class Medal(QLabel):
    #基本属性
    h_width=70
    h_height=70

    #包含属性
    h_img_path=None
    style_path = 'gui/medal_widget.qss'
    def __init__(self,parent):
        super(Medal, self).__init__()
        self.setParent(parent)
        self.init_ui()

    def init_atr(self,img):
        self.h_img_path=img
        self.setObjectName(img)
        self.set_style(self.style_path)

    def init_ui(self):
        self.setGraphicsEffect(get_shadow_effect(self))
        self.resize(self.h_width,self.h_height)

    def set_style(self, path):
        file = open(path, 'r', encoding='utf-8')
        style_content = file.read()
        self.setStyleSheet(style_content)



class MedalWall(QFrame):
    _num_changed_signal=pyqtSignal([int])
    PATH=dirname(dirname(abspath(__file__))) +"/data/medal_wall/medal.json"
    #基本属性
    h_width=500
    h_height=225
    two_medal_space=23
    h_scroll_width=460
    h_scroll_height=120
    h_title_label_width=80
    h_title_label_height=40
    last_time_move=None
    medal_center=None

    #基础控件
    h_medal_wall_scroll_area=None
    h_medal_wall_scroll_area_widget=None
    h_scroll_bar=None
    h_title_label=None

    #存放奖章列表
    h_medal_list=[]
    #当前奖章
    h_medal=None
    h_medal_width=None
    h_medal_height=None
    h_medal_num=0

    def __init__(self,parent):
        super(MedalWall, self).__init__()
        self.setParent(parent)

        #初始化控件
        self.h_medal_wall_scroll_area=QScrollArea(self)
        self.h_medal_wall_scroll_area_widget=QFrame(self.h_medal_wall_scroll_area)
        self.h_scroll_bar=self.h_medal_wall_scroll_area.horizontalScrollBar()
        self.h_title_label=QLabel(self)

        #设定父子关系
        self.h_medal_wall_scroll_area.setWidget(self.h_medal_wall_scroll_area_widget)

        #奖章相关信息初始化
        self.h_medal_width=Medal.h_width
        self.h_medal_height=Medal.h_height
        self.medal_center=int((self.h_scroll_height-self.h_medal_height)/2)

        #滚动控制相关
        self.h_medal_wall_scroll_area.installEventFilter(self)
        self.last_time_move = 0
        self.load_to_local()
        self.init_ui()

    def add_medals(self,plant_name):
        self.h_medal=Medal(self.h_medal_wall_scroll_area_widget)
        if(len(self.h_medal_list)==0):
            self.h_medal.move(self.h_medal_width*len(self.h_medal_list),self.medal_center)
        else:
            self.h_medal.move(self.h_medal_width * len(self.h_medal_list)+self.two_medal_space*len(self.h_medal_list), self.medal_center)
        self.h_medal_list.append(self.h_medal)
        if(len(self.h_medal_list)>=5):
            self.h_medal_wall_scroll_area_widget.resize(self.h_medal_width*len(self.h_medal_list)+self.two_medal_space*(len(self.h_medal_list)),self.h_scroll_height)
        self.h_medal_num+=1
        self.h_medal.init_atr(plant_name)
        self._num_changed_signal.emit(self.h_medal_num)

    def init_ui(self):
        self.h_title_label.setGraphicsEffect(get_shadow_effect(self))
        self.setGraphicsEffect(get_shadow_effect(self))

        #设置id
        self.h_medal_wall_scroll_area.setObjectName("medal_list_box")
        self.h_medal_wall_scroll_area_widget.setObjectName("medal_list_box_frame")
        self.h_title_label.setObjectName("medal_title_label")
        self.setObjectName("medal_frame")
        self.h_title_label.setProperty('class','title_three')

        #设置大小
        self.h_title_label.resize(self.h_title_label_width,self.h_title_label_height)
        self.resize(self.h_width,self.h_height)
        self.h_medal_wall_scroll_area.resize(self.h_scroll_width,self.h_scroll_height)
        self.h_medal_wall_scroll_area_widget.resize(450,120)

        #设置文字
        self.h_title_label.setText("奖章墙")

        #移动位置
        self.h_title_label.move(20,20)
        self.h_medal_wall_scroll_area.move((self.h_width-self.h_scroll_width)/2+10,(self.h_height-self.h_scroll_height)/2+30)

        self.setStyleSheet(
            "#medal_list_box QScrollBar{"
            "max-width:0px;"
            "}"
        )

        #文字居中
        self.h_title_label.setAlignment(Qt.AlignCenter)

    def save_to_file(self):
        data_list=[]
        for i in self.h_medal_list:
            data={
                'img':i.h_img_path
            }
            data_list.append(data)
        try:
            with open(self.PATH, 'w') as fp:
                json.dump(data_list,fp)
        except IOError as e:
            pass

    def load_to_local(self):
        try:
            with open(self.PATH,'r') as fp:
                data_list=json.load(fp)
                for data in data_list:
                    self.add_medals(data["img"])
        except IOError as e:
            pass

    #增加滚动
    def eventFilter(self, source, event):
           if event.type() == QEvent.MouseMove:
               if self.last_time_move == 0:
                   self.last_time_move = event.pos().x()
               distance = self.last_time_move - event.pos().x()
               self.h_scroll_bar.setValue(self.h_scroll_bar.value() + distance)
               self.last_time_move = event.pos().x()
           elif event.type() == QEvent.MouseButtonRelease:
               self.last_time_move = 0
           return QFrame.eventFilter(self, source, event)


class InformationDispalyFrame(QFrame):

    space_x=30
    space_y=85
    two_label_space=30

    h_width=500
    h_height=225
    h_statistic=None
    h_title_label_width=80
    h_title_label_height=40
    h_label_width=200
    h_label_height=40


    h_medal_wall=None
    h_title_label=None
    medal_num_label=None
    total_use_day_label=None
    full_use_day_label=None
    all_finished_task_label=None


    def __init__(self,parent,statistic,medal_wall):
        super(InformationDispalyFrame, self).__init__()
        self.setParent(parent)
        #初始化属性
        self.h_statistic=statistic

        #初始化控件
        self.h_title_label=QLabel(self)
        self.medal_num_label=QLabel(self)
        self.total_use_day_label=QLabel(self)
        self.full_use_day_label=QLabel(self)
        self.all_finished_task_label=QLabel(self)
        self.h_medal_wall=medal_wall


        self.init_ui()
        self.update_medal_num(self.h_medal_wall.h_medal_num)
        self.update_full_use_day()
        self.update_total_use_day()
        self.update_all_finished_task()
        self.h_medal_wall._num_changed_signal.connect(self.update_medal_num)

    def update_medal_num(self,medal_num):
        self.medal_num_label.setText('拥有奖章数'+str(medal_num)+'个')

    def update_total_use_day(self):
        self.total_use_day_label.setText('你使用该应用'+str(self.h_statistic.total_use_days)+'天')

    def update_full_use_day(self):
        self.full_use_day_label.setText('完整打卡天数'+str(self.h_statistic.full_days_counts)+'天')

    def update_all_finished_task(self):
        self.all_finished_task_label.setText("任务完成数量"+str(self.h_statistic.to_do_finished_count+
                                                          self.h_statistic.my_day_finished_count+self.h_statistic.habit_finished_count)
                                            +"个")

    def paintEvent(self,e):
        self.h_statistic.is_full_day()
        self.h_statistic.use_days()
        self.update_total_use_day()
        self.update_all_finished_task()

    def init_ui(self):
        self.setGraphicsEffect(get_shadow_effect(self))
        self.h_title_label.setGraphicsEffect(get_shadow_effect(self))
        self.medal_num_label.setGraphicsEffect(get_shadow_effect(self))
        self.total_use_day_label.setGraphicsEffect(get_shadow_effect(self))
        self.full_use_day_label.setGraphicsEffect(get_shadow_effect(self))
        self.all_finished_task_label.setGraphicsEffect(get_shadow_effect(self))


        #设置id
        self.setObjectName("info_frame")
        self.h_title_label.setObjectName("info_title_label")
        self.medal_num_label.setObjectName("info_medal_num_label")
        self.total_use_day_label.setObjectName("info_total_use_day_label")
        self.full_use_day_label.setObjectName("info_full_use_day_label")
        self.all_finished_task_label.setObjectName("info_temp_label")
        self.h_title_label.setProperty('class','title_three')
        self.medal_num_label.setProperty('class','description_two')
        self.total_use_day_label.setProperty('class','description_two')
        self.all_finished_task_label.setProperty('class','description_two')
        self.full_use_day_label.setProperty('class','description_two')

        #设置文字
        self.h_title_label.setText("信息栏")

        #设置大小
        self.resize(self.h_width,self.h_height)
        self.h_title_label.resize(self.h_title_label_width,self.h_title_label_height)
        self.medal_num_label.resize(self.h_label_width,self.h_label_height)
        self.full_use_day_label.resize(self.h_label_width,self.h_label_height)
        self.total_use_day_label.resize(self.h_label_width,self.h_label_height)
        self.all_finished_task_label.resize(self.h_label_width, self.h_label_height)

        #移动位置
        self.h_title_label.move(20,20)
        self.medal_num_label.move(self.space_x,self.space_y)
        self.total_use_day_label.move(self.space_x,self.space_y+self.medal_num_label.height()+self.two_label_space)
        self.full_use_day_label.move(self.space_x+self.medal_num_label.width()+self.two_label_space,self.space_y)
        self.all_finished_task_label.move(self.space_x + self.medal_num_label.width() + self.two_label_space, self.space_y + self.medal_num_label.height() + self.two_label_space)

        #文字居中
        self.h_title_label.setAlignment(Qt.AlignCenter)
        self.medal_num_label.setAlignment(Qt.AlignCenter)
        self.total_use_day_label.setAlignment(Qt.AlignCenter)
        self.full_use_day_label.setAlignment(Qt.AlignCenter)
        self.all_finished_task_label.setAlignment(Qt.AlignCenter)


class LineChartFrame(QFrame):
    h_width=500
    h_height=500
    h_title_label_width=80
    h_title_label_height=40
    h_chart_width=350
    h_chart_height=350
    space_x=None
    space_y=None

    week_info_bar=None
    num_info_bar=None
    h_paint=None
    h_title_label = None
    h_chart=None
    h_statistic=None
    def __init__(self,parent,statistic):
        super(LineChartFrame, self).__init__()
        self.setParent(parent)
        #初始化属性
        self.h_statistic=statistic

        #初始化控件
        self.h_title_label=QLabel(self)
        self.week_info_bar = WeekInfoBar(self)
        self.num_info_bar=NumInfoBar(self)
        self.h_chart=Chart(self,self.h_statistic)

        self.space_x=self.week_info_bar.x_space
        self.space_y=self.num_info_bar.y_space


        self.init_ui()

    def init_ui(self):
        self.setGraphicsEffect(get_shadow_effect(self))
        self.h_title_label.setGraphicsEffect(get_shadow_effect(self))

        #设置id
        self.setObjectName("line_chart_frame")
        self.h_title_label.setObjectName("line_chart_titlr_label")
        self.h_title_label.setProperty('class','title_three')

        #设置文字
        self.h_title_label.setText("折线图")

        #设置大小
        self.h_title_label.resize(self.h_title_label_width,self.h_title_label_height)
        self.resize(self.h_width,self.h_height)

        #移动位置
        self.h_title_label.move(20,20)
        self.num_info_bar.move(55,45)
        self.week_info_bar.move(75,self.h_height-self.week_info_bar.h_height)
        self.h_chart.move(80,80)

        #文字居中
        self.h_title_label.setAlignment(Qt.AlignCenter)


class Chart(QFrame):
    h_width=350
    h_height=350
    space_x=58
    space_y=13
    h_statistic=None



    def __init__(self,parent,statistic):
        super(Chart, self).__init__()
        self.setParent(parent)
        self.h_statistic=statistic
        self.init_ui()

    def paintEvent(self, e):
            qp = QPainter()

            qp.begin(self)
            self.draw_my_day_line(qp)
            self.draw_habit_line(qp)
            qp.end()

    def draw_my_day_line(self,qp):
          qp.setRenderHint(QPainter.Antialiasing)
          myday_dict=self.h_statistic.myday_week_finished
          zero_coordinate=self.h_height
          qb=QPen()
          qb.setColor(QColor(249,152,35))
          qb.setWidth(5)
          qp.setPen(qb)
          for i in range(6):
              qp.drawLine(self.space_x*(i),zero_coordinate-myday_dict[str(i)]*self.space_y,self.space_x*(i+1),zero_coordinate-myday_dict[str(i+1)]*self.space_y)

    def draw_habit_line(self,qp):
          qp.setRenderHint(QPainter.Antialiasing)
          myday_dict=self.h_statistic.habit_week_finished
          zero_coordinate=self.h_height-5
          qb=QPen()
          qb.setColor(QColor(226,44,75))
          qb.setWidth(5)
          qp.setPen(qb)
          for i in range(6):
              qp.drawLine(self.space_x*(i),zero_coordinate-myday_dict[str(i)]*self.space_y,self.space_x*(i+1),zero_coordinate-myday_dict[str(i+1)]*self.space_y)


    def init_ui(self):
        self.resize(self.h_width,self.h_height)
        self.setObjectName("chart_frame")
        # self.setFrameShape(QFrame.Box)


class NumLabel(QLabel):
    h_width=80
    h_height=80


    def __init__(self,parent,num_info):
        super(NumLabel, self).__init__()
        self.setParent(parent)
        self.num_info=num_info
        self.init_ui()

    def init_ui(self):
        self.setProperty('class','description_three')
        self.resize(self.h_width, self.h_height)
        self.setText(str(self.num_info))


class NumInfoBar(QFrame):
    # 基础属性
    h_height = 600
    h_width = 80
    y_space=None

    num_info_len=len(num_info_list)

    def __init__(self,parent):
        super().__init__()
        self.setParent(parent)
        self.label_list=[]
        for i in range(self.num_info_len):
                self.label_list.append(WeekLabel(self, num_info_list[i]))
        self.init_ui()

    def init_ui(self):
        x_space=int((self.h_width-self.label_list[0].h_width)/2)
        # y_space = int((self.h_height-self.num_info_len*self.label_list[0].h_height)/(self.num_info_len+1))
        # self.y_space=y_space
        y_space=57
        for i in range(self.num_info_len):
            if(i==6 or i==5):
                self.label_list[i].move(x_space+6,y_space*i)
            else:
                self.label_list[i].move(x_space, y_space * i)


class WeekLabel(QLabel):
    # 基础属性
    h_width = 80
    h_height = 80

    def __init__(self, parent, week_info):
        super().__init__()
        self.setParent(parent)

        # 初始化属性
        self.week_info = week_info

        # 初始化ui
        self.init_ui()

    def init_ui(self):
        self.setProperty('class','description_three')
        self.resize(self.h_width, self.h_height)
        self.setText(str(self.week_info))
        # self.show()


class WeekInfoBar(QFrame):
    # 基础属性
    h_height = 80
    h_width = 600
    x_space=None


    def __init__(self,parent):
        super().__init__()
        self.setParent(parent)
        self.label_list = []

        # 初始化标签
        for i in range(7):
                self.label_list.append(WeekLabel(self, week_info_list[i]))
        # 初始化ui
        self.init_ui()

    def init_ui(self):
        # x_space = int((self.h_width-7*self.label_list[0].h_width)/8)
        y_space = int((self.h_height-self.label_list[0].h_height)/2)
        # self.x_space=(x_space+self.label_list[0].h_width)*4/5
        x_space=57

        for i in range(7):
            self.label_list[i].move(x_space*i,y_space)


class MedalWallFrame(QFrame):
    h_width=1200
    h_height=700
    h_statistic=None
    space_x=50
    space_y=50

    h_medal_wall=None
    h_inf_display_frame=None
    h_line_chart_frame=None

    def __init__(self,parent,statistic):
        super(MedalWallFrame, self).__init__(parent)
        # 初始化基本信息
        self.h_statistic = statistic

        #初始化控件
        self.h_medal_wall=MedalWall(self)
        self.h_inf_display_frame=InformationDispalyFrame(self,self.h_statistic,self.h_medal_wall)
        self.h_line_chart_frame=LineChartFrame(self,self.h_statistic)
        self.init_ui()

    def init_ui(self):
        #设置id
        self.setObjectName("medal_wall_widget")

        #重新设置大小
        self.resize(self.h_width,self.h_height)

        #移动
        self.h_medal_wall.move(self.space_x,self.space_y)
        self.h_inf_display_frame.move(self.space_x,self.h_medal_wall.h_height+self.space_y*2)
        self.h_line_chart_frame.move(self.h_medal_wall.h_width+self.space_x*2,self.space_y)
