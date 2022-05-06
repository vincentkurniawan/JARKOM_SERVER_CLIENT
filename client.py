# Nadia Clarissa Hermawan / 6181901013

# The steps to make this client-server gui calculator :
# 1) make the base client-server multi-threading TCP program beforehand (check the CUI folder)
# 2) check if number 1 is working properly
# 3) continue on importing tkinter, and setup the GUI window (focus on setupGUI(), etc method)
# 4) p.s A = 5, B = 10

import socket
import tkinter as tk
from tkinter import ANCHOR, CENTER, font
from functools import partial

#GUI font size collection
LARGE_FONT_STYLE = ("Helvetica", 15, "bold")
SMALL_FONT_STYLE = ("Arial", 13)

#GUI colors collection
LIGHT_GRAY = "#F5F5F5"
DARK_GRAY = "#404040"

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
        self.question_answer_recv()
        

    #setup the gui window
    def setupGUI(self):
        self.window = tk.Tk()
        self.window.geometry("500x250")
        self.window.resizable(0,0)
        self.window.title("Calculator GUI")

        #create the empty frame 
        self.display_frame, self.button_frame, self.result_frame = self.create_display_frame()

        #empty frame filling
        self.title, self.question, self.answer_a, self.answer_b, self.answer_c, self.answer_d, self.score_state, self.score = self.create_display_labels()
        # self.total_label, self.expression_input, self.get_text_button = self.create_display_labels()
        

    #create top part frame for displaying the typed math opr & button
    def create_display_frame(self):
        #contains title & input box
        frame = tk.Frame(self.window, bg=DARK_GRAY, pady=20)
        frame.pack(expand=False, fill="both")

        #contains submit button
        button_frame = tk.Frame(self.window, bg=DARK_GRAY)
        button_frame.pack(expand=False, fill="both")

        #contains result
        result_frame = tk.Frame(self.window, bg=DARK_GRAY, pady=5)
        result_frame.pack(expand=False, fill="both")

        return frame, button_frame, result_frame


    #assigning text to the text-view in display frame
    def create_display_labels(self):

        # title
        title = tk.Label(self.display_frame, anchor=CENTER, text="Question ", font=LARGE_FONT_STYLE, bg=DARK_GRAY, fg=LIGHT_GRAY)
        title.pack(expand=False, fill=None)

        # the question
        question = tk.Label(self.display_frame, anchor=CENTER, text="????", font=LARGE_FONT_STYLE, bg=DARK_GRAY, fg=LIGHT_GRAY)
        question.pack(expand=False, fill=None)

        # the answer A
        answer_a = tk.Button(self.button_frame, text="A????", font=SMALL_FONT_STYLE, command=partial(self.handler_answer_send, ANSWER_A))
        answer_a.grid(row=0, column=0, padx=0, pady=0)

        # the answer B
        answer_b = tk.Button(self.button_frame, text="A????", font=SMALL_FONT_STYLE, command=partial(self.handler_answer_send, ANSWER_B))
        answer_b.grid(row=1, column=0, padx=0, pady=0)

        # the answer C
        answer_c = tk.Button(self.button_frame, text="A????", font=SMALL_FONT_STYLE, command=partial(self.handler_answer_send, ANSWER_C))
        answer_c.grid(row=2, column=0, padx=0, pady=0)

        # the answer D
        answer_d = tk.Button(self.button_frame, text="A????", font=SMALL_FONT_STYLE, command=partial(self.handler_answer_send, ANSWER_D))
        answer_d.grid(row=3, column=0, padx=0, pady=0)

        # score state
        score_state = tk.Label(self.result_frame, anchor=CENTER, text="Your answer is ???", font=LARGE_FONT_STYLE, bg=DARK_GRAY, fg=LIGHT_GRAY)
        score_state.pack(expand=False, fill=None)

        # current score
        score = tk.Label(self.result_frame, anchor=CENTER, text="CURRENT SCORE = ", font=LARGE_FONT_STYLE, bg=DARK_GRAY, fg=LIGHT_GRAY)
        score.pack(expand=False, fill=None)

        return title, question, answer_a, answer_b, answer_c, answer_d, score_state, score


    def question_answer_recv (self):
        data0 = self.client.recv(1024)
        data0 = data0.decode('utf-8')
        data = list(data0.split("_"))
        self.handler_question_score(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])


    def handler_answer_send (self, answer):
        msg = str(answer)
        print("client's answer", msg)
        self.client.send(msg.encode('utf-8'))


    #Update GUI text view
    def handler_question_score (self, question_number, question, answer_a, answer_b, answer_c, answer_d, current_score, state_score):
        # set question 
        self.title.config(text = self.title.cget("text") + question_number)
        self.question.config(text = question)
        self.answer_a.config(text = answer_a)
        self.answer_b.config(text = answer_b)
        self.answer_c.config(text = answer_c)
        self.answer_d.config(text = answer_d)

        # set current score
        self.score.config(text = "CURRENT SCORE = " + current_score)

        # set score state
        if (state_score == SCORE_STATE_TRUE):
            self.score_state.config(text = "Your answer is CORRECT!")
        elif (state_score == SCORE_STATE_FALSE):
            self.score_state.config(text = "Your answer is WRONG!")

    #start the GUI window 
    def run(self):
        self.window.mainloop()


#run these code below once the py launched
if __name__ == '__main__':
    gui = Main()
    gui.run()

    
        



