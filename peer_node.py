import socket
import sys

def start_receiver(HOST, PORT):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server.bind((HOST, PORT)) 
    server.listen(30) #listens for 30 active connections
   
    while True: 
        conn, addr = server.accept()
        splitMessage;  
        with conn: 
            #TODO: add connection to known connections 
            message = conn.recv(2048).decode('UTF-8')
            splitMessage = message.split(" ", 2) #PACKET DEFINITION: packet = sourceIP targetNode rest:message 
            if(splitMessage[1] == HOST): #target is this machine --> print message 
                print(splitMessage[0], ": ", splitMessage[2])
            conn.close()
           
        #TODO: check forwarding table and what to do if not found 
        server.connect((splitMessage[1], PORT)) #TODO: handle different ports 
        #TODO:send to other connection ... server.send() --> connection muss erst bestehen
        server.send(message.encode('UTF-8'))
        print("forward")
           
        # server.close()

#TODO: NTU etc... 

if __name__ == '__main__':
   # checks whether sufficient arguments have been provided
    if len(sys.argv) != 3: 
        print("Correct usage: script, IP address, port number")
        exit()
    start_server(str(sys.argv[1]), int(sys.argv[2])) #host ip and port are given via command line 
