# Nadia Clarissa Hermawan / 6181901013
# we definitely dont need any GUI on the server side :)

import socket, threading
from _thread import *

class ClientThread(threading.Thread) :
    #constructor
    def __init__(self, clientAddress, clientSocket) :
        threading.Thread.__init__(self)
        self.csocket = clientSocket
        self.caddress = clientAddress
        print("New connection added: ", self.caddress)

    #thread.start() akan menjalankan ini
    def run(self) :
        print("Connection from: ", self.caddress)
        while True :
            #terima message (mathematical operations) from client
            data = self.csocket.recv(2048)
            msg = data.decode('utf-8')

            #stopper connections 
            if msg == 'done':
                break
                
            #do the mathematical operations
            res = str(self.count(msg))

            #sends back mathematical operations result to client
            self.csocket.send(res.encode('utf-8'))
            
        print("Client at ", self.caddress, " disconnected...")

    #method to do mathematical operations
    def count(self, msg) :
        try :
            return eval(msg)
        except SyntaxError :
            return 'Invalid syntax, please try again.. :('


def main():
    # define the server's addess & port, 
    # then bind it
    host = "127.0.0.1"
    port = 8080
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    print('Server started. Socket binded to port ', port)

    #put the socket into listening mode, 5 client at max
    server.listen(5)
    print("socket is listening, waiting for client request..")

    #TCP = keep connections until client wants to exit
    while True:
        #establish connection with client
        clientSocket, clientAddress = server.accept()  

        #start new thread to do operations & logic for each client
        newThread = ClientThread(clientAddress, clientSocket)
        newThread.start()
    
    #turn off server
    s.close()


if __name__ == '__main__':
    main()
    