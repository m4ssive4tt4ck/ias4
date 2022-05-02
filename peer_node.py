import socket
import sys
import time
import numpy as np

import numpy_converter
from cost_array import update as update
from cost_array import initialize as initialize
from cost_array import cost_array as ca
from cost_array import pending_messages as pending
import numpy_converter as nc

own_name = ""
all_init = False


# sends all pending messages (pending, if the final node has not yet been initialized)
def send_pending(HOST, PORT):
    global pending
    pending2 = []
    for message in pending:

        # tcpSenderServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # tcpSenderServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #to reuse address
        # tcpSenderServer.bind((HOST, PORT))

        sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)  # to reuse address
        sender_socket.bind((HOST, PORT + 10))  # TODO: random port --> weil mehrere nodes auf gleichem gerät laufen
        # server.listen(30)  # listens for 30 active connections
        try:
            sender_socket.connect(message[0])
            sender_socket.send(str.encode(numpy_converter.array_to_string(message[1:])))
        except:
            # print("in exception", message)
            pending2.append(message)
            print("pending2: ", pending2)
        sender_socket.close()
    pending.clear()
    pending = pending2


def start_receiver(HOST, PORT):
    print("receiving on ", HOST, " ", PORT)
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)  # to reuse address
    receiver_socket.bind((HOST, PORT))  # TODO: handle ports
    receiver_socket.listen(100)  # listens for 100 active connections
    time.sleep(0.01)
    global all_init
    global pending
    while True:
        conn, addr = receiver_socket.accept()
        with conn:
            if all_init and len(pending) > 0:
                send_pending(HOST, PORT)
            message_array = nc.string_to_array(conn.recv(2048).decode())
            if message_array[0, 0] == "reset":
                conn.close()  # TODO: check if setup_node wird ausgeführt
                global own_name
                own_name = message_array[0, 1]

                initialize(message_array)
                all_init = False
                print("newly initialized")
                if message_array[0, 2] == "final":
                    # send update to all
                    all_init = True
                    # for message in pending: #instead of 
                    #     print(message[0])
                    #     server.connect(message[0])
                    #     server.send(str.encode(numpy_converter.array_to_string(message[1:])))
                    #     server.close() #TODO: neccessary here ?? closes only connection ...  (?)
                    # pending.clear()
            elif message_array[0, 0] == "update":
                update(message_array)
                send_pending(HOST, PORT)
                # for message in pending: #instead of send_pending(HOST, PORT)
                #     print(message[0])
                #     server.connect(message[0])
                #     server.send(str.encode(numpy_converter.array_to_string(message[1:])))
                #     server.close() #TODO: neccessary here ?? closes only connection ...  (?)
                # pending.clear()
            elif message_array[0, 0] == "whisper":
                if message_array[0, 1] == own_name:
                    print(message_array[0, 2])
                    conn.close()
                else:
                    conn.close()  # TODO: check if forward message noch aufgerufen wird
                    print("forward")
                    destination_index = np.argwhere(ca[1, :] == message_array[0, 2])
                    next_ip = ca[destination_index[4, destination_index]]
                    next_port = int(ca[destination_index[5, destination_index]])
                    receiver_socket.connect((next_ip, next_port))
                    receiver_socket.send(str.encode(numpy_converter.array_to_string(message_array)))
                    receiver_socket.close()


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
