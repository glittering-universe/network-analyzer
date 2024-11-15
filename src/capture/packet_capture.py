# src/capture/packet_capture.py

import scapy.all as scapy
import threading

class PacketCapture:
    def __init__(self, statistics):
        self.packets = []
        self.capture_thread = None
        self.stop_sniff = False
        self.statistics = statistics  # 添加统计对象引用

    def start_capture(self):
        if self.capture_thread and self.capture_thread.is_alive():
            print("捕获已经在进行中。")
            return
        self.stop_sniff = False
        self.capture_thread = threading.Thread(target=self._capture, daemon=True)
        self.capture_thread.start()

    def _capture(self):
        print("开始捕获数据包...")
        scapy.sniff(prn=self.process_packet, store=0, stop_filter=self.should_stop)

    def should_stop(self, packet):
        return self.stop_sniff

    def process_packet(self, packet):
        self.packets.append(packet)
        self.statistics.collect(packet)  # 收集统计数据
        # print(f"捕获到数据包: {packet.summary()}")  # 可选：减少输出避免性能问题

    def stop_capture(self):
        if self.capture_thread and self.capture_thread.is_alive():
            self.stop_sniff = True
            self.capture_thread.join()
            print("已停止数据包捕获。")

    def save_packets(self, filename):
        try:
            scapy.wrpcap(filename, self.packets)
            print(f"数据包已保存到 {filename}")
        except Exception as e:
            print(f"保存数据包时发生错误: {e}")

    def reset(self):
        self.packets = []
        print("捕获的数据包已重置。")

    def __del__(self):
        self.stop_capture()

if __name__ == "__main__":
    from analysis.statistics import Statistics

    stats = Statistics()
    capture = PacketCapture(stats)
    try:
        capture.start_capture()
        input("按回车键停止捕获...\n")
    except KeyboardInterrupt:
        print("停止捕获数据包...")
    finally:
        capture.stop_capture()
        capture.save_packets("captured_packets.pcap")
        print(f"捕获到 {len(capture.packets)} 个数据包")