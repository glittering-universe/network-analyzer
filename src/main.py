# network-analyzer/src/main.py

import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from capture.packet_capture import PacketCapture
from analysis.statistics import Statistics
from analysis.visualization import Visualization

def main():
    app = QApplication(sys.argv)
    
    # 初始化统计和可视化
    statistics = Statistics()
    visualization = Visualization(statistics)
    
    # 初始化数据捕获，传递统计对象
    packet_capture = PacketCapture(statistics)
    
    # 创建主窗口
    main_window = MainWindow(packet_capture, statistics, visualization)
    main_window.show()

    # 启动应用程序
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()