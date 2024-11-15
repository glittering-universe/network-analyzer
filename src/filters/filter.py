class PacketFilter:
    def __init__(self):
        self.filters = []

    def add_filter(self, filter_condition):
        self.filters.append(filter_condition)

    def apply_filters(self, packets):
        filtered_packets = packets
        for filter_condition in self.filters:
            filtered_packets = [packet for packet in filtered_packets if filter_condition(packet)]
        return filtered_packets

    def clear_filters(self):
        self.filters = []