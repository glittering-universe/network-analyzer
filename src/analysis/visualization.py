# src/analysis/visualization.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib import rcParams

class Visualization(QWidget):
    def __init__(self, statistics):
        super().__init__()
        self.statistics = statistics
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 配置Matplotlib中文字体
        rcParams['font.family'] = 'SimHei'  # 或 'Microsoft YaHei'
        rcParams['axes.unicode_minus'] = False

        # 创建 Matplotlib 图形
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        # 创建子图
        self.ax_pie = self.figure.add_subplot(221)  # IPv4 和 IPv6 饼图
        self.ax_bar = self.figure.add_subplot(222)  # TCP, UDP, ARP 柱状图
        self.ax_line = self.figure.add_subplot(212)  # DNS 折线图

        self.figure.tight_layout()

    def clear(self):
        """清除当前图表内容"""
        self.ax_pie.clear()
        self.ax_bar.clear()
        self.ax_line.clear()
        self.canvas.draw()

    def update_charts(self, stats):
        """根据统计数据更新图表"""
        self.clear()

        # 更新饼图 (IPv4 和 IPv6)
        ipv4 = stats.get('IPv4', 0)
        ipv6 = stats.get('IPv6', 0)
        if ipv4 + ipv6 > 0:
            self.ax_pie.pie(
                [ipv4, ipv6],
                labels=['IPv4', 'IPv6'],
                autopct='%1.1f%%',
                startangle=140,
                colors=['#66b3ff','#99ff99']
            )
            self.ax_pie.set_title('IPv4 与 IPv6 分布', fontsize=12)
        else:
            self.ax_pie.text(
                0.5, 0.5, '无数据', horizontalalignment='center',
                verticalalignment='center', fontsize=12
            )
            self.ax_pie.set_title('IPv4 与 IPv6 分布', fontsize=12)

        # 更新柱状图 (TCP, UDP, ARP)
        tcp = stats.get('TCP', 0)
        udp = stats.get('UDP', 0)
        arp = stats.get('ARP', 0)
        protocols = ['TCP', 'UDP', 'ARP']
        counts = [tcp, udp, arp]
        colors = ['#ff9999','#66b3ff','#99ff99']
        self.ax_bar.bar(protocols, counts, color=colors)
        self.ax_bar.set_title('TCP、UDP、ARP 报文数量', fontsize=12)
        self.ax_bar.set_ylabel('数量', fontsize=10)
        self.ax_bar.tick_params(labelsize=10)

        # 更新折线图 (DNS 随时间变化)
        dns_data = self.statistics.dns_over_time
        if dns_data:
            times, dns_counts = zip(*dns_data)
            self.ax_line.plot(times, dns_counts, marker='o', linestyle='-', color='purple')
            self.ax_line.set_title('DNS 报文随时间变化', fontsize=12)
            self.ax_line.set_xlabel('时间 (秒)', fontsize=10)
            self.ax_line.set_ylabel('DNS 报文数量', fontsize=10)
            self.ax_line.tick_params(labelsize=10)
        else:
            self.ax_line.text(
                0.5, 0.5, '无数据', horizontalalignment='center',
                verticalalignment='center', fontsize=12
            )
            self.ax_line.set_title('DNS 报文随时间变化', fontsize=12)
            self.ax_line.set_xlabel('时间 (秒)', fontsize=10)
            self.ax_line.set_ylabel('DNS 报文数量', fontsize=10)

        self.canvas.draw()