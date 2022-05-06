# Kelompok :
# Nadia Clarissa Hermawan / 6181901013
# Vincent Kurniawan / 6181901024

import socket, threading
import time
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


rounds = [Round("Nama lapisan protokol internet yang berfungsi untuk mengatur routing datagram dan informasi IP dari source ke destination ?", 3, "Link Layer", "Transport Layer", "Network Layer", "Application Layer"), 
            Round("Nama lapisan protokol internet yang berfungsi untuk membuat paket agar dapat di transfer dari satu device ke device lain serta melibatkan hardware ?", 1, "Link Layer", "Transport Layer", "Network Layer", "Application Layer"),
            Round("Disebut apakah fungsi dari network layer dalam menyalurkan paket dari port input router ke port output router ?", 4, "Decapsulation", "Encapsulation", "Routing", "Forwarding"),
            Round("Kapan fragmentasi dilakukan ?", 3, "Ketika ukuran MTU sebelumnya > dari MTU selanjutnya", "Ketika ukuran paket datagram > ukuran MTU", "A & B", "Tidak ada yang benar"),
            Round("Akan dikirimkan paket sebesar 8000 byte dari komputer A ke komputer B. MTU A = 10kB, MTU B = 576 byte. Berapakah fragment yang terbentuk ?", 2, "0", "15", "16", "20"),
            Round("Apa command yang digunakan untuk mengecek IP Address ?", 1, "ipconfig", "ipaddress", "netstat", "ping website.com"),
            Round("Network address : 192.168.1.0/24. Manakah network id nya ?", 2, ".0", "192.168.1", "192.168", "192"),
            Round("Network address : 192.168.1.0/24. Apakah host id nya ?", 3, "192.168.1", "192.168", ".0", "192"),
            Round("Apa arti Subnetting ?", 4, "Membuka warung kopi", "Menjalankan program di internet", "Memegang kendali dari suatu program", "Mengalokasikan IP address ke dalam beberapa bagian yang memiliki network id unik"),
            Round("Apa nama translator pada router yang bertugas mentranslasikan IP address lokal dari setiap device yang tekonek ke suatu WiFi agar dapat dikenali ISP ?", 4, "TAN", "ATN", "NAD", "NAT")
        ]


class ClientThread(threading.Thread) :
    #constructor
    def __init__(self, clientAddress, clientSocket) :
        threading.Thread.__init__(self)
        self.csocket = clientSocket
        self.caddress = clientAddress
        self.server_wait = True
        self.server_score = 0
        self.client_score = 0
        self.exceed_time = False
        print("New connection added: ", self.caddress)


    #thread.start() akan menjalankan ini
    def run(self) :
        print("Connection from: ", self.caddress)
        i = 0
        total_question_number = len(rounds)
        for i in range (0, total_question_number+1) :
            
            #terima message (mathematical operations) from client
            data = self.csocket.recv(2048)
            msg = data.decode('utf-8')
            score_state = SCORE_STATE_NOTSET

            #stopper connections 
            if msg == 'done':
                break

            elif(msg != 'init'):
                # evaluate client question answer
                if (self.evaluate_answer(i-1, self.convert_answer(msg))):
                    score_state = SCORE_STATE_TRUE
                    self.client_score += 100
                else:
                    score_state = SCORE_STATE_FALSE

            if (i < total_question_number):
                
                question_score = [i, rounds[i].question, rounds[i].a, rounds[i].b, rounds[i].c, rounds[i].d, self.client_score, score_state]
                str_question_score = "_".join(str(x) for x in question_score)
                self.csocket.send(str_question_score.encode('utf-8'))

                for j in range (5, 0, -1):
                    print ('Please wait ', j, ' seconds for next question ...')
                    time.sleep(1)

                # open cui on server player
                self.handler_question_score(i, rounds[i].question, rounds[i].a, rounds[i].b, rounds[i].c, rounds[i].d, self.server_score)
                
                self.server_wait = True
                self.exceed_time = False

                threading.Thread(target=self.server_wait_time).start()
                answer = str(input())
                if (self.exceed_time):
                    answer = "INVALID"
        
                if (self.evaluate_answer(i, self.convert_answer(answer))):
                        self.server_score += 100
                        print ("\nYour Answer is Correct !\n")
                else:
                        print ("\nYour Answer is Wrong !\n")
                print ("Waiting for player 2 response ...")
                self.server_wait = False
                
            i += 1
        
        # end game to client
        final_score = [self.server_score, self.client_score]
        str_final_score = "_".join(str(x) for x in final_score)
        self.csocket.send(str_final_score.encode('utf-8'))

        # end game on server
        print ("<==========================================>")
        print ('FINAL SCORE:')
        print ("<==========================================>")
        print ('YOU : ', self.server_score, ' OTHER PLAYER : ', self.client_score)
        print ("<==========================================>")
        for i in range (10, 0, -1):
            print ('The game will shut down in ', i, ' ...')
            time.sleep(1)
        print ("<==========================================>")
        print("Client at ", self.caddress, " disconnected...")


    def server_wait_time (self):
        check = True
        print ('You have 10 seconds left to answer ...')
        for i in range (10, 0, -1):
            if (self.server_wait == False):
                check = False
                break
            time.sleep(1)
        # kalau ga jawab dalam 10 detik:
        if (check):
            print ("Your time is up! You didn't get any score :( ")
            print ("Please input anything to proceed the next question ...")
            self.exceed_time = True


    def handler_question_score (self, question_number, question, answer_a, answer_b, answer_c, answer_d, current_score):

        print ("<==========================================>")
        print ("\nYour Current Score : ",current_score,'\n')
        print ("<==========================================>")
        print ("<==========================================>")
        print ("\nQuestion ",question_number+1,'\n')
        print ("<==========================================>")
        print (question, '\n')
        
        print ("A: " + answer_a)
        print ("B: " + answer_b)
        print ("C: " + answer_c)
        print ("D: " + answer_d + "\n")
        print ("Type your answer (A/B/C/D) :\n")
        

    def convert_answer (self, answer):
        answer = answer.lower()
        if (answer == 'a'):
            return 1
        elif (answer == 'b'):
            return 2
        elif (answer == 'c'):
            return 3
        elif (answer == 'd'):
            return 4
        else:
            return -100


    def evaluate_answer(self, question_number, answer):
        if (rounds[question_number].key == answer):
            return True
        return False


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
    