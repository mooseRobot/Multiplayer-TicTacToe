import socket

def send_message(socket, dst):
    """
    Sends a message to a server/client using a socket

    Args:
        socket: socket
        msg (str): Message to send
        dst (str): The IP address of the receiver
    """

    msg = input(f"Message {dst}\n")
    socket.send(bytes(msg, encoding="utf-8"))


def receive_message(socket):
    """

    """
    response = socket.recv(4096)
    msg = response
    while len(response) > 0:
        msg = msg + response
        response = socket.recv(4096)
    return msg

