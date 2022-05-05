# Nadia Clarissa Hermawan / 6181901013
# we definitely dont need any GUI on the server side :)

import socket, threading
from _thread import *

# score state collection
SCORE_STATE_TRUE = 1
SCORE_STATE_FALSE = 2
SCORE_STATE_NOTSET = 3

class Round():
    #constructor
    def __init__(self, question, key, a, b, c, d):
        self.question = question
        self.key = key
        self.a = a
        self.b = b
        self.c = c
        self.d = d

rounds = [Round("Siapa penemu gravitasi ?", 2, "Albert Einstein", "Isaac Newton", "Duncan Lord", "Kingsman"), 
            Round("Apa nama makanan khas Italia ?", 1, "Pizza", "Burger", "Kentang goreng", "Sushi"),
            Round("question 3 ?", 2, "Albert Einstein", "Isaac Newton", "Duncan Lord", "Kingsman"),
            Round("question 4?", 2, "Albert Einstein", "Isaac Newton", "Duncan Lord", "Kingsman")
            ]

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
        i = 0
        client_score = 0
        while True :
            
            #terima message (mathematical operations) from client
            data = self.csocket.recv(2048)
            msg = data.decode('utf-8')

            if msg == 'init':
                question_score = [i+1, rounds[i].question, rounds[i].a, rounds[i].b, rounds[i].c, rounds[i].d, client_score, SCORE_STATE_NOTSET]
                
            #stopper connections 
            elif msg == 'done':
                break

            else:
                # evaluate client question answer
                if (self.evaluate_client_answer(i, msg)):
                    score_state = SCORE_STATE_TRUE
                else:
                    score_state = SCORE_STATE_FALSE
                question_score = [i+2, rounds[i+1].question, rounds[i+1].a, rounds[i+1].b, rounds[i+1].c, rounds[i+1].d, client_score, score_state]
            
            self.csocket.send(question_score.encode('utf-8'))
            i += 1
            
        print("Client at ", self.caddress, " disconnected...")

    def evaluate_client_answer (self, question_number, msg):
        if (rounds[question_number].key == msg):
            return True
        return False

    # #method to do mathematical operations
    # def count(self, msg) :
    #     try :
    #         return eval(msg)
    #     except SyntaxError :
    #         return 'Invalid syntax, please try again.. :('


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
    