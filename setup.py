from setuptools import setup, find_packages

setup(
    name='network-analyzer',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A network packet analyzer with GUI for capturing and analyzing network traffic.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'scapy',  # 用于网络数据包捕获
        'matplotlib',  # 用于数据可视化
        'PyQt5',  # 用于GUI开发
        'pandas'  # 用于数据处理
    ],
    entry_points={
        'console_scripts': [
            'network-analyzer=main:main',  # 假设main.py中有一个main函数作为入口
        ],
    },
)