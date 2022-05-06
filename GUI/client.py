# Kelompok :
# Nadia Clarissa Hermawan / 6181901013
# Vincent Kurniawan / 6181901024

from functools import partial
import socket
import threading
import time
import tkinter as tk
from tkinter import WORD, font
from tkinter.font import BOLD, families

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
    #constructor
    def __init__(self):
        self.setupGUI()
        self.setupClient()
        self.handler_answer_send('init')


    #setup the client connection with the server
    def setupClient(self):
        #define the server's address & port on which you want to connect
        server_host = '127.0.0.1'
        server_port = 8080
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #connect to server on local computer
        self.client.connect((server_host, server_port))
        print("Hello! you are now connected to the server..") 


    #setup the gui window
    def setupGUI(self):
        self.window = tk.Tk()
        self.window.title('KAHUUT !! (CLIENT)')
        self.window.geometry("700x700")

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
        self.title = tk.Label(self.frame_title, text='', font = ('Courier New', 18), wraplength=600)
        self.title.pack()

        self.question = tk.Label(self.frame_title, text='', font = ('Courier New', 18), wraplength=600)
        self.question.pack()

        self.answer_a = tk.Button(self.frame_button, text='', font = ('Courier New', 18), bg='#9FB4FF', command=partial(self.handler_answer_send, ANSWER_A), wraplength=600)
        self.answer_a.pack()

        self.answer_b = tk.Button(self.frame_button, text='', font = ('Courier New', 18), bg='#9FB4FF', command=partial(self.handler_answer_send, ANSWER_B), wraplength=600)
        self.answer_b.pack()

        self.answer_c = tk.Button(self.frame_button, text='', font = ('Courier New', 18), bg='#9FB4FF', command=partial(self.handler_answer_send, ANSWER_C), wraplength=600)
        self.answer_c.pack()

        self.answer_d = tk.Button(self.frame_button, text='', font = ('Courier New', 18), bg='#9FB4FF', command=partial(self.handler_answer_send, ANSWER_D), wraplength=600)
        self.answer_d.pack()

        self.score_state = tk.Label(self.frame_result, text='', font = ('Courier New', 18), wraplength=600)
        self.score_state.pack()

        self.score = tk.Label(self.frame_result, text='', font = ('Courier New', 18), wraplength=600)
        self.score.pack()

        self.status = tk.Label(self.frame_result, text='', font = ('Courier New', 18), wraplength=600)
        self.status.pack()


    def handler_answer_send (self, answer):
        msg = str(answer)
        self.client.send(msg.encode('utf-8'))
        self.client_wait = False
        threading.Thread(target=self.question_answer_recv).start()


    def question_answer_recv (self):
        data0 = self.client.recv(1024)
        data0 = data0.decode('utf-8')
        data = list(data0.split("_"))
        if (len(data) > 2):
            self.handler_question_score(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])
        else:
            server_score = data[0]
            client_score = data[1]
            if (client_score > server_score):
                self.title['text'] = 'CONGRATS YOU WIN!'
            elif (client_score < server_score):
                self.title['text'] = 'YOU LOSE!'
            else:
                self.title['text'] = 'TIED GAME!'
            
            self.question['text'] = 'your score : ' + str(client_score) + '\nother player score : ' + str(server_score)
            
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
            self.window.destroy()
            exit()


    def handler_question_score (self, question_number, question, answer_a, answer_b, answer_c, answer_d, current_score, state_score):
        question_number = int(question_number) + 1
        question_number = str(question_number)

        self.question['text'] = ''
        self.title['text'] = ''
        self.answer_a['text'] = ''
        self.answer_b['text'] = ''
        self.answer_c['text'] = ''
        self.answer_d['text'] = ''

        if (int(state_score) == SCORE_STATE_TRUE):
            self.score_state.config(text='Your Answer is Correct!')
            self.score['text'] = 'SCORE : ' + current_score
        elif (int(state_score) == SCORE_STATE_FALSE):
            self.score_state.config(text='Your Answer is Wrong!')
            self.score['text'] = 'SCORE : ' + current_score

        for j in range (5, 0, -1):
            self.status.config(text='Please wait '+ str(j)+ ' seconds for next question ...')
            self.window.update()
            time.sleep(1)

        self.title.config(text='Question ' + question_number)
        self.question.config(text=question)
        self.answer_a.config(text=answer_a)
        self.answer_b.config(text=answer_b)
        self.answer_c.config(text=answer_c)
        self.answer_d.config(text=answer_d)
        self.score_state['text'] = ''
        self.score['text'] = ''
        
        self.client_wait = True
        self.exceed_time = False
        threading.Thread(target=self.client_wait_time).start()


    def client_wait_time (self):
        check = True
        for i in range (10, 0, -1):
            self.status['text'] = 'You have ' + str(i) + ' seconds left to answer'
            if (not self.client_wait):
                check = False
                break
            self.window.update()
            time.sleep(1)
        if (check):
            self.exceed_time = True
            self.score['text'] = 'Time is up!'
            self.handler_answer_send(-100)
        else:
            self.status['text'] = 'Waiting for other player ...'


    #start the GUI window 
    def run(self):
        self.window.mainloop()


#run these code below once the py launched
if __name__ == '__main__':
    gui = Main()
    gui.run()

    
        



