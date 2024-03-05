import socket


SERVER_IP = "127.0.0.1"
PORT = 12345

def get_a_file():
    """
    Using a socket to GET a file
    """
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_IP, PORT))
    connected = True
    print(f"Connected to {SERVER_IP}:{PORT}")
    
    while connected:
        msg = input(f"Message {SERVER_IP}...\n")
        s.send(bytes(msg, encoding='utf-8'))

        # Taken from get_large_file
        response = s.recv(4096)
        server_msg = response
        while len(response) > 0:
            server_msg = server_msg + response
            response = s.recv(4096)
        print(server_msg.decode())

    s.close()
    return response

print(get_a_file())
