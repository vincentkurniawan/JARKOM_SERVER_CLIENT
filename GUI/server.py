# Nadia Clarissa Hermawan / 6181901013
# we definitely dont need any GUI on the server side :)

from functools import partial
import socket, threading
import time
from _thread import *
import tkinter as tk

# score state collection
SCORE_STATE_TRUE = 1
SCORE_STATE_FALSE = 2
SCORE_STATE_NOTSET = 3

# answer collection
ANSWER_A = 1
ANSWER_B = 2
ANSWER_C = 3
ANSWER_D = 4

window = tk.Tk()

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
        self.server_wait = True
        self.server_score = 0
        self.client_score = 0

        self.server_answer = -100

        print("New connection added: ", self.caddress)
        self.setupGUI()

    def setupGUI (self):
        self.window = window
        self.window.title('KAHUUT !! (SERVER)')

        #create the empty frame 
        self.create_display_frame()
        self.create_display_labels()

    def create_display_frame(self):
        self.frame_title = tk.Frame(self.window, relief='sunken')
        self.frame_title.pack(fill='both', expand=True, padx=10, pady=10)

        self.frame_button = tk.Frame(self.window, relief='sunken')
        self.frame_button.pack(fill='both', expand=True, padx=10, pady=10)

        self.frame_result = tk.Frame(self.window, relief='sunken')
        self.frame_result.pack(fill='both', expand=True, padx=10, pady=10)


    def create_display_labels(self):
        self.title = tk.Label(self.frame_title, text='', font = ('Courier New', 18))
        self.title.pack()

        self.question = tk.Label(self.frame_title, text='', font = ('Courier New', 18))
        self.question.pack()

        self.answer_a = tk.Button(self.frame_button, text='', font = ('Courier New', 18), bg='#9FB4FF', command=partial(self.handler_answer_send, ANSWER_A))
        self.answer_a.pack()

        self.answer_b = tk.Button(self.frame_button, text='', font = ('Courier New', 18), bg='#9FB4FF', command=partial(self.handler_answer_send, ANSWER_B))
        self.answer_b.pack()

        self.answer_c = tk.Button(self.frame_button, text='', font = ('Courier New', 18), bg='#9FB4FF', command=partial(self.handler_answer_send, ANSWER_C))
        self.answer_c.pack()

        self.answer_d = tk.Button(self.frame_button, text='', font = ('Courier New', 18), bg='#9FB4FF', command=partial(self.handler_answer_send, ANSWER_D))
        self.answer_d.pack()

        self.score_state = tk.Label(self.frame_result, text='', font = ('Courier New', 18))
        self.score_state.pack()

        self.score = tk.Label(self.frame_result, text='', font = ('Courier New', 18))
        self.score.pack()

        self.status = tk.Label(self.frame_result, text='', font = ('Courier New', 18))
        self.status.pack()

    def handler_answer_send(self, answer):
        self.answer = str(answer)
        self.server_wait = False
        self.status['text'] = 'Waiting for other player ...'

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
                if (self.evaluate_answer(i-1, int(msg))):
                    score_state = SCORE_STATE_TRUE
                    self.client_score += 100
                else:
                    score_state = SCORE_STATE_FALSE

            if (i < total_question_number):
                
                question_score = [i, rounds[i].question, rounds[i].a, rounds[i].b, rounds[i].c, rounds[i].d, self.client_score, score_state]
                str_question_score = "_".join(str(x) for x in question_score)
                self.csocket.send(str_question_score.encode('utf-8'))

                for j in range (5, 0, -1):
                    self.status.config(text='Please wait '+ str(j)+ ' seconds for next question ...')
                    self.window.update()
                    time.sleep(1)

                # open cui on server player
                self.handler_question_score(i, rounds[i].question, rounds[i].a, rounds[i].b, rounds[i].c, rounds[i].d, self.server_score)
                
                self.server_wait = True

                threading.Thread(target=self.server_wait_time, args=(i,)).start()
        
        # end game to client
        final_score = [self.server_score, self.client_score]
        str_final_score = "_".join(str(x) for x in final_score)
        self.csocket.send(str_final_score.encode('utf-8'))

        if (self.client_score > self.server_score):
            self.title['text'] = 'CONGRATS YOU WIN!'
        elif (self.client_score < self.server_score):
            self.title['text'] = 'YOU LOSE!'
        else:
            self.title['text'] = 'TIED GAME!'

        self.question['text'] = 'your score : ' + str(self.server_score) + ' . other player score : ' + str(self.client_score)

        self.answer_a['text'] = ''
        self.answer_b['text'] = ''
        self.answer_c['text'] = ''
        self.answer_d['text'] = ''
        self.score['text'] = ''
        self.score_state['text'] = ''

        for i in range (10, 0, -1):
            self.status['text'] = 'The game will shutdown in ' + str(i) + ' seconds ...'
            self.window.update()
            time.sleep(1)

    def server_wait_time (self, question_number):
        check = True
        for i in range (10, 0, -1):
            self.status['text'] = 'You have ' + str(i) + ' seconds left to answer'
            if (self.server_wait == False):
                check = False
                break
            self.window.update()
            time.sleep(1)
        # kalau ga jawab dalam 10 detik:
        if (check):
            self.answer = -100

        if (self.evaluate_answer(question_number, self.answer)):
                self.server_score += 100
                self.score_state['text'] = 'Your Answer is Correct!'
                self.score['text'] = 'SCORE : ' + str(self.server_score)
        else:
                self.score_state['text'] = 'Your Answer is Wrong!'
                self.score['text'] = 'SCORE : ' + str(self.server_score)

    def handler_question_score (self, question_number, question, answer_a, answer_b, answer_c, answer_d, current_score):
        self.title['text'] = 'Question ' + str(question_number + 1)
        self.question['text'] = question
        self.answer_a['text'] = answer_a
        self.answer_b['text'] = answer_b
        self.answer_c['text'] = answer_c
        self.answer_d['text'] = answer_d

        self.score_state['text'] = ''
        self.score['text'] = ''

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
    server.listen(1)
    print("socket is listening, waiting for client request..")

    #TCP = keep connections until client wants to exit
    #establish connection with client
    clientSocket, clientAddress = server.accept()

    #start new thread to do operations & logic for each client
    newThread = ClientThread(clientAddress, clientSocket)
    newThread.start()
    window.mainloop()


if __name__ == '__main__':
    main()
    