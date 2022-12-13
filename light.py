import socket

host = "192.168.50.206"
port = 36157
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
offset = False

def show_single_light(index):
    buf = bytearray()
    buf.append(69)
    for i in range(150):
        if i == index:
            buf += bytearray([255, 255, 255])
        else:
            buf += bytearray([0, 0, 0])
    s.sendto(buf, (host, port))

def send_pattern(func):
    buf = bytearray()
    buf.append(69)
    for i in range(150):
        buf += bytearray(func(i))
    s.sendto(buf, (host, port))
    