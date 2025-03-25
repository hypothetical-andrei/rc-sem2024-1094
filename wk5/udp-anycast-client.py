# anycast_sender.py (IPv6)
import socket
import struct

def send_anycast_message_ipv6(message, anycast_group, anycast_port):
    """Sends an IPv6 anycast message."""
    try:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        ttl = struct.pack('i', 1) #ipv6 ttl
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, ttl)
        sock.sendto(message.encode('utf-8'), (anycast_group, anycast_port, 0, 0)) #ipv6 needs scope id and flowinfo
        print(f"IPv6 message sent to [{anycast_group}]:{anycast_port}")
    except Exception as e:
        print(f"Error sending IPv6 anycast message: {e}")
    finally:
        if 'sock' in locals():
            sock.close()

# Example usage:
anycast_group_ipv6 = "ff0e::1"  # Link-local anycast group.
anycast_port_ipv6 = 5007
message_ipv6 = "IPv6 Anycast Message!"

send_anycast_message_ipv6(message_ipv6, anycast_group_ipv6, anycast_port_ipv6)