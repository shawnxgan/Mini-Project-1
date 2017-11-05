import sqlite3 as lite
import sys
from Shopper.shopper import *
from Shopper.DB_Make import *
from tkinter import *

def DB_Try_connect(path):
    
    try:
        conn = lite.connect(path)
        cursor = conn.cursor()
        return conn, cursor
    except Error as e:
        print(e)
    return None,None

def main(argv):  #Main function, passed the name of the database
    if(len(sys.argv) > 1):  #Check for name existence
        path="./" + argv[1]
    else:
        path="./register.db"    #Default name
    #~ print(path)
    conn,cursor = DB_Try_connect(path)
    if conn is not None:
        loadSchema(conn, cursor, 'prj-tables.sql')
    else:
        print("A fatal Error was encountered\nClosing program...")
        exit

    #insert_data()
    conn.create_function("hash", 1 , encrypt)
    root = Tk()
    shop = Shopper(root, conn, cursor)
    #conn.commit()    <-  Necessary????  Might not want to commit after closing GUI
    conn.close()
    return

if __name__ == "__main__":  #main function, executed from command
	main(sys.argv) #Call main function, pass through any inputs from command line
