def save_to_file(data, filename):
    with open(filename, 'w') as file:
        file.write(data)

def load_from_file(filename):
    with open(filename, 'r') as file:
        return file.read()

def format_packet_data(packet):
    return f"Packet: {packet}"

def filter_packets(packets, condition):
    return [packet for packet in packets if condition(packet)]

def calculate_statistics(packets):
    statistics = {
        'IPv4': 0,
        'IPv6': 0,
        'UDP': 0,
        'TCP': 0,
        'ARP': 0,
        'DNS': 0
    }
    for packet in packets:
        if packet['type'] == 'IPv4':
            statistics['IPv4'] += 1
        elif packet['type'] == 'IPv6':
            statistics['IPv6'] += 1
        elif packet['type'] == 'UDP':
            statistics['UDP'] += 1
        elif packet['type'] == 'TCP':
            statistics['TCP'] += 1
        elif packet['type'] == 'ARP':
            statistics['ARP'] += 1
        elif packet['type'] == 'DNS':
            statistics['DNS'] += 1
    return statistics