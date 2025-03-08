# Ping Application

## Project Description
The Ping Application is a network diagnostic tool implemented in Python using raw sockets. It functions similarly to the standard `ping` command, allowing users to send ICMP Echo Request packets to a specified host and receive responses. The application helps measure network latency, detect packet loss, and analyze the round-trip time (RTT) of network requests. It is useful for troubleshooting connectivity issues and monitoring network performance.

## Features
- Sends ICMP Echo Request packets
- Receives ICMP Echo Reply packets
- Calculates round-trip time (RTT)
- Implements ICMP checksum validation
- Displays packet loss and statistics

## Prerequisites
- Python 3.x
- Administrator/root privileges (required for raw socket operations)
- PyCharm Community Edition (optional, used for development)

## Installation
1. Clone this repository or download the script:
   ```sh
   git clone <repository_url>
   cd ping-application
   ```
2. Ensure you have Python installed:
   ```sh
   python --version
   ```
3. Run the script with administrator/root privileges:
   ```sh
   sudo python ping.py <target_host>
   ```
   Example:
   ```sh
   sudo python ping.py google.com
   ```

## How It Works
1. The script constructs an ICMP Echo Request packet.
2. It sends the packet to the target host using a raw socket.
3. The target host responds with an ICMP Echo Reply.
4. The application calculates the round-trip time (RTT) and displays statistics.

## Output Example
```
Pinging google.com with 32 bytes of data:
Reply from 142.250.185.206: bytes=32 time=10ms TTL=115
Reply from 142.250.185.206: bytes=32 time=12ms TTL=115
Reply from 142.250.185.206: bytes=32 time=9ms TTL=115
--- google.com ping statistics ---
Packets: Sent = 3, Received = 3, Lost = 0 (0% loss)
Approximate round-trip times in ms:
    Minimum = 9ms, Maximum = 12ms, Average = 10.3ms
```

## Known Issues
- Requires administrative privileges to run due to raw socket access.
- Some systems may block raw socket usage for security reasons.

## Author
Indura Nawarathne

