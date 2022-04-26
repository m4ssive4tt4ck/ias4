import socket
import sys
import time
import numpy as np

import numpy_converter
from cost_array import update as update
from cost_array import initialize as initialize
from cost_array import cost_array as ca
import numpy_converter as nc


def start_receiver(HOST, PORT):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((socket.gethostname(), 65432))  # TODO: handle ports
    server.listen(30)  # listens for 30 active connections

    while True:
        time.sleep(0.01)
        conn, addr = server.accept()
        with conn:
            message_array = nc.string_to_array(conn.recv(2048).decode())
            if message_array[0, 0] == "init":
                conn.close()  # TODO: check if setup_node wird ausgeführt
                initialize(message_array)
                print("newly initialized")
                if message_array[0, 1] == "last":
                    NotImplemented
                    # TODO send update to all
            elif message_array[0, 0] == "update":
                update(message_array)
            elif message_array[0, 0] == "whisper":
                if message_array[0, 1] == HOST:
                    print(message_array[0, 2])
                    conn.close()
                else:
                    conn.close()  # TODO: check if forward message noch aufgerufen wird
                    print("forward")
                    destination_index = np.argwhere(ca[1, :] == message_array[0, 2])
                    next_ip = ca[destination_index[4, destination_index]]
                    next_port = int(ca[destination_index[5, destination_index]])
                    server.connect((next_ip, next_port))
                    server.send(numpy_converter.array_to_string(message_array))
                    server.close()


def forward_message(message_array, address):
    # TODO: check connections of this node -> see who it has to be delivered to
    # get ip if in forwarding table
    # server.connect((splitMessage[1], PORT)) #TODO: handle different ports 
    # server.send(message.encode('UTF-8'))
    NotImplemented


def setup_node(message):
    # TODO: message aufsplitten (node + connections, nodelist, ...)
    # TODO: forwarding TABLE !!! einrichten
    NotImplemented


if __name__ == '__main__':
    # checks whether sufficient arguments have been provided
    if len(sys.argv) != 3:
        print("Correct usage: script, IP address, port number")
        exit()
    start_receiver(str(sys.argv[1]), int(sys.argv[2]))  # host ip and port are given via command line
