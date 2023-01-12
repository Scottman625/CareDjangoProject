import socket

db = 'postgres'
addr = socket.getaddrinfo(db, 5432, 0, socket.SOCK_STREAM, socket.IPPROTO_TCP)
print(addr)