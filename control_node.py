import sys
import socket
import json
import numpy as np


# pure tcp sender
def send_message():
    HOST = str(sys.stdin.readline(
        "Who should be the source of the message"))
    # first one to receive the message, as control_node is only for testing (IP)
    PORT = 65432

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((socket.gethostname(), 54322))  # TODO: gethostname überprüfen
    server.connect((HOST, PORT))
    while True:
        message = sys.stdin.readline("format: targetNodeName message")
        message = HOST + message  # VORGABE EINGABE: HOST(=sourceNode) targetNodeName message TODO: use nodename instead of IP
        server.send(message.encode('UTF-8'))
        server.close()  # close connection directly after sending message


def setup_network_topology():
    file = open('network_topology_1.json')
    network_topology = json.load(file)  # TODO: make global variable
    allnodes = ""

    for node in network_topology['nodelist']:
        allnodes += node['nodename'] + " "

    for node in network_topology['nodelist']:
        print(node)
        # send nodelist with nodenames only + whole object of node to node
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((socket.gethostname(), 54322))  # TODO: gethostname überprüfen
        server.connect((node['ip'], 65432))  # TODO: woher weiss ich den port ...
        while True:
            server.send("__SETUP", node.encode('UTF-8'), allnodes.encode('UTF-8'))  # TODO: check
            server.close()  # close connection directly after sending message


# TODO: method to give new file to setup_network_topology(file)
def read_network():
    f = open("network_topology_1.json")
    network = json.load(f)

    nodelist = network["nodelist"]

    all_arrays = []
    allnodes = []
    for i in range(len(nodelist)):
        allnodes.append(nodelist[i]["nodename"])

    for current_node in allnodes:
        costs = ["-1"] * len(allnodes)
        neighbours = [""] * len(allnodes)
        ips = [""] * len(allnodes)
        ports = [""] * len(allnodes)
        first_line = [""] * len(allnodes)
        first_line[0] = "reset"
        first_line[1] = current_node
        for i in range(len(allnodes)):
            if nodelist[i]["nodename"] == current_node:
                for connection in nodelist[i]["connections"]:
                    costs[allnodes.index(connection["nodename"])] = connection["RTT"]
                    neighbours[allnodes.index(connection["nodename"])] = connection["nodename"]
                    ips[allnodes.index(connection["nodename"])] = connection["ip"]
                    # TODO add actual port
                    ports[allnodes.index(connection["nodename"])] = str(65432)

        all_arrays.append(np.array([first_line, allnodes, costs, neighbours, ips, ports]))
    all_arrays[-1][0, 2] = "final"
    for array in all_arrays:
        print(array)
    # TODO send to recipients


if __name__ == '__main__':
    read_network()
    # setup_network_topology()

    # checks whether sufficient arguments have been provided
    # send_message()
