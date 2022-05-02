import socket
import sys
import select
import time

def start_connection(HOST, PORT):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket (af_inet for ipv4 addresses, sock_stream for tcp) 
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT)) 
    server.listen(5) #listens for 5 active connections
    try:
        while True: 
            #wait(50) ms --> weil sonst spikt CPU nutzung 
            conn, addr = server.accept()
            with conn: 
                print(f"Connected by {addr}")
                read_sockets, write_socket, error_socket = select.select([sys.stdin, conn], [], [], 0) #select so it doesn't block

                for socks in read_sockets:
                    if socks == conn:
                        message = socks.recv(512).decode('UTF-8') 
                        if message == b'': 
                            break
                        print("Client: ", message)
                    else:
                        message = sys.stdin.readline()
                        conn.send(message.encode('UTF-8'))
                        sys.stdout.write("<You>")
                        sys.stdout.write(message)
                        sys.stdout.flush()
    finally: 
        server.close()

if __name__ == '__main__':
   # checks whether sufficient arguments have been provided
    if len(sys.argv) != 3: 
        print("Correct usage: script, IP address, port number")
        exit()
    start_connection(str(sys.argv[1]), int(sys.argv[2])) #host ip and port are given via command line 
