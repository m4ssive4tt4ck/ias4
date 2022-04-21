import sys
import socket
import select

#pure tcp sender 
def start_connection(HOST, PORT):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server.bind((socket.gethostname(), 54322)) #TODO: gethostname überprüfen 
    server.connect((HOST, PORT))
    while True:
        message = sys.stdin.readline()
        #VORGABE EINGABE: targetNodeName message
        #TODO: add sourceNode to message 
        server.send(message.encode('UTF-8'))
        server.close() #close connection directly after sending message

#TODO: send NTU to all nodes 
#knows all connections (all ips)

#For simplicity, the network topology is read-in from a file in a simplistic raw format.
#In other words, it can be a list of node-names with IPs, and a list of node-names with
#connections to some other node-names, each with an integer number for its RTT. The
#exact format can be chosen freely.

if __name__ == '__main__':
    # checks whether sufficient arguments have been provided
    if len(sys.argv) != 3:
        print("Correct usage: script, Host IP address, port number")
        exit()
    start_connection(str(sys.argv[1]), str(sys.argv[2]))
