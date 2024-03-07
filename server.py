# Python program to implement server side of chat room.
import socket
import select
import uuid
from tictactoe import TicTacToe


class Server():

    def __init__(self, ip_address="127.0.0.1", port=12345) -> None:
        self.clients = {}
        self.ip_address = ip_address
        self.port = port
        self.games = {}
        self.servername = "Server".encode('utf-8')
        self.serverheader = f"{len(self.servername):<{10}}".encode('utf-8')

    def start_server(self):
        """

        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allows us to reuse address
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.ip_address, self.port))
        s.listen()  # increase this number to increase the amount of people in a chatroom
        sockets_list = [s]
        print(f"Chatroom open on {self.ip_address} on port {self.port}")
        while True:
            read_sockets, _, exception_sockets = select.select(
                sockets_list, [], sockets_list)

            for client_socket in read_sockets:
                # Server is notified of a new connection
                if client_socket == s:
                    client_conn, client_addr = s.accept()
                    user = self.receive_message(client_conn)
                    # User disconnected before sending username
                    if user is False:
                        continue
                    sockets_list.append(client_conn)
                    self.clients[client_conn] = {'user': user, 'game': None}
                    print(
                        f"{user['data'].decode('utf-8')} joined from {client_addr[0]}:{client_addr[1]}")
                # Existing socket is sending message
                else:
                    msg = self.receive_message(client_socket)
                    # If no message is accepted, then close the connection
                    if msg is False:
                        print(
                            f"{self.clients[client_socket]['user']['data'].decode('utf-8')} has disconnected")
                        sockets_list.remove(client_socket)
                        del self.clients[client_socket]
                        continue
                    user = self.clients[client_socket]
                    # Create a method for the server to send a message....

                    # Add a check for game move
                    # Check if the user is in a game otherwise ignore
                    # then check if it is the users turn
                    # Then call a method that checks if the move is valid

                    # Then we check for a winner.
                    # Print board and announce winner if there is.

                    # Add a check for /forfeit

                        
                            
                        

                    if msg['data'].decode()[:11] == "/tictactoe ":
                        if user['game'] != None:
                            msg = 'Please finish or forfeit your game with "/forfeit"'.encode(
                                'utf-8')
                            msg_header = f"{len(msg):<{10}}".encode('utf-8')
                            client_socket.send(
                                self.serverheader + self.servername + msg_header + msg)
                            continue

                        # Find and validate opponent
                        opponent_name = msg['data'].decode()[11:]
                        opponent_conn = self.validate_opponent(
                            user['user']['data'], opponent_name)
                        if opponent_conn is False:
                            self.send_message(client_socket, "Invalid user")
                            # msg = "Invalid user".encode('utf-8')
                            # msg_header = f"{len(msg):<{10}}".encode('utf-8')
                            # client_socket.send(
                            #     self.serverheader + self.servername + msg_header + msg)
                            continue

                        # Generate a unique game key and create the game
                        gamekey = uuid.uuid1().int
                        game = TicTacToe([client_socket, opponent_conn])
                        user['game'] = gamekey
                        self.clients[opponent_conn]['game'] = gamekey
                        self.games[gamekey] = game

                        # Construct message to send
                        board_str = self.games[gamekey].print_board()
                        msg = f"Welcome to TicTacToe! To play a move enter /x,y. x and y can be from any value 1-3.\n{self.clients[game.get_current_turn()]['user']['data'].decode('utf-8')}'s turn.\n" + board_str
                        msg_header = f"{len(msg):<10}".encode('utf-8')
                        self.broadcast(client_socket, self.serverheader,
                                       self.servername, msg_header, msg.encode('utf-8'))
                        # Send message to person who initiated the game
                        client_socket.send(
                            self.serverheader + self.servername + msg_header + msg.encode('utf-8'))
                        continue
                    
                    if msg['data'].decode()[:1] == "/":
                        if user['game'] == None:
                            self.send_message(client_socket, "You are currently not in a game. Start a game with /tictactoe playername")
                            continue
                        
                        x_coord = msg['data'].decode()[1]
                        if msg['data'].decode()[3] == ' ':
                            y_coord = msg['data'].decode()[4]
                        else:
                            y_coord = msg['data'].decode()[3]
                        if not x_coord.isnumeric() or not y_coord.isnumeric():
                            msg = "Did you mean to play a move? /x,y".encode('utf-8')
                            msg_header = f"{len(msg):<{10}}".encode('utf-8')
                            client_socket.send(
                                self.serverheader + self.servername + msg_header + msg.encode('utf-8'))
                            continue

                    print(
                        f'Received message from {user["user"]["data"].decode("utf-8")}: {msg["data"].decode("utf-8")}')
                    # Send message to all connect clients
                    self.broadcast(
                        client_socket, user['user']['header'], user['user']['data'], msg['header'], msg['data'])
                    
                    
                    
    def send_message(self, client_socket, msg):
        """Sends a message to an individual user

        Args:
            client_socket (socket): the users socket
            msg (str): The message to send
        """
        msg_header = f"{len(msg):<{10}}".encode('utf-8')
        client_socket.send(
            self.serverheader + self.servername + msg_header + msg.encode('utf-8'))

    def broadcast(self, client_socket, user_header, user_data, msg_header, msg_data):
        for client in self.clients:
            if client != client_socket:
                client.send(user_header + user_data + msg_header + msg_data)

    def receive_message(self, conn):
        try:
            message_header = conn.recv(10)
            if not len(message_header):
                return False
            message_length = int(message_header.decode('utf-8').strip())
            return {'header': message_header, 'data': conn.recv(message_length)}
        except:
            return False

    def validate_opponent(self, user, opponent):
        for client_conn, client_user in self.clients.items():
            client_to_check = client_user['user']['data'].decode("utf-8")
            if client_to_check == user:
                return False
            elif client_to_check == opponent:
                return client_conn
        return False

    # Add a check for a message with a game


if __name__ == '__main__':
    server = Server()
    server.start_server()
