import socket

def broadcast_listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", 5000))  # Listen on all interfaces
    while True:
        data, addr = sock.recvfrom(1024)
        if data == b"DISCOVER":
            # Respond with the server IP
            server_ip = socket.gethostbyname(socket.gethostname())
            sock.sendto(server_ip.encode(), addr)

broadcast_listener()