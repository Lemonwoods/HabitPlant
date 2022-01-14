'''
主文件
'''

from PyQt5.QtWidgets import QApplication
import sys
from main_window.home_window import HomeWindow
from plant.plant_small_window import PlantSmallWindow
from Controller.statistic_control import StatisticController
from to_do.to_do_widget import ToDoWidget
from main_window.tab_bar import TabBar
from habit.habit_bar import HabitBar

if __name__ == '__main__':
    app = QApplication(sys.argv)

    statistic = StatisticController()
    window = HomeWindow(statistic)
    small_plant = PlantSmallWindow(statistic,window.h_plant_widget.h_farm.plant)
    small_plant.show()
    # window.hide()

    # 引用赋值
    window.h_plant_widget.h_farm.statistic_control = statistic
    small_plant.h_mainwindow=window

    # 信号连接
    # small_plant.water_button.clicked.connect(window.h_plant_widget.h_farm.water_button_clicked)

    sys.exit(app.exec_())