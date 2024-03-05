import socket
import message

# Citation for the following function:
# Date: 1/18/2024
# Adapted from:
# https://docs.python.org/3/library/socket.html
def http_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 12345))
    s.listen()
    conn, addr = s.accept()
    
    print("Connected by ", {addr})
    connected = True
    with conn:
        while connected:
            req = conn.recv(4096)  # Receive request
            print(f"\n{addr[0]}:", req.decode())
            msg = input(f"Message {addr[0]}\n")
            conn.send(bytes(msg, encoding='utf-8'))

if __name__ == '__main__':
    http_server()


# def http_server():
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.bind(("127.0.0.1", 12345))
#     s.listen()
#     conn, addr = s.accept()
    
#     print("Connected by ", {addr})
#     connected = True
#     with conn:
#         while connected:
#             response_msg = message.receive_message(conn)
#             print(response_msg.decode())

#             message.send_message(conn, addr)
#             print('Server awaiting response')
