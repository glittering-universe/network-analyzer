# src/analysis/statistics.py

import time

class Statistics:
    def __init__(self):
        self.data = {
            'IPv4': 0,
            'IPv6': 0,
            'UDP': 0,
            'TCP': 0,
            'ARP': 0,
            'DNS': 0
        }
        self.dns_over_time = []
        self.start_time = time.time()

    def reset(self):
        """重置统计数据。"""
        for key in self.data:
            self.data[key] = 0
        self.dns_over_time = []
        self.start_time = time.time()
        print("统计数据已重置。")

    def collect(self, packet):
        """收集数据包信息以进行统计分析。"""
        if packet.haslayer('IP'):
            if packet['IP'].version == 4:
                self.data['IPv4'] += 1
            elif packet['IP'].version == 6:
                self.data['IPv6'] += 1
        if packet.haslayer('TCP'):
            self.data['TCP'] += 1
        if packet.haslayer('UDP'):
            self.data['UDP'] += 1
        if packet.haslayer('ARP'):
            self.data['ARP'] += 1
        if packet.haslayer('DNS'):
            self.data['DNS'] += 1
            self._record_dns_over_time()

    def _record_dns_over_time(self):
        """记录 DNS 报文随时间的变化"""
        current_time = time.time() - self.start_time
        self.dns_over_time.append((current_time, self.data['DNS']))

    def calculate(self):
        """返回当前的统计数据。"""
        return self.data

    def save_to_file(self, filename):
        """将统计数据保存到文件。"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for key, value in self.data.items():
                    f.write(f"{key}: {value}\n")
                f.write("\nDNS报文随时间变化:\n")
                for time_point, dns_count in self.dns_over_time:
                    f.write(f"{time_point:.2f}秒: {dns_count}\n")
            print(f"统计数据已保存到 {filename}")
        except Exception as e:
            print(f"保存统计数据时发生错误: {e}")