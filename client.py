import socket
import sys
import time

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 9999))
    print("Socket Created")
except socket.error as err:
    print(f"Socket Creation Failed: {err}")
    sys.exit(0)

# while True:
#     msg = s.recv(1024).decode()
#     print(msg)
#     if '\nquit\n' == msg:
#         break

#     print(f'Client: {msg}')

#     s.send('Client: Sending Messaqge'.encode())

s.send('Client: Sending Messaqge'.encode())
time.sleep(3)

s.shutdown(socket.SHUT_RDWR)
s.close()