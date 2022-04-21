import socket
import sys

def start_receiver(HOST, PORT):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server.bind((socket.gethostname(), 65432)) #TODO: handle ports 
    server.listen(30) #listens for 30 active connections

    while True: 
        conn, addr = server.accept() 
        with conn: 
            message = conn.recv(2048).decode('UTF-8')
            if (message.startswith('__SETUP')):
                conn.close() #TODO: check if setup_node wird ausgeführt
                setup_node(message)
            else: 
                splitMessage = message.split(" ", 2) #PACKET DEFINITION: packet = sourceIP targetNode rest:message 
                if(splitMessage[1] == HOST): #target is this machine --> print message 
                    print(splitMessage[0], ": ", splitMessage[2])
                    conn.close()
                else: 
                    conn.close() #TODO: check if forward message noch aufgerufen wird 
                    print("forward")
                    forward_message(message) 

def forward_message(message):
    #TODO: check connections of this node -> see who it has to be delivered to 
    #get ip if in forwarding table 
    # server.connect((splitMessage[1], PORT)) #TODO: handle different ports 
    # server.send(message.encode('UTF-8'))
    NotImplemented

def setup_node(message):
    #TODO: message aufsplitten (node + connections, nodelist, ...) 
    #TODO: forwarding TABLE !!! einrichten 
    NotImplemented
    
if __name__ == '__main__':
   # checks whether sufficient arguments have been provided
    if len(sys.argv) != 3: 
        print("Correct usage: script, IP address, port number")
        exit()
    start_receiver(str(sys.argv[1]), int(sys.argv[2])) #host ip and port are given via command line 
