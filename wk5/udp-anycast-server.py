# anycast_receiver.py (IPv6)
import socket
import struct

def receive_anycast_message_ipv6(anycast_group, anycast_port):
    """Receives an IPv6 anycast message."""
    try:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #reuse address

        sock.bind(('', anycast_port, 0, 0)) #bind to all interfaces

        group = socket.inet_pton(socket.AF_INET6, anycast_group)
        mreq = group + struct.pack('i', 0) # interface index 0 = all interfaces
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

        print(f"Listening for IPv6 anycast messages on [{anycast_group}]:{anycast_port}...")

        while True:
            data, addr = sock.recvfrom(1024)
            print(f"Received IPv6 message from {addr}: {data.decode('utf-8')}")

    except Exception as e:
        print(f"Error receiving IPv6 anycast message: {e}")

    finally:
        if 'sock' in locals():
            sock.close()

# Example receiver usage:
anycast_group_ipv6 = "ff0e::1"  # Link-local anycast group.
anycast_port_ipv6 = 5007

receive_anycast_message_ipv6(anycast_group_ipv6, anycast_port_ipv6)