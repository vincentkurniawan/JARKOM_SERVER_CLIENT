# Kelompok :
# Nadia Clarissa Hermawan / 6181901013
# Vincent Kurniawan / 6181901024

import socket, time, threading

# score state collection
SCORE_STATE_TRUE = 1
SCORE_STATE_FALSE = 2
SCORE_STATE_NOTSET = 3

# answer collection
ANSWER_A = 1
ANSWER_B = 2
ANSWER_C = 3
ANSWER_D = 4

class Main():
    def __init__(self):
        self.setupClient()


    #setup the client connection with the server
    def setupClient(self):
        #define the server's address & port on which you want to connect
        server_host = '127.0.0.1'
        server_port = 8080
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #connect to server on local computer
        self.client.connect((server_host, server_port))
        print("Hello! you are now connected to the server..")
        
        #begin QnA rounds
        self.client.send("init".encode('utf-8'))
        while True:
            self.question_answer_recv()
        

    def question_answer_recv (self):
        data0 = self.client.recv(1024)
        data0 = data0.decode('utf-8')
        data = list(data0.split("_"))
        if (len(data) > 2):
            for j in range (5, 0, -1):
                print ('Please wait ', j, ' seconds for next question ...')
                time.sleep(1)
            self.handler_question_score(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])
        else:
            server_score = data[0]
            client_score = data[1]
            print ("<==========================================>")
            print ('FINAL SCORE:')
            print ("<==========================================>")
            print ('YOU : ', client_score, ' OTHER PLAYER : ', server_score)
            print ("<==========================================>")
            for i in range (10, 0, -1):
                print ('The game will shut down in ', i, ' ...')
                time.sleep(1)
            print ("<==========================================>")
            self.client.close()
            exit()


    def handler_question_score (self, question_number, question, answer_a, answer_b, answer_c, answer_d, current_score, state_score):
        question_number = int(question_number) + 1
        question_number = str(question_number)

        if (int(state_score) == SCORE_STATE_TRUE):
            print ('\nYour Answer is Correct !\n')
        elif (int(state_score) == SCORE_STATE_FALSE):
            print ('\nYour Answer is Wrong !\n')

        print ("<==========================================>")
        print ("\nYour Current Score : ",current_score,'\n')
        print ("<==========================================>")
        print ("<==========================================>")
        print ("\nQuestion ",question_number,'\n')
        print ("<==========================================>")
        print (question, '\n')
        
        print ("A: " + answer_a)
        print ("B: " + answer_b)
        print ("C: " + answer_c)
        print ("D: " + answer_d + "\n")
        print ("Type your answer (A/B/C/D) :\n")

        self.client_wait = True
        self.exceed_time = False
         
        threading.Thread(target=self.client_wait_time).start()
        answer = str(input())
        if (self.exceed_time):
            answer = "INVALID"
        self.client_wait = False
        
        print ('Waiting for host response ...')
        self.handler_answer_send(answer)


    def handler_answer_send (self, answer):
        msg = str(answer)
        self.client.send(msg.encode('utf-8'))


    def client_wait_time (self):
        check = True
        print ('You have 10 seconds left to answer ...')
        for i in range (10, 0, -1):
            if (self.client_wait == False):
                check = False
                break
            time.sleep(1)
        # kalau ga jawab dalam 10 detik:
        if (check):
            print ("Your time is up! You didn't get any score :( ")
            print ("Please input anything to proceed the next question ...")
            self.exceed_time = True


if __name__ == '__main__':
    cui = Main()