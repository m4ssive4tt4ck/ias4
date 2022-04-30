import sys
import socket
import json
import numpy as np
import numpy_converter as nc


# pure tcp sender
#ip and port provided via command line 
def send_message(HOST, PORT):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((socket.gethostname(), 54322))  # TODO: gethostname überprüfen
    server.connect((HOST, PORT))
    while True:
        message = sys.stdin.readline("type your message") #format: targetNodeName message 
        message = HOST + message  # VORGABE EINGABE: HOST(=sourceNode) targetNodeName message TODO: use nodename instead of IP
        server.send(message.encode('UTF-8'))
        server.close()  # close connection directly after sending message


#TODO: remove
def setup_network_topology(network_topology):
    file = open(network_topology) #feed network topology file ('network_topology_1.json')
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
def read_network(network_topology):
    f = open(network_topology) #TODO: check if it works
    network = json.load(f)

    nodelist = network["nodelist"]

    all_arrays = []
    allnodes = []
    all_addresses = []
    for i in range(len(nodelist)):
        allnodes.append(nodelist[i]["nodename"])
        all_addresses.append((nodelist[i]["ip"], int(nodelist[i]["port"])))

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
                    # DONE: add actual port
                    ports[allnodes.index(connection["nodename"])] = connection["port"]

        all_arrays.append(np.array([first_line, allnodes, costs, neighbours, ips, ports]))
    all_arrays[-1][0, 2] = "final"
    i = 0
    for array in all_arrays:
        # print(array)
        # print(all_addresses[i])
        message = str.encode(nc.array_to_string(array))
        address = all_addresses[i]
        i += 1

        # TODO send to recipients
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((socket.gethostname(), 54322))  # TODO: gethostname überprüfen
        server.connect(address)  # TODO: print address (ip, port)
        while True:
            server.send("__SETUP", message)  # TODO: message to bytes ??!!
            server.close()  # close connection directly after sending message


if __name__ == '__main__':
    if (sys.argv[1] == 'SETUP'):
        read_network(sys.argv[2])
    elif(sys.argv[1] == 'MESSAGE'):
        send_message(sys.argv[2], sys.argv[2])
    else: 
        print("Correct usage: script SETUP <filename>")
        print("Correct usage: script MESSAGE <source host> <source port>")
    exit()
    
    #TODO: checks whether sufficient arguments have been provided
