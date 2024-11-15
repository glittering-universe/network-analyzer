# 网络数据包分析器

该项目是一个网络数据包分析器，旨在抓取进出计算机的网络报文，并对其进行统计和可视化分析。用户可以通过图形用户界面（GUI）与程序进行交互，查看不同类型报文的统计数据和图表。

小水果取🤔

## 功能

- **数据包捕获**：实时捕获进出计算机的网络报文。
- **报文过滤**：提供简单的过滤器，允许用户根据特定条件筛选报文。
- **统计分析**：统计不同类型的网络报文，包括IPv4、IPv6、UDP、TCP、ARP和DNS。
- **数据可视化**：以饼图、柱状图和折线图展示统计结果。
- **数据保存**：支持将捕获的数据保存为文件，便于后续分析和查看。

## 项目结构

```
network-analyzer
├── src
│   ├── main.py                # 应用程序入口点
│   ├── gui
│   │   └── main_window.py      # GUI界面定义
│   ├── capture
│   │   └── packet_capture.py    # 网络数据包捕获
│   ├── filters
│   │   └── filter.py            # 报文过滤器
│   ├── analysis
│   │   ├── statistics.py        # 统计分析
│   │   └── visualization.py      # 数据可视化
│   └── utils
│       └── helpers.py           # 辅助函数
├── requirements.txt             # 项目依赖库
├── README.md                    # 项目文档
└── setup.py                     # 安装脚本
```

## 安装步骤

1. 克隆该项目到本地：
   ```
   git clone https://github.com/glittering-universe/network-analyzer.git
   ```
2. 进入项目目录：
   ```
   cd network-analyzer
   ```
3. 安装依赖库：
   ```
   pip install -r requirements.txt
   ```
4. 运行应用程序：
   ```
   python src/main.py
   ```
5. 打包安装（可选）
   ```
   python setup.py install
   ```

## 使用说明

- 启动程序后，用户可以通过主窗口进行操作。
- 使用过滤器功能筛选所需的报文。
- 查看统计数据和可视化图表，分析网络流量。
- 捕获的数据可以保存为文件，便于后续使用。

## 注意事项

- 请确保在具有管理员权限的环境中运行程序，以便能够捕获网络数据包。
- 该程序在运行时不会影响计算机的正常使用。

## 贡献

欢迎任何形式的贡献！请提交问题或拉取请求以帮助改进该项目。