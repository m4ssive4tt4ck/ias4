import sys
import socket
import json

#pure tcp sender 
def send_message():
    HOST = str(sys.stdin.readline("Who should be the source of the message")) #first one to receive the message, as control_node is only for testing (IP)
    PORT = 65432

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server.bind((socket.gethostname(), 54322)) #TODO: gethostname überprüfen 
    server.connect((HOST, PORT))
    while True:
        message = sys.stdin.readline("format: targetNodeName message")
        message = HOST + message #VORGABE EINGABE: HOST(=sourceNode) targetNodeName message TODO: use nodename instead of IP 
        server.send(message.encode('UTF-8'))
        server.close() #close connection directly after sending message

def setup_network_topology():
    file = open('network_topology_1.json') 
    network_topology = json.load(file) #TODO: make global variable
    allnodes = ""

    for node in network_topology['nodelist']:
        allnodes += node['nodename'] + " "

    for node in network_topology['nodelist']:
        print(node)
        #send nodelist with nodenames only + whole object of node to node 
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        server.bind((socket.gethostname(), 54322)) #TODO: gethostname überprüfen 
        server.connect((node['ip'], 65432)) #TODO: woher weiss ich den port ... 
        while True:
            server.send("__SETUP", node.encode('UTF-8'), allnodes.encode('UTF-8') ) #TODO: check
            server.close() #close connection directly after sending message 

#TODO: method to give new file to setup_network_topology(file)

if __name__ == '__main__':
    setup_network_topology() 

    # checks whether sufficient arguments have been provided
    send_message()
