from tkinter import *
from .Agent import *
from .Customer import *

class Shopper:
    
    def __init__(self, master, conn, cursor):
        self.__conn = conn
        self.__cursor = cursor
        self.__root = master
        self.__Agent = Agent(master, conn, cursor)
        self.__Customer = Customer(master, conn, cursor)
        
        #Login frame and it's required Widgets
        self.__Login_frame = Frame(self.__root, height=720, width=960)
        self.__agent_button = Button(self.__Login_frame, text="Login as Agent", command=self.Login_as_Agent) #Command?
        self.__customer_button = Button(self.__Login_frame, text="Login as Customer", command=self.Login_as_Customer) #Command?
        
        #Run the loop of the GUI: Starting with login page
        self.Login_Choose()
        self.__root.mainloop()
    
    def Login_Choose(self):
        self.__Login_frame.grid(padx=10, pady=10)
        self.__agent_button.grid(row=1, column=1, padx=50, pady=10)
        self.__customer_button.grid(row=1, column=3, padx=50, pady=10)
        
    def Login_as_Agent(self):
        #~ print("Agent_Button")
        self.__Login_frame.grid_forget()
        self.__Agent.Login_as_Agent_page()

    def Login_as_Customer(self):
        #~ print("Customer_Button")
        self.__Login_frame.grid_forget()
        self.__Customer.Login_as_Customer_page()
        
        
