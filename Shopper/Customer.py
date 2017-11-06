from tkinter import *

class Customer:
    def __init__(self, master, conn, cursor):
        self.__conn = conn
        self.__cursor = cursor
        self.__root = master
        
        #Customer's login page frame
        self.__Customer_Login_frame = Frame(self.__root, height=720, width=960)
        self.__Customer_Username = Label(self.__Customer_Login_frame, text="Username")
        self.__Customer_Password = Label(self.__Customer_Login_frame, text="Password")
        self.__Customer_Username_entry = Entry(self.__Customer_Login_frame)
        self.__Customer_Password_entry = Entry(self.__Customer_Login_frame, show="*")
        self.__Customer_Login_button = Button(self.__Customer_Login_frame, text="Sign in", command=self.Customer_Sign_in_button)
        self.__Customer_Register_button = Button(self.__Customer_Login_frame, text="Register", command=self.Customer_Register_button)
        self.__Customer_Check_Register_button = Button(self.__Customer_Login_frame, text="Check if valid and sign up", 
                                                                            command=self.Customer_Check_Register_button)
    def Login_as_Customer_page(self):
        #~ print("Customer_Button")
        self.__Customer_Login_frame.grid(padx=10, pady=10)
        
        self.__Customer_Username.grid(row=1, column=1, padx=10, pady=10, sticky=E)
        self.__Customer_Username_entry.grid(row=1, column=2, padx=10, pady=10)
        
        self.__Customer_Password.grid(row=2, column=1, padx=10, pady=10, sticky=E)
        self.__Customer_Password_entry.grid(row=2, column=2, padx=10, pady=10)
        
        self.__Customer_Login_button.grid(row=3, column=1, padx=10, pady=10, sticky=E)
        self.__Customer_Register_button.grid(row=3, column=2, padx=10, pady=10, sticky=E)
        
    def Customer_Sign_in_button(self):
        #~ print("Trying to sign in...")
        #Put database lookup code here, as well as encryption
        #self.__Customer_Password_entry.get()
        self.__Customer_Username_entry.delete(0, 'end')
        self.__Customer_Password_entry.delete(0, 'end')
        self.__Customer_Login_frame.grid_forget()
        #IMPORTANT!!! REMOVE THIS WHEN DONE!!!
        # V V V V V V V V V
        self.Login_Choose()
        
    def Customer_Register_button(self):
        #~ print("Time to register!!!")
        #Remakes the customer login page so that they can try to register
        self.__Customer_Login_button.grid_forget()
        self.__Customer_Register_button.grid_forget()
        self.__Customer_Password_entry.delete(0, 'end')
        self.__Customer_Check_Register_button.grid(row=3, column=1, columnspan=2, padx=10, pady=10)
    
    def Customer_Check_Register_button(self):
        #~ print("Checking if that name is available")
        #Check database for alrady existing CID
        #Use self.__Customer_Username_entry.get()
        #AND self.__Customer_Password_entry.get()
        #If valid, encrypt the password and add/assiciate with CID
        #If Valid, move to customer page
        self.__Customer_Password_entry.delete(0, 'end')
        #If not valid, have them try again, print relevant error message
        self.__Customer_Check_Register_button.grid_forget()
        self.__Customer_Login_frame.grid_forget()
        #Replace VVV with customer work page 
        self.Login_Choose()

        
