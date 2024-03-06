import socket
import sys
import errno
import time


HEADER_LENGTH = 10
SERVER_IP = "127.0.0.1"
PORT = 12345

def receive_message(s):
    try:
        while True:
            username_header = s.recv(HEADER_LENGTH)
            if not len(username_header):
                print("Connection closed")
                sys.exit

            # Receive and decode username
            username_length = int(username_header.decode('utf-8'.strip()))
            username = s.recv(username_length).decode('utf-8')

            # Decode and display the received message
            msg_header = s.recv(HEADER_LENGTH)
            msg_length = int(msg_header.decode('utf-8').strip())
            msg = s.recv(msg_length).decode('utf-8')

            print(f'<{username}> {msg}')
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()
            
            
def main():
    """
    Using a socket to GET a file
    """

    username = " "
    client_username = input("Enter a username: ")
    username = client_username.encode('utf-8')
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_IP, PORT))
    s.setblocking(False)
    print(f"Connected to {SERVER_IP}:{PORT}\n"
            'To play TicTacToe enter "/tictactoe playername"\n'\
            'To leave the chat room, enter "/q"')
    s.sendall(username_header + username)

    while True:
        game_move = False
        msg = input(f"<{client_username}> ")
        if msg:
            # Check to see if the client is trying to play a move
            # If the client is trying to play a move, then we know that the server will definitely reply and
            # we should try to get the updated board.
            if msg[0] == "/":
                game_move = True
            msg = msg.encode('utf-8')
            msg_header = f"{len(msg):<{HEADER_LENGTH}}".encode('utf-8')
            s.send(msg_header + msg)
            if game_move:
                time.sleep(0.2)
                receive_message(s)
        # Get messages and print them
        receive_message(s)

main()
