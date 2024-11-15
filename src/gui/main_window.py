# src/gui/main_window.py

from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QVBoxLayout, QWidget, QLabel, QPushButton, QHBoxLayout, QStatusBar
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QTimer
from analysis.visualization import Visualization

class MainWindow(QMainWindow):
    def __init__(self, packet_capture, statistics, visualization):
        super().__init__()
        self.packet_capture = packet_capture
        self.statistics = statistics
        self.visualization = visualization

        self.setWindowTitle("网络数据包分析器")
        self.setGeometry(100, 100, 900, 1500)
        self.setWindowIcon(QIcon("icons/app_icon.png"))  # 设置应用图标
        self.initUI()

        # 设置定时器以定期更新图表
        self.timer = QTimer()
        self.timer.setInterval(20)  # 每2秒更新一次
        self.timer.timeout.connect(self.update_visualization)

    def initUI(self):
        # 设置中心窗口和主布局
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout()
        self.central_widget.setLayout(main_layout)

        # 添加标题标签
        self.title_label = QLabel("网络数据包分析器")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Microsoft YaHei", 16, QFont.Bold))
        main_layout.addWidget(self.title_label)

        # 添加按钮布局
        button_layout = QHBoxLayout()

        self.start_button = QPushButton("开始捕获")
        self.start_button.setIcon(QIcon("icons/start.png"))
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.start_button.clicked.connect(self.start_capture)
        button_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("停止捕获")
        self.stop_button.setIcon(QIcon("icons/stop.png"))
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        self.stop_button.clicked.connect(self.stop_capture)
        button_layout.addWidget(self.stop_button)

        self.save_button = QPushButton("保存数据")
        self.save_button.setIcon(QIcon("icons/save.png"))
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #008CBA;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #007bb5;
            }
        """)
        self.save_button.clicked.connect(self.save_data)
        button_layout.addWidget(self.save_button)

        main_layout.addLayout(button_layout)

        # 添加统计信息标签
        self.stats_label = QLabel("统计数据:")
        self.stats_label.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        main_layout.addWidget(self.stats_label)

        self.stats_display = QLabel("暂无数据")
        self.stats_display.setFont(QFont("Microsoft YaHei", 10))
        self.stats_display.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.stats_display.setStyleSheet("""
            QLabel {
                background-color: #f0f0f0;
                padding: 10px;
                border-radius: 5px;
            }
        """)
        main_layout.addWidget(self.stats_display)

        # 添加可视化组件
        self.visualization_widget = self.visualization
        main_layout.addWidget(self.visualization_widget)

        # 创建菜单
        self.create_menu()

        # 添加状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("准备就绪")

        # 应用整体样式表
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
            QLabel {
                color: #333333;
            }
        """)

    def create_menu(self):
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #333333;
                color: white;
            }
            QMenuBar::item {
                background: transparent;
            }
            QMenuBar::item:selected {
                background-color: #555555;
            }
            QMenu {
                background-color: #ffffff;
                color: #333333;
            }
            QMenu::item:selected {
                background-color: #f0f0f0;
            }
        """)

        file_menu = menubar.addMenu("文件")

        save_action = QAction(QIcon("icons/save.png"), "保存", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_data)
        file_menu.addAction(save_action)

        exit_action = QAction(QIcon("icons/exit.png"), "退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def start_capture(self):
        """启动数据包捕获"""
        self.status_bar.showMessage("开始捕获数据包...")
        self.packet_capture.start_capture()
        self.statistics.reset()
        self.visualization.clear()
        self.stats_display.setText("统计数据:\n正在捕获中...")
        self.timer.start()

    def stop_capture(self):
        """停止数据包捕获"""
        self.status_bar.showMessage("停止捕获数据包...")
        self.packet_capture.stop_capture()
        self.timer.stop()
        stats = self.statistics.calculate()
        self.display_statistics(stats)
        self.visualization.update_charts(stats)
        self.status_bar.showMessage("捕获已停止")

    def save_data(self):
        """保存统计数据和捕获的数据包"""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "保存统计数据", "", "文本文件 (*.txt);;所有文件 (*)", options=options)
        if file_name:
            try:
                self.statistics.save_to_file(file_name)
                self.status_bar.showMessage(f"统计数据已保存到 {file_name}")
            except Exception as e:
                self.status_bar.showMessage(f"保存统计数据时发生错误: {e}")

        # 选择是否保存捕获的数据包
        save_packets = QFileDialog.question(self, "保存数据包", "是否保存捕获的数据包?", QFileDialog.Yes | QFileDialog.No, QFileDialog.No)
        if save_packets == QFileDialog.Yes:
            packets_file, _ = QFileDialog.getSaveFileName(self, "保存数据包", "", "PCAP 文件 (*.pcap);;所有文件 (*)", options=options)
            if packets_file:
                try:
                    self.packet_capture.save_packets(packets_file)
                    self.status_bar.showMessage(f"数据包已保存到 {packets_file}")
                except Exception as e:
                    self.status_bar.showMessage(f"保存数据包时发生错误: {e}")

    def display_statistics(self, stats):
        """在GUI中显示统计数据"""
        stats_text = "\n".join([f"{key}: {value}" for key, value in stats.items()])
        self.stats_display.setText(f"统计数据:\n{stats_text}")

    def update_visualization(self):
        """定期更新图表"""
        stats = self.statistics.calculate()
        self.visualization.update_charts(stats)