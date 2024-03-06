 # Python program to implement server side of chat room. 
import socket 
import select 
import sys 



class Server():
    
    def __init__(self, ip_address="127.0.0.1", port=12345) -> None:
        self.clients = {}
        self.ip_address = ip_address
        self.port = port
        self.games = {}
        
    def start_server(self):
        """
        
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allows us to reuse address
        s.bind((self.ip_address, self.port))
        s.listen()  # increase this number to increase the amount of people in a chatroom
        sockets_list = [s]
        print(f"Chatroom open on {self.ip_address} on port {self.port}")
        while True:
            read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

            for client_socket in read_sockets:
                # Server is notified of a new connection
                if client_socket == s:
                    client_conn, client_addr = s.accept()
                    user = self.receive_message(client_conn)
                    # User disconnected before sending username
                    if user is False:
                        continue
                    sockets_list.append(client_conn)
                    self.clients[client_conn] = user
                    self.clients[client_conn] = {'game': None}
                    print(f"{user['data'].decode('utf-8')} joined from {client_addr[0]}:{client_addr[1]}")
                # Existing socket is sending message
                else:
                    msg = self.receive_message(client_socket)
                    # If no message is accepted, then close the connection
                    if msg is False:
                        print(f"{self.clients[client_socket]['data'].decode('utf-8')} has disconnected")
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
                            msg = 'Please finish or forfeit your game with "/forfeit"'.encode('utf-8')
                            msg_header = f"{len(msg):<10}".encode('utf-8')
                            client_socket.send(user['header'] + "Server".encode('utf-8') + msg_header + msg)  # use user['header'] as its a known header length
                            continue

                        # Find and validate opponent
                        opponent_name = msg['data'].decode()[11:]
                        opponent_conn = self.validate_opponent(user['data'], opponent_name)
                        if opponent_conn is False:
                            msg = "Invalid user".encode('utf-8')
                            msg_header = f"{len(msg):<10}".encode('utf-8')
                            client_socket.send(user['header'] + "Server".encode('utf-8') + msg_header + msg)  # use user['header'] as its a known header length
                            continue
                        
                        # Generate a unique game key and create the game
                        gamekey = client_socket + opponent_conn
                        user['game'] = gamekey
                        self.clients[opponent_conn]['game'] = gamekey
                        self.games[gamekey] 


                    print(f"Received message from {user['data'].decode('utf-8')}")
                    # Send message to all connect clients
                    self.broadcast(client_socket, user, msg)

    def broadcast(self, client_socket, user, msg):
        for client in self.clients:
            if client != client_socket:
                client.send(user['header'] + user['data'] + msg['header'] + msg['data'])

    def receive_message(self, conn):
        try:
            message_header = conn.recv(10)
            if not len(message_header):
                return False
            message_length = int(message_header.decode('utf-8').strip())
            return {'header': message_header, 'data': conn.recv(message_length)}
        except:
            return False
        
    def generate_tictactoe_game(self, user_conn, opponent_conn):
        """I AM WORKING HERE RIGHT NOW

        Args:
            user_conn (_type_): _description_
            opponent_conn (_type_): _description_
        """
        gamekey = user_conn + opponent_conn
        self.clients[user_conn]['game']  = gamekey
        self.clients[opponent_conn]['game'] = gamekey
        self.games[gamekey] = {
            player1 = 
        }
        
    def play_tictactoe(self, msg):
        pass

    def validate_opponent(self, user, opponent):
        for client_conn, client_user in self.clients.items():
            if client_user == user:
                return False
            elif client_user == opponent:
                return client_conn
        return False

        
    # Add a check for a message with a game
                            

if __name__ == '__main__':
    server = Server()
    server.start_server()
