from tkinter import *

class Agent:
    def __init__(self, master, conn, cursor):
        self.__conn = conn
        self.__cursor = cursor
        self.__root = master

        #Agent's login page frame
        self.__Agent_Login_frame = Frame(self.__root, height=720, width=960)
        self.__Agent_Username = Label(self.__Agent_Login_frame, text="Username")
        self.__Agent_Password = Label(self.__Agent_Login_frame, text="Password")
        self.__Agent_Username_entry = Entry(self.__Agent_Login_frame)
        self.__Agent_Password_entry = Entry(self.__Agent_Login_frame, show="*")
        self.__Agent_Login_button = Button(self.__Agent_Login_frame, text="Sign in", command=self.Agent_Sign_in_button)
        
        #Agent's work select page frame
        self.__Agent_Work_frame = Frame(self.__root, height=720, width=960)
        self.__Agent_Setup_Delivery_button = Button(self.__Agent_Work_frame, text="Setup Delivery",
                                                                    command=self.Agent_Setup_Delivery)
        self.__Agent_Update_Delivery_button = Button(self.__Agent_Work_frame, text="Update Delivery", 
                                                                    command=self.Agent_Update_Delivery)
        self.__Agent_Add_Stock_button = Button(self.__Agent_Work_frame, text="Add Stock",
                                                                        command=self.Agent_Add_Stock)
        
        #Agent's Add Stock page frame
        self.__Agent_Add_Stock_frame = Frame(self.__root, height=720, width=960)
        self.__Agent_StoreID_label = Label(self.__Agent_Add_Stock_frame, text="Store ID")
        self.__Agent_StoreID_entry = Entry(self.__Agent_Add_Stock_frame)
        self.__Agent_ProcuctID_label = Label(self.__Agent_Add_Stock_frame, text="Procuct ID")
        self.__Agent_ProductID_entry = Entry(self.__Agent_Add_Stock_frame)
        self.__Agent_Add_Quantity_label = Label(self.__Agent_Add_Stock_frame, text="Quantity to add")
        self.__Agent_Add_Quantity_entry = Entry(self.__Agent_Add_Stock_frame)
        self.__Agent_Change_Price_check_var = IntVar()
        self.__Agent_Change_Price_check = Checkbutton(self.__Agent_Add_Stock_frame, text="Change price?", 
                            variable=self.__Agent_Change_Price_check_var , command=self.Agent_Change_Price)
        self.__Agent_Price_entry = Entry(self.__Agent_Add_Stock_frame)
        self.__Agent_Confirm_Update_button = Button(self.__Agent_Add_Stock_frame, text="Confirm Update", 
                                                                    command=self.Agent_Confirm_Update_button)
        self.__Agent_Add_Stock_label = Label(self.__Agent_Add_Stock_frame, text=" ")
        self.__Agent_Add_Stock_Back_button = Button(self.__Agent_Add_Stock_frame, text="Back", 
                                                                    command=self.Agent_Add_Stock_Back_button)
        
        #Agent's Set Delivery page frame
        self.__Agent_Set_Delivery_frame = Frame(self.__root, height=720, width=960)
        self.__Agent_Set_Delivery_scrollbar = Scrollbar(self.__Agent_Set_Delivery_frame , orient=VERTICAL)
        self.__Agent_Set_Delivery_listbox = Listbox(self.__Agent_Set_Delivery_frame, selectmode=EXTENDED, 
                                                    yscrollcommand=self.__Agent_Set_Delivery_scrollbar.set)
        self.__Agent_Set_Delivery_scrollbar.config(command=self.__Agent_Set_Delivery_listbox.yview)
        self.__Agent_Set_Delivery_button = Button(self.__Agent_Set_Delivery_frame, text="Set up Delivery Package",
                                                    command=self.Agent_Set_Delivery_button)
                                                    
        #Agent's Set Delivery Pickup Time frame
        self.__Agent_Set_Pickup_Time_frame = Frame(self.__root)
        self.__Agent_Set_Pickup_Time_scrollbar = Scrollbar(self.__Agent_Set_Pickup_Time_frame, orient=VERTICAL)
        self.__Agent_Set_Pickup_Time_listbox = Listbox(self.__Agent_Set_Pickup_Time_frame, selectmode=EXTENDED, 
                                                        yscrollcommand=self.__Agent_Set_Pickup_Time_scrollbar.set)
        self.__Agent_Set_Pickup_Time_scrollbar.config(command=self.__Agent_Set_Pickup_Time_listbox.yview)
        self.__Agent_Set_Pickup_Time_entry = Entry(self.__Agent_Set_Pickup_Time_frame)
        self.__Agent_Set_Pickup_Time_button = Button(self.__Agent_Set_Pickup_Time_frame, text="Set Pickup Time", 
                                                    command=self.Agent_Set_Pickup_Time_button)
        self.__Agent_Confirm_Pickup_Time_button = Button(self.__Agent_Set_Pickup_Time_frame, text="Confirm Delivery settings",
                                                    command=self.Agent_Confirm_Delivery_button)


    def Login_as_Agent_page(self):
        #~ print("Agent_Button")
        self.__Agent_Login_frame.grid(padx=10, pady=10)
        self.__Agent_Username.grid(row=1, column=1, padx=10, pady=10, sticky=E)
        self.__Agent_Password.grid(row=2, column=1, padx=10, pady=10, sticky=E)
        self.__Agent_Username_entry.grid(row=1, column=2, padx=10, pady=10)
        self.__Agent_Password_entry.grid(row=2, column=2, padx=10, pady=10)
        self.__Agent_Login_button.grid(row=3, column=1, columnspan=2, padx=10, pady=10)

    def Agent_Sign_in_button(self):
        #~ print("Trying to sign in...")
        #Put database lookup code here, as well as encryption
        #self.__Agent_Password_entry.get()
        #self.__Agent_Username_entry.get()
        #Check database for AID
        #If valid, compare PW against AID.PW in database
        #If valid, move to Agent_Work_page
        #If any are invalid, show relevant error message
        
        self.__Agent_Username_entry.delete(0,'end')
        self.__Agent_Password_entry.delete(0,'end')
        self.__Agent_Login_frame.grid_forget()
        self.Agent_Work_page()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
    def Agent_Work_page(self):
        self.__Agent_Work_frame.grid(padx=10, pady=10)
        self.__Agent_Setup_Delivery_button.grid(row=0, column=0, padx=50, pady=10)
        self.__Agent_Update_Delivery_button.grid(row=1, column=0, padx=50, pady=10)
        self.__Agent_Add_Stock_button.grid(row=2, column=0, padx=50, pady=10)
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    
    def Agent_Change_Price(self):
        if self.__Agent_Change_Price_check_var.get():
            self.__Agent_Price_entry.grid(row=1, column=3, padx=25, pady=10)
        else:
            self.__Agent_Price_entry.delete(0, 'end')
            self.__Agent_Price_entry.grid_forget()
    
    def Agent_Confirm_Update_button(self):
        #Add stock, and maybe adjust price
        self.__Agent_StoreID_entry.delete(0, 'end')
        self.__Agent_ProductID_entry.delete(0, 'end')
        self.__Agent_Add_Quantity_entry.delete(0, 'end')
        if self.__Agent_Change_Price_check_var.get(): #This 'if' should be used to either update the price, or not
            self.__Agent_Price_entry.delete(0, 'end')
            self.Agent_Stock_Update_Succeed()
            #here is the maybe-price-adjustment
        else:
            self.Agent_Stock_Update_Fail()
            
        #If the item cant be found (store/product dont exist)
        #then use Stock_Update_Fail
        #If it exists, use Stock_Update_Succeed
        
        
    def Agent_Stock_Update_Succeed(self):
        self.__Agent_Add_Stock_label.config(text="Stock added!")
        
    def Agent_Stock_Update_Fail(self):
        self.__Agent_Add_Stock_label.config(text="Error, stock not added")
        
    def Agent_Add_Stock_Back_button(self):
        self.__Agent_Add_Stock_label.config(text=" ")
        self.__Agent_Add_Stock_frame.grid_forget()
        self.Agent_Work_page()
        
    def Agent_Add_Stock(self):
        #~ print("todo1")
        self.__Agent_Work_frame.grid_forget()
        self.__Agent_Add_Stock_frame.grid(padx=10, pady=10)
        self.__Agent_StoreID_label.grid(row=0, column=0, padx=25, pady=10)
        self.__Agent_StoreID_entry.grid(row=1, column=0, padx=25, pady=10)
        self.__Agent_ProcuctID_label.grid(row=0, column=1, padx=25, pady=10)
        self.__Agent_ProductID_entry.grid(row=1, column=1, padx=25, pady=10)
        self.__Agent_Add_Quantity_label.grid(row=0, column=2, padx=25, pady=10)
        self.__Agent_Add_Quantity_entry.grid(row=1, column=2, padx=25, pady=10)
        self.__Agent_Change_Price_check.grid(row=0, column=3, padx=55, pady=10)
        self.__Agent_Confirm_Update_button.grid(row=2, column=1, columnspan=2, pady=10)
        self.__Agent_Add_Stock_label.grid(row=3, column=1, columnspan=2, pady=10)
        self.__Agent_Add_Stock_Back_button.grid(row=2, column=0, padx=10, pady=10)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def Agent_Update_Delivery(self):
        #~ print("todo2")
        self.__Agent_Work_frame.grid_forget()
        self.Login_Choose()
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def Agent_Setup_Delivery(self):
        #~ print("todo3")
        #Find ALL orders that are not in any delivery
        #Pull usefull data as strings, then fill the listbox below
        self.__Agent_Work_frame.grid_forget()
        self.__Agent_Set_Delivery_frame.grid(padx=10, pady=10)
        self.__Agent_Set_Delivery_listbox.grid(row=0, column=0, pady=10, sticky=N+S)
        self.__Agent_Set_Delivery_scrollbar.grid(row=0, column=1, pady=10, sticky=N+S)
        self.__Agent_Set_Delivery_button.grid(row=1, column=0, columnspan=2, pady=10)
        #~ for i in range(0, 200):
            #~ self.__Agent_Set_Delivery_listbox.insert(END, "TEST"+str(i))
            #Use the above comment to insert all orders in place of TEST, 
            # HAS to be a string (descriptive? or just OID)
        
    def Agent_Set_Delivery_button(self):
        delivery_selections = self.__Agent_Set_Delivery_listbox.curselection()
        #Delivery_selections is either a list of strings, or a list of int, use it to put
        #data into the listbox based on which orders are in 'THIS' delivery
        #Also need to generate Delivery ID
        self.__Agent_Set_Delivery_frame.grid_forget()
        self.__Agent_Set_Pickup_Time_frame.grid(padx=10, pady=10)
        self.__Agent_Set_Pickup_Time_listbox.grid(row=0, column=0, pady=10, sticky=N+S)
        self.__Agent_Set_Pickup_Time_scrollbar.grid(row=0, column=1, pady=10, sticky=N+S+W)
        self.__Agent_Set_Pickup_Time_entry.grid(row=1, column=0, pady=10)
        self.__Agent_Set_Pickup_Time_button.grid(row=1, column=1, pady=10)
        self.__Agent_Confirm_Pickup_Time_button.grid(row=2, column=0, columnspan=2, pady=10)
        
    def Agent_Set_Pickup_Time_button(self):
        Pickup_Time = self.__Agent_Set_Pickup_Time_entry.get()
        #Turn string into time, otherwise set to 0
        if (Pickup_Time):
            self.__Agent_Set_Pickup_Time_entry.delete(0, END)
            Order_pickup_time_selections = self.__Agent_Set_Pickup_Time_listbox.curselection()
            for i in reversed(Order_pickup_time_selections):
                self.__Agent_Set_Pickup_Time_listbox.delete(i)
                #Pull from the "Orders" list, update the pickup time, then remove it from the list
                #VERY important to use reversed ^^^ so as not to mess up the list order, 
                #we are accesing by index numer i and need them to be in the same order while removing
                #Other items
                
    def Agent_Confirm_Delivery_button(self):
            self.__Agent_Set_Pickup_Time_frame.grid_forget()
            #Set the rest of the list of OID pickup times to null
            
            self.Agent_Work_page()
