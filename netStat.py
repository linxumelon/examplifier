import psutil
import time
import socket


def get_global_stat():
    stats = psutil.net_io_counters(pernic=False, nowrap=True)
    bytes_sent = stats.bytes_sent
    bytes_recv = stats.bytes_recv
    packets_sent = stats.packets_sent
    packets_recv = stats.packets_recv
    errin = stats.errin  # total number of errors while receiving
    errout = stats.errout   # total number of errors while sending
    dropin = stats.dropin  # total number of incoming packets which were dropped
    dropout = stats.dropout  # total number of outgoing packets which were dropped (always 0 on macOS and BSD)


def get_socket_connections(kind="all"):
    connections = psutil.net_connections(kind=kind)
    for c in connections:
        fd = c.fd  # the socket file descriptor
        family = c.family  # the address family, either AF_INET, AF_INET6 or AF_UNIX.
        type = c.type  # the address type, either SOCK_STREAM, SOCK_DGRAM or SOCK_SEQPACKET.
        laddr = c.laddr  # the local address as a(ip, port) or a path in case of AF_UNIX sockets
        raddr = c.raddr  # the remote address as a(ip, port) or an absolute path in case of UNIX sockets
        status = c.status  # the status of a TCP connection
        pid = c.pid  # PID of the process which opened the socket


def get_NIC_address():
    nic_addresses = psutil.net_if_addrs()
    for interface_name, addresses in nic_addresses:
        for a in addresses:
            family = a.family  # the address family
            address = a.address  # primary NIC address
            netmask = a.netmask  # netmask address
            broadcast = a.broadcast  # broadcast address
            ptp = a.ptp # destination address on a point to point interface


def get_NIC_stats():
    nic_stats = psutil.net_if_stats()
    for interface_name, stat in nic_stats:
        is_up = stat.isup  # indicate if the interface is running
        duplex = stat.duplex  # the duplex communication type
        speed = stat.speed # speed in MB
        mtu = stat.mtu # MTU in B


def socket_monitoring():
    # get socket information at the beginning
    remote_ips = set()
    sockets = psutil.net_connections(kind='all')
    num_of_socks = len(sockets)
    for s in sockets:
        remote_ips.add(s.raddr)
    print("**************BEGINNING STATISTICS*****************")
    print(("number of sockets connections: {}").format(num_of_socks))
    print(remote_ips)
    step = 1
    sleep_time = 60  # in second
    while True:
        time.sleep(sleep_time)  # check statistics in every 2 minutes
        current_sockets = psutil.net_connections(kind='all')
        new_connection = set()
        for current_s in current_sockets:
            remote_ip = current_s.raddr
            if remote_ip in remote_ips:
                continue
            else:
                ip = remote_ip.ip
                port = remote_ip.port
                try:
                    addr = socket.gethostbyaddr(ip)
                    new_connection.add((addr[0], ip, port))
                except socket.herror:
                    new_connection.add(remote_ip)
                    pass

        print(("**************TIME={} min STATISTICS*****************").format(step * sleep_time / 60))
        print(("number of sockets connections: {}").format(len(current_sockets)))
        if len(new_connection) == 0:
            print("no new connection found")
        else:
            print("new connections not found in at the beginning: ")
            print(new_connection)

        step += 1


if __name__ == '__main__':
    socket_monitoring()
