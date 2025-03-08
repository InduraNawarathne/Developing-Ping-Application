import os
import sys
import struct
import time
import select
import socket

ICMP_ECHO_REQUEST = 8  # ICMP type code for echo request


def checksum(source_string):
    """Calculate the checksum of the packet."""
    total = 0
    max_count = (len(source_string) // 2) * 2
    count = 0

    while count < max_count:
        val = (source_string[count + 1]) * 256 + (source_string[count])
        total = total + val
        total = total & 0xffffffff
        count = count + 2

    if max_count < len(source_string):
        total = total + (source_string[len(source_string) - 1])
        total = total & 0xffffffff

    total = (total >> 16) + (total & 0xffff)
    total = total + (total >> 16)
    answer = ~total
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def create_packet(packet_id):
    """Create a new ICMP Echo Request packet."""
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, 0, packet_id, 1)
    data = struct.pack('d', time.time())
    my_checksum = checksum(header + data)

    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), packet_id, 1)
    return header + data


def send_ping(sock, dest_addr, packet):
    """Send ICMP Echo Request."""
    sock.sendto(packet, (dest_addr, 1))


def receive_ping(sock, packet_id, timeout):
    """Receive ICMP Echo Reply."""
    time_left = timeout

    while True:
        start_time = time.time()
        ready = select.select([sock], [], [], time_left)
        time_in_select = (time.time() - start_time)

        if ready[0] == []:  # Timeout
            return None

        time_received = time.time()
        rec_packet, addr = sock.recvfrom(1024)

        icmp_header = rec_packet[20:28]
        icmp_type, code, checksum_recv, recv_packet_id, sequence = struct.unpack('bbHHh', icmp_header)

        if recv_packet_id == packet_id:
            bytes_in_double = struct.calcsize('d')
            time_sent = struct.unpack('d', rec_packet[28:28 + bytes_in_double])[0]
            return time_received - time_sent

        time_left = time_left - time_in_select
        if time_left <= 0:
            return None


def ping(host):
    """Main ping function."""
    try:
        dest_addr = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"PING {host} - Request timed out (host not found)")
        return

    print(f"PING {host} ({dest_addr}) in Python")

    icmp = socket.getprotobyname('icmp')
    with socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp) as sock:
        packet_id = os.getpid() & 0xFFFF

        for seq in range(6):
            packet = create_packet(packet_id)
            send_ping(sock, dest_addr, packet)
            delay = receive_ping(sock, packet_id, 1)

            if delay is None:
                print(f"Request timeout for icmp_seq {seq}")
            else:
                delay_ms = round(delay * 1000, 3)
                print(f"64 bytes from {dest_addr}: icmp_seq={seq} ttl=55 time={delay_ms} ms")

            time.sleep(1)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python ping.py <hostname>")
        sys.exit(1)

    ping(sys.argv[1])
