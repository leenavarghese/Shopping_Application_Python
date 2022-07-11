"""
Author       :   Leena
Date         :   December 14, 2021
This is a shopping application that allows customers to search products, add new items, display the products, and order
products. The application is integrated with a database in MySQL with a schema of 6 tables. Create account option registers
customers using customers’ first name, last name, user name, password and unique identifier. Email ID is used as unique
identifier. Every email address is unique so customer information is added to the system using unique identifier which is
Email ID. Before a customer is registered, system checks to see if this customer is not already registered in the system.
An already existing user  can login using his email id and password. Once the customer successfully logs in(for existing user)
or create a new account(for new users), he is presented with the welcome page. For an existing user who has made orders in
the past, he can know the details of his order by choosing the search order option. If the order id exists, the details of
the order are displayed. A scroll bar is provided so as to easily navigate is case of multiple entries. Next, the user can
choose between 4 departments- Electronics, Toys, Clothing and Baby products. This gives the customer an option to choose
a product from the drop-down menu which lists the products available in that category and the customer can chose the quantity
of items. When Checkout button is selected the screen with options to enter his address is displayed and thus he can successfully
place the order.
"""
from tkinter import *
from tkinter import messagebox
import mysql.connector
from datetime import date

#Establishing mysql connection
mydb = mysql.connector.connect(host='localhost', user='root', password='leena8034')
print(mydb)
my_cursor = mydb.cursor()
my_cursor.execute("USE project")
#Creating the main window
login_window=Tk()
login_window.geometry('300x200+300+300')
login_window.title("Welcome !!!")
#Declaring global variables
login_email=StringVar()
login_password=StringVar()
create_newUser_first_name=StringVar()
create_newUser_last_name=StringVar()
create_newUser_user_name=StringVar()
create_newUser_password=StringVar()
create_newUser_emailid=StringVar()
search_order_orderID=IntVar()
checkout_first_name=StringVar()
checkout_last_name=StringVar()
checkout_line1=StringVar()
checkout_line2=StringVar()
checkout_state=StringVar()
checkout_zipcode=StringVar()
selected_quantity=StringVar()
selected_product=StringVar()
global c_ID
global totPrice
#This function checks the credentials entered by the user has a matching entry in the customers_pr table
def checkCredentialinDB():
    print("Inside checkCredentialinDB function")
    sql = "SELECT email_address, password from customers_pr"
    my_cursor.execute(sql)
    registeredCustomers = my_cursor.fetchall()
    print("registeredCustomers: {}".format(registeredCustomers))
    email_ID = login_email.get()
    print(email_ID)
    password = login_password.get()
    correctCredentials = False

    for result in registeredCustomers:
        if result[0] == email_ID and result[1] == password:
            correctCredentials = True
    if correctCredentials == False:
        messagebox.showinfo("Wrong Credentials", "The credentials entered are not correct...")
    else:
        my_cursor.execute('SELECT customer_id FROM customers_pr WHERE email_address = %s', (email_ID,) )
        cust_id = my_cursor.fetchone()
        print("cust_id : {}".format(cust_id[0]))
        global c_ID
        c_ID = cust_id[0]
        print("c_ID : {}" .format(c_ID))
        login_email.set("")
        login_password.set("")
        openMainPage()

#This function is to perform the search corresponding to the order_id entered by the user. It also displays the order details
#if the order exists
def mainSearchOrder():
    print("Inside mainSearchOrder function")
    search_order_window = Toplevel()
    search_order_window.geometry("300x200+300+300")
    search_order_window.title("Search Order")
    search_order_orderID.set("")
    def cancelOperation():
        print("Inside cancelOperation function")
        search_order_window.destroy()
        search_order_window.update()
    def searchOrder():
        print("inside searchOrder function")
        orderFound = False
        sql = "SELECT order_id, order_price, tax_amount, customer_id from orders_pr"
        my_cursor.execute(sql)
        order_table_data = my_cursor.fetchall()
        print("order_table_data : {}".format(order_table_data))
       
        for result in order_table_data:
            order_ID = search_order_orderID.get()
            print(result)
            print("Order Id {}".format(result[0]))
            print("Order Price {}".format(result[1]))
            print("Tax Amount {}".format(result[2]))
            print("Customer Id {}".format(result[3]))
            if result[0] == order_ID:
                orderFound =True
                print(orderFound)
                cancelOperation()
                display_search_result_window = Toplevel()
                display_search_result_window.geometry("650x300+400+500")
                display_search_result_window.title("Order information")
                v_scroll = Scrollbar(display_search_result_window, orient="vertical")
                v_scroll.pack(side=RIGHT, fill=Y)
                text_data_display = Text(display_search_result_window, padx=5, pady=5, spacing1=1, spacing3=1)
                text_data_display["yscrollcommand"] = v_scroll
                v_scroll.config(command=text_data_display.yview)
                text_data_display.pack()
                display = ""
                display += "%25s%25s%25s\n" % ("Order ID", "Order Price", "Tax Amount")
                display += "%25s%25s%25s" % (result[0],result[1],result[2])
                text_data_display.insert(END, display)
                search_order_orderID.set("")
                search_order_window.destroy()
                search_order_window.update()
                break
        if orderFound == False:
                messagebox.showinfo("Order ID not found", "No records matching the orderID ...")
                search_order_orderID.set("")
                search_order_window.destroy()
                search_order_window.update()

    search_order_label1 = Label(search_order_window, text="Order ID", font=('ariel', 10)).grid(row=0, column=0, ipadx=5, ipady=2,pady=5,padx=5)
    search_order_text1 = Entry(search_order_window, textvariable=search_order_orderID).grid(row=0,column=1,ipadx=10,ipady=2)
    Search_order_button = Button(search_order_window, text="Search", bg="light blue", fg="black",
                                 font=('ariel', 12), command=searchOrder).grid(row=1,column=0, padx=20, pady=30)
    Place_order_button = Button(search_order_window, text="Cancel", fg="black",
                                font=('ariel', 12), command=cancelOperation).grid(row=1,column=1, padx=10, pady=10)

#adding the items to cart
def addCategory():
    print("Inside addCategory function")
    print(selected_quantity.get() +" " + selected_product.get())
    messagebox.showinfo("Item added", "Item successfully added to cart!!!")

#After checkout, this function displays the order details
def displayOrder():
    print("Inside displayOrder function")
    display_order_window = Toplevel()
    display_order_window.geometry("650x300+400+500")
    display_order_window.title("Order information")

    v_scroll = Scrollbar(display_order_window, orient="vertical")
    v_scroll.pack(side=RIGHT, fill=Y)
    text_data_display = Text(display_order_window, padx=5, pady=5, spacing1=1, spacing3=1)
    text_data_display["yscrollcommand"] = v_scroll
    v_scroll.config(command=text_data_display.yview)
    text_data_display.pack()
    display = ""
    display += "%20s%20s%10s%10s\n" % ("Product Name", "Quantity", "Price")
    '''
    display += "%20s%20s%10s%10s" % ()
    '''
    text_data_display.insert(END, display)

def checkout_category():
    print("Inside checkout_category function")

    def placeOrder():
        global c_ID
        global totPrice
        print("Inside placeOrder function")
        order_date = date.today()
        print("order_date : {} ".format(order_date))
        print("c_ID : {}".format(c_ID))
        #tax_amount = totPrice * 0.05

        sql4 = "INSERT INTO addresses_pr (line1, line2, state, zip_code, customer_id) values (%s, %s, %s, %s, %s)"
        data4 = (checkout_line1.get(), checkout_line2.get(), checkout_state.get(), checkout_zipcode.get(), c_ID)
        my_cursor.execute(sql4, data4)
        mydb.commit()

        displayOrder()
        #to change
        str1 = 1200
        m1 = "Order successfully placed. Your order id is {0}".format(str1)
        messagebox.showinfo("Order Placed", m1)

    def cancelOrder():
        print("Inside cancelOrder function")
        checkout_window.destroy()
        checkout_window.update()
    checkout_window = Toplevel()
    checkout_window.geometry("300x250+300+300")
    checkout_window.title("Checkout")
    checkout_label1 = Label(checkout_window, text="First Name", font=('ariel', 10)). \
        grid(row=0, column=0, ipadx=5, ipady=2, pady=5)
    checkout_text1 = Entry(checkout_window, textvariable=checkout_first_name). \
        grid(row=0, column=1, ipadx=5, ipady=2)
    checkout_label2 = Label(checkout_window, text="Last Name", font=('ariel', 10)). \
        grid(row=1, column=0, ipadx=5, ipady=2)
    checkout_text2 = Entry(checkout_window, textvariable=checkout_last_name). \
        grid(row=1, column=1, ipadx=5, ipady=2)
    checkout_label3 = Label(checkout_window, text="Line 1", font=('ariel', 10)). \
        grid(row=2, column=0, ipadx=5, ipady=2)
    checkout_text3 = Entry(checkout_window, textvariable=checkout_line1). \
        grid(row=2, column=1, ipadx=5, ipady=2)
    checkout_label4 = Label(checkout_window, text="Line 2", font=('ariel', 10)). \
        grid(row=3, column=0, ipadx=5, ipady=2)
    checkout_text4 = Entry(checkout_window, textvariable=checkout_line2). \
        grid(row=3, column=1, ipadx=5, ipady=2)
    checkout_label5 = Label(checkout_window, text="State", font=('ariel', 10)). \
        grid(row=4, column=0, ipadx=5, ipady=2)
    checkout_text5 = Entry(checkout_window, textvariable=checkout_state). \
        grid(row=4, column=1, ipadx=5, ipady=2)
    checkout_label6 = Label(checkout_window, text="Zip Code", font=('ariel', 10)). \
        grid(row=5, column=0, ipadx=5, ipady=2)
    checkout_text6 = Entry(checkout_window, textvariable=checkout_zipcode). \
        grid(row=5, column=1, ipadx=5, ipady=2)
    place_order_button = Button(checkout_window, text="Place Order", bg="light blue", fg="black", font=('ariel', 12),
                                command=placeOrder). \
        grid(row=6, column=0, padx=10, pady=20)
    cancel_button = Button(checkout_window, text="Cancel Order", fg="black", font=('ariel', 12), command=cancelOrder). \
        grid(row=6, column=1)
    checkout_window.mainloop()

def displayElectronicsCategory():
    product_information = {}
    def cancelCategory():
        win.destroy()
        win.update()
    print("Inside displayElectronicsCategory function")
    win = Toplevel()
    win.geometry("300x200+300+300")
    win.title("Electronics")
    label = Label(win, text="Select your product below:", font=('ariel', 10))
    sql = "SELECT product_id, product_name, price from products_pr where department_id = 1"
    my_cursor.execute(sql)
    OptionList = my_cursor.fetchall()
    print("OptionList: {}".format(OptionList))
    for result in OptionList:
        product_information["product_id"] = result[0]
        product_information["product_name"] = result[1]
        product_information["price"] = result[2]
        print("product_information : {}".format(product_information))

    # Access the Menu Widget using StringVar function
    selected_product.set(OptionList[0])
    # Create an instance of Menu in the frame
    main_menu = OptionMenu(win, selected_product, *OptionList)
    label.pack()
    main_menu.pack(pady=10)

    quantity_lbl = Label(
        win,
        text='Quantity',
        font=('ariel', 10)
    )
    quantity_lbl.pack()
    selected_quantity.set("")
    quantity_tf = Entry(win, textvariable=selected_quantity)
    quantity_tf.pack()
    add_button = Button(win, text="Add Item", bg="light blue", fg="black", font=('ariel', 12),
                        command=addCategory).pack(side =RIGHT, padx =5, pady =5)
    checkout_button = Button(win, text="Checkout", fg="black", font=('ariel', 12),
                             command=checkout_category).pack(side =RIGHT)

    cancel_button = Button(win, text="Cancel Order", fg="black", font=('ariel', 12), command=cancelCategory).pack(side =RIGHT)
    win.mainloop()

def displayClothingCategory():
    def cancelCategory():
        winClothing.destroy()
        winClothing.update()
    print("Inside displayClothingCategory function")
    winClothing = Toplevel()
    winClothing.geometry("300x200+300+300")
    winClothing.title("Clothing")
    label = Label(winClothing, text="Select your product below:", font=('ariel', 10))
    '''
    OptionList = [
        "Shirts", "Bottoms", "Jeans", "Scarfs", "Caps", "Jackets"
    ]
    '''
    sql = "SELECT product_name from products_pr where department_id =2"
    my_cursor.execute(sql)
    OptionList = my_cursor.fetchall()
    # Access the Menu Widget using StringVar function
    selected_product.set(OptionList[0])
    # Create an instance of Menu in the frame
    main_menu = OptionMenu(winClothing, selected_product, *OptionList)
    label.pack()
    main_menu.pack(pady=10)

    quantity_lbl = Label(
        winClothing,
        text='Quantity',
        font=('ariel', 10)
    )
    quantity_lbl.pack()
    selected_quantity.set("")
    quantity_tf = Entry(winClothing, textvariable=selected_quantity)
    quantity_tf.pack()
    add_button = Button(winClothing, text="Add Item", bg="light blue", fg="black", font=('ariel', 12),
                        command=addCategory).pack(side=RIGHT, padx=5, pady=5)
    checkout_button = Button(winClothing, text="Checkout", fg="black", font=('ariel', 12),
                             command=checkout_category).pack(side=RIGHT)

    cancel_button = Button(winClothing, text="Cancel Order", fg="black", font=('ariel', 12), command=cancelCategory).pack(side=RIGHT)
    winClothing.mainloop()

def displayToysCategory():
    def cancelCategory():
        winToys.destroy()
        winToys.update()
    print("Inside displayToysCategory function")
    print("Inside displayClothingCategory function")
    winToys = Toplevel()
    winToys.geometry("300x200+300+300")
    winToys.title("Toys")
    label = Label(winToys, text="Select your product below:", font=('ariel', 10))

    '''
    OptionList = [
        "Cars", "Animals", "Dolls", "Electronic Toys", "Educational Toys", "Action figures"
    ]
    '''
    sql = "SELECT product_name from products_pr where department_id = 3"
    my_cursor.execute(sql)
    OptionList = my_cursor.fetchall()
    # Access the Menu Widget using StringVar function
    selected_product.set(OptionList[0])
    # Create an instance of Menu in the frame
    main_menu = OptionMenu(winToys, selected_product, *OptionList)
    label.pack()
    main_menu.pack(pady=10)

    quantity_lbl = Label(
        winToys,
        text='Quantity',
        font=('ariel', 10)
    )
    quantity_lbl.pack()
    selected_quantity.set("")
    quantity_tf = Entry(winToys, textvariable=selected_quantity)
    quantity_tf.pack()
     add_button = Button(winToys, text="Add Item", bg="light blue", fg="black", font=('ariel', 12),
                        command=addCategory).pack(side=RIGHT, padx=5, pady=5)
    checkout_button = Button(winToys, text="Checkout", fg="black", font=('ariel', 12),
                             command=checkout_category).pack(side=RIGHT)

    cancel_button = Button(winToys, text="Cancel Order", fg="black", font=('ariel', 12),
                           command=cancelCategory).pack(side=RIGHT)
    winToys.mainloop()


def displayBabyCategory():
    def cancelCategory():
        winBaby.destroy()
        winBaby.update()
    print("Inside displayBabyCategory function")
    print("Inside displayClothingCategory function")
    winBaby = Toplevel()
    winBaby.geometry("300x200+300+300")
    winBaby.title("Kids Section")
    label = Label(winBaby, text="Select your product below:", font=('ariel', 10))
    '''
    OptionList = [
        "Rompers", "Socks", "Footwear", "Toys"
    ]
    '''
    sql = "SELECT product_name from products_pr where department_id =4"
    my_cursor.execute(sql)
    OptionList = my_cursor.fetchall()
    # Access the Menu Widget using StringVar function
    selected_product.set(OptionList[0])
    # Create an instance of Menu in the frame
    main_menu = OptionMenu(winBaby, selected_product, *OptionList)
    label.pack()
    main_menu.pack(pady=10)

    quantity_lbl = Label(
        winBaby,
        text='Quantity',
        font=('ariel', 10)
    )
    quantity_lbl.pack()
    selected_quantity.set("")
    quantity_tf = Entry(winBaby, textvariable=selected_quantity)
    quantity_tf.pack()
    add_button = Button(winBaby, text="Add Item", bg="light blue", fg="black", font=('ariel', 12),
                        command=addCategory).pack(side=RIGHT, padx=5, pady=5)
    checkout_button = Button(winBaby, text="Checkout", fg="black", font=('ariel', 12),
                             command=checkout_category).pack(side=RIGHT)

    cancel_button = Button(winBaby, text="Cancel Order", fg="black", font=('ariel', 12),
                           command=cancelCategory).pack(side=RIGHT)
    winBaby.mainloop()

def placeOrder_Start_Shopping():
    print("Inside placeOrder_Start_Shopping function")
    category_place_order_window = Toplevel()
    category_place_order_window.geometry("300x200+300+300")
    category_place_order_window.title("Categories")
    Electonics_button = Button(category_place_order_window, text="Electronics", fg="black", font=('ariel', 12),command=displayElectronicsCategory). \
        grid(row=0, column=0, ipadx=10, ipady=10, padx=40, pady=10)
    Toys_button = Button(category_place_order_window, text="Toys",bg="light blue", fg="black", font=('ariel', 12),command=displayToysCategory). \
        grid(row=0, column=1, ipadx=10, ipady=10, padx=10, pady=10)
    Clothing_button = Button(category_place_order_window, text="Clothing",bg="light blue", fg="black", font=('ariel', 12),command=displayClothingCategory).\
        grid(row=1, column=0, ipadx=10, ipady=10, padx=10, pady=30)
    Baby_button = Button(category_place_order_window, text="Baby", fg="black", font=('ariel', 12),command=displayBabyCategory).\
        grid(row=1, column=1, ipadx=10, ipady=10, padx=10, pady=10)

def openMainPage():
    main_page_window = Toplevel()
    main_page_window.geometry("300x200+300+300")
    main_page_window.title("Main Page")
    Place_order_start_shopping_button = Button(main_page_window, text="Start Shopping", bg="light blue", fg="black", font=('ariel', 12),
                                command=placeOrder_Start_Shopping). \
        grid(row=1, column=1, ipadx=50, ipady=10, padx=50, pady=10)
    Search_order_button = Button(main_page_window, text="Search Order", fg="black", font=('ariel', 12),
                                 command=mainSearchOrder). \
        grid(row=0, column=1, ipadx=50, ipady=10, padx=50, pady=30)

def createNewAccount():
    print("Inside createNewAccount function")
    def saveToDB():
        print("Inside saveToDB function")
        if create_newUser_first_name.get() == '' or create_newUser_last_name.get() == '' or create_newUser_user_name.get() == '' \
                or create_newUser_password.get() == '' or create_newUser_emailid.get() == '' :
            messagebox.showinfo('Fill in all fields','One or more fields are not filled ...')
        else:
            emailidAlreadyReg = False
            sql = "SELECT email_address from customers_pr"
            my_cursor.execute(sql)
            customers_emailids = my_cursor.fetchall()
            print("customers_emailids: {}" .format(customers_emailids))
            email = create_newUser_emailid.get()
            print(type(email))
            for result in customers_emailids:
                print("Email ID {}".format(result))
                if result[0] == email:
                    messagebox.showinfo('Email ID already registered','This Email ID is already registered with the application...')
                    emailidAlreadyReg = True
                    break
            if emailidAlreadyReg == False:
                firstname = create_newUser_first_name.get()
                lastname = create_newUser_last_name.get()
                username = create_newUser_user_name.get()
                password = create_newUser_password.get()

                sql = "INSERT INTO customers_pr (first_name, last_name, user_name, password, email_address) values (%s, %s, %s, %s, %s)"
                data = (firstname, lastname, username, password, email)
                my_cursor.execute(sql, data)
                mydb.commit()
                print(emailidAlreadyReg)
                messagebox.showinfo('Saved to DataBase', 'Entries are successfully saved in Database...')
                create_new_account_window.destroy()
                create_new_account_window.update()
                openMainPage()
            create_newUser_first_name.set("")
            create_newUser_last_name.set("")
            create_newUser_user_name.set("")
            create_newUser_emailid.set("")
            create_newUser_password.set("")
    create_new_account_window = Toplevel()
    create_new_account_window.geometry("300x200+300+300")
    create_new_account_window.title("Create new account")
    create_new_account_label1 = Label(create_new_account_window, text="First Name", font=('ariel', 10)).grid(row=0, column=0, ipadx=10, ipady =2)
    create_new_account_text1 = Entry(create_new_account_window, textvariable=create_newUser_first_name).grid(row=0, column=1, ipadx=10, ipady =2)
    create_new_account_label2 = Label(create_new_account_window, text="Last Name", font=('ariel', 10)).grid(row=1, column=0, ipadx=10, ipady =2)
    create_new_account_text2 = Entry(create_new_account_window, textvariable=create_newUser_last_name).grid(row=1, column=1, ipadx=10, ipady =2)
    create_new_account_label3 = Label(create_new_account_window, text="User Name", font=('ariel', 10)).grid(row=2, column=0, ipadx=10, ipady =2)
    create_new_account_text3 = Entry(create_new_account_window, textvariable=create_newUser_user_name).grid(row=2, column=1, ipadx=10, ipady =2)
    create_new_account_label4 = Label(create_new_account_window, text="Password", font=('ariel', 10)).grid(row=3, column=0, ipadx=10, ipady =2)
    create_new_account_text4 = Entry(create_new_account_window, textvariable=create_newUser_password).grid(row=3, column=1, ipadx=10, ipady =2)
    create_new_account_label5 = Label(create_new_account_window, text="Email ID", font=('ariel', 10)).grid(row=4, column=0, ipadx=10, ipady =2)
    create_new_account_text5 = Entry(create_new_account_window, textvariable=create_newUser_emailid).grid(row=4, column=1, ipadx=10, ipady =2)
    Create_new_account_button = Button(create_new_account_window, text="Create Account", bg="light blue", fg="black", font=('ariel', 12),command=saveToDB).grid(row=5, column=1, columnspan=2, padx=10,pady=10)

    create_new_account_window.mainloop()

login_label1=Label(login_window, text="Email", font=('ariel', 10)).grid(row=0, column=0,padx=10, pady=10)
login_text1=Entry(login_window, textvariable=login_email).grid(row=0, column=1,padx=10, pady=10)
login_label2=Label(login_window, text="Password", font=('ariel', 10)).grid(row=1, column=0,padx=10, pady=10)
login_text2=Entry(login_window, textvariable=login_password).grid(row=1, column=1,padx=10, pady=10)

login_button=Button(login_window, text="User Login", fg="black", font=('ariel',12), command=checkCredentialinDB).grid(row=2,column=0, padx=10, pady=10)
newAccount_button=Button(login_window, text="New Account", bg="light blue", fg="black", font=('ariel',12), command=createNewAccount).grid(row=2,column=1, padx=10, pady=10)
login_window.mainloop()