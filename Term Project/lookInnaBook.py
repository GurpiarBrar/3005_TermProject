import sqlite3
cart = []

# Key information for functionality of currently logged in users
userRole=''
userID= ''

#Menus for each type of user
user = ["{:<20} {:>5}".format('View Orders:',1),
        "{:<20} {:>5}".format('Search for a Book:',2),
        "{:<20} {:>5}".format('View a Book:',3),
        "{:<20} {:>5}".format('Add Book to cart:',4),
        "{:<20} {:>5}".format('Checkout:',5),]

admin = ["{:<20} {:>5}".format('View Orders:',1),
        "{:<20} {:>5}".format('Search for a Book:',2),
        "{:<20} {:>5}".format('View a Book:',3),
        "{:<20} {:>5}".format('Add Book to cart:',4),
        "{:<20} {:>5}".format('Checkout:',5),
        "{:<20} {:>5}".format('Add a Book:',6),
        "{:<20} {:>5}".format('Remove a Book:',7),
        "{:<20} {:>5}".format('View all Publishers:',8),
        "{:<20} {:>5}".format('View all reports:',9),]

bookColoumns = ["ISBN", "Title", "Author", "Genre","Sell Price","Publisher Sales Cut", "Copies Sold", "Stock", "Number of Pages", "Publisher"]

# Prints Books in a nice format
def prettyBook(row):
    if len(row)> 1:
        if(userRole == 'admin'):
            for i in range  (len(row)):
                print(bookColoumns[i]+": "+str(row[i]))
        
        else:
            for i in range (len(row)):
                if not (i == 5 or i ==6):
                    print(bookColoumns[i]+": "+str(row[i]))
    else:
        if(userRole == 'admin'):
            for i in range  (len(row[0])):
                print(bookColoumns[i]+": "+str(row[0][i]))
            
        else:
            for i in range  (len(row[0])):
                if not (i == 5 or i ==6):
                    print(bookColoumns[i]+": "+str(row[0][i]))

# Prints information in nice format
def prettyPrint(row):
    string =""
    for i in range  (len(row)):
        string+= cur.description[i][0]+": "+str(row[i])+" \n"
    print(string)

# View a specificed order by inputted orderID
def viewOrder():
    option = input("Enter Order Number to view book: ")
    if(option ==''):
        print("No input")
        return
    target = cur.execute("SELECT * FROM orders WHERE orderID = ?",(int(option),)).fetchall()
    target=target[0]
    if (target!=[]):
        print("\nYour Order:")
        print("Order ID: "+ str(target[0]))
        print("Shipping Info: "+ str(target[1]))
        print("Billing Info: "+ str(target[2]))
        print("Tracking Info: "+ str(target[3]))
        print("\n")
        rows = cur.execute("SELECT * FROM partOf WHERE orderID = ?",(int(option),)).fetchall()
        for row in rows: print("ISBN: "+str(row[1])+" Copies: "+str(row[2]))
        return
    print("No orders matching: "+option)

# View all publishers that have a book in the store
def viewPublishers():
    rows = cur.execute("SELECT * FROM publisher").fetchall()
    print("\nYour Publishers:")

    for row in rows:
        print(row)
      
# View a book based on ISBN
def viewBook():
    option = input("Enter ISBN to view book: ")
    if(option ==''):
        print("No input")
        return
    bisbn = cur.execute("SELECT * FROM book WHERE isbn = ?",(option,)).fetchall()
    if(bisbn !=[]):
        print("\n Book with ISBN matching: "+option)
        prettyBook(bisbn)
        return
        
    print("No books matching: "+option)

# admin only: View sales per genre
def viewReports():
    rows = cur.execute('''Select genre, sum(copiesSold) as copies, sum(copiesSold * sellPrice) as gross, sum((copiesSold * sellPrice)-copiesSold * sellPrice * (PublisherSalesCut)/100) as publisher
                            From book
                            Group By genre''').fetchall()
    print("\nGenre Reports:")
    for row in rows:
        print("Genre: "+ str(row[0]))
        print("Copies Sold: "+ str(row[1]))
        print("Gross: "+ str(row[2]))
        print("Net: "+ str(row[3]))
        print("\n")
    rows = cur.execute('''Select publisher, sum(copiesSold) as copies, sum(copiesSold * sellPrice) as gross, sum((copiesSold * sellPrice)-copiesSold * sellPrice * (PublisherSalesCut)/100) as pub
                            From book
                            Group By publisher''').fetchall()
    print("\nPublisher Reports:")
    for row in rows:
        print("Publisher: "+ str(row[0]))
        print("Copies Sold: "+ str(row[1]))
        print("Gross: "+ str(row[2]))
        print("Net: "+ str(row[3]))
        print("\n")

    rows = cur.execute('''Select author, sum(copiesSold) as copies, sum(copiesSold * sellPrice) as gross, sum((copiesSold * sellPrice)-copiesSold * sellPrice * (PublisherSalesCut)/100) as pub
                            From book
                            Group By author''').fetchall()
    print("\nAuthor Reports:")
    for row in rows:
        print("Author: "+ str(row[0]))
        print("Copies Sold: "+ str(row[1]))
        print("Gross: "+ str(row[2]))
        print("Net: "+ str(row[3]))
        print("\n")

# Search book based on isbn, title, author, genre, or publisher
def searchBook():
    print("Search by ISBN, Title, Author, Genre, or Publisher")
    option = input("Enter Search Term: ")
    if(option ==''):
        print("No input")
        return
    # if the input is a number, check if there is a matching isbn book
    if option.isnumeric():
        bisbn = cur.execute("SELECT ISBN, Title, Author, Genre FROM book WHERE isbn = ?",(option,)).fetchall()
        if(bisbn !=[]):
            print("\n Book with ISBN matching: "+option)
            prettyBook(bisbn)
            return
    else:
        # if the input is not a number, check if there is a matching book in any of the following
        btitle = cur.execute("SELECT ISBN, Title, Author, Genre FROM book WHERE title = ?",(option,)).fetchall()
        if(btitle !=[]):
            print("\n Books with Titles matching: "+option)
            for row in btitle:
                prettyBook(row)
                print("\n")
            return
        bauthor = cur.execute("SELECT ISBN, Title, Author, Genre FROM book WHERE author = ?",(option,)).fetchall()
        if(bauthor !=[]):
            print("\n Books with Authors matching: "+option)
            for row in bauthor:
                prettyBook(row)
                print("\n")
            return
        bgenre = cur.execute("SELECT ISBN, Title, Author, Genre FROM book WHERE genre = ?",(option,)).fetchall()
        if(bgenre !=[]):
            print("\n Books with Genre matching: "+option)
            for row in bgenre:
                prettyBook(row)
                print("\n")
            return
        bpub = cur.execute("SELECT ISBN, Title, Author, Genre FROM book WHERE publisher = ?",(option,)).fetchall()
        if(bpub !=[]):
            print("\n Books with publisher matching: "+option)
            for row in bpub:
                prettyBook(row)
                print("\n")
            return
    print("No Books matching search term")

# Add specificed book (isbn) to cart
def addToCart():
    global cart
    option = input("Enter ISBN to add book to cart: ")
    if((not option.isnumeric()) or option ==''):
        print("Invalid input")
        return

    # Check if isbn matches
    rows = cur.execute("SELECT * FROM book").fetchall()
    for row in rows:
        if (row[0]==int(option)):
            # Get quantity
            quantity = input("Enter quantity: ")
            if ((not quantity.isnumeric()) or int(quantity) <1):
                print("Please enter a valid quantity")
            else:
                # Add to cart
                print("Your Cart: \n")
                consolidateCart(row, quantity)
                print(cart)

            return
    print("No books matching: "+option)

# Adds book to store page
def addBook():
    # Book information
    isbn = input("Enter ISBN of new Book ")
    title = input("Enter Title of new Book ")
    author = input("Enter Author of new Book ")
    genre = input("Enter main Genre of new Book ")
    sell = input("Enter Sell Price of new Book ")
    cut = input("Enter publisher sale percent of new Book ")
    stock = input("Enter stock of new Book ")
    pages = input("Enter number of pages of new Book ")
    publisher = input("Enter name of publisher of new Book ")

    # Checks for null or incorrect values
    if(title =='' or author =='' or genre =='' or sell =='' or cut =='' or stock =='' or pages =='' or publisher ==''):
        print("There can be no null values")
        return
    if((not isbn.isnumeric()) or (not sell.isnumeric()) or(not cut.isnumeric()) or (not stock.isnumeric()) or(not pages.isnumeric())):
        print("ISBN, Sell price, Publisher sales percent, and Number of pages have to be numbers")
        return


    # If publisher exists enter book
    rows = cur.execute("SELECT * FROM publisher").fetchall()
    for row in rows:
        if(row[0]==publisher):
            print("Book Added")
            con.execute('''INSERT or IGNORE INTO book (isbn, title, author, genre, 
                sellPrice, PublisherSalesCut, copiesSold, 
                stock, NumberofPages, publisher) values (?, ?, ?, ?, ?,?,?,?,?,?)''',(isbn,title,author,genre,sell,cut,0,stock,pages,publisher ))
            con.commit() 
            return


    # Creat publisher and then insert book with new publisher 
    print("Creating new Publisher")
    name = input("Enter name of new publisher ")
    email = input("Enter email of new publisher ")
    address = input("Enter address of new publisher ")
    num = input("Enter phone number of new publisher ")
    binfo = input("Enter banking info of new publisher ")

    if(name =='' or email =='' or address =='' or num =='' or binfo ==''):
        print("There can be no null values")
        return

    con.execute("INSERT or IGNORE INTO publisher (name,email,address,phoneNum,bankingInfo) values (?, ?, ?, ?, ?)",
            (name,email,address,num,binfo))
    print("Publisher added")
    con.execute('''INSERT or IGNORE INTO book (isbn, title, author, genre, 
        sellPrice, PublisherSalesCut, copiesSold, 
        stock, NumberofPages, publisher) values (?, ?, ?, ?, ?,?,?,?,?,?)''',(isbn,title,author,genre,sell,cut,0,stock,pages,name ))
    print("Book Added")

    con.commit()   


# Remove Book from store page
def removeBook():

    isbn = input("Enter ISBN of new Book to be removed ")
    if((not isbn.isnumeric()) or isbn =="" or isbn == " " ):
        print("Enter a valid ISBN number")
        return

    # Find book with matching isbn
    cur.execute("DELETE FROM book where isbn = ?", (isbn,))
    if cur.rowcount<0:
        print("No books deleted")
    else:
        print(isbn," deleted")
    con.commit() 

# Checkout Books in cart   
def checkout():
    global cart,userID
    if(len(cart)==0):
        print("No items in Cart")
        return
    
    firstEntryCreateOrder = True
    for i in range (len(cart)):
        if (type(cart[i]) == tuple):
            row = cur.execute("SELECT * FROM book WHERE isbn = ?",(cart[i][0],)).fetchall()
            # Checks if there is enough stock to fulfill order
            if (int(cart[i+1])>int(row[0][7])):
                print("Not enough in stock to complete this request for: "+ str(cart[i][0])+", "+ str(cart[i][1]))
            else:
                # There is enough stock to fulfill order
                newStock = int(row[0][7]) -int(cart[i+1])
                cur.execute("Update book set stock = ?, copiesSold = ? where isbn = ?", (newStock,cart[i+1],cart[i][0] ))
                # If this is the first book, then create a new order
                if (firstEntryCreateOrder):
                    shipping = input("Enter shipping information: ")
                    billing = input("Enter billing information: ")
                    cur.execute("INSERT or IGNORE INTO orders (shippingInfo, billingInfo, trackingInfo , userID) values (?, ?, ?, ?)",
                        (shipping, billing, 'Order Processed ', userID))
                    firstEntryCreateOrder =False
                    orderID =cur.lastrowid
                    print("You can track your order with the following order number: "+str(orderID))
                
                # Insert book to newly created order
                con.execute("INSERT or IGNORE INTO partOf (orderId, ISBN, numberofCopies ) values (?, ?, ?)",
                    (orderID, cart[i][0], cart[i+1],))
                if (userRole=='admin' and newStock<=3):
                    row = cur.execute("SELECT * FROM publisher WHERE name = ?",(cart[i][9],)).fetchall()

                    print("The number of copies of "+str(cart[i][0])+": "+str(cart[i][1])+" is below 4")
                    print("Sending a buy order for "+str((10-newStock))+" more copies to: "+row[0][0])

            print("\n")
    # Empty cart
    cart=[]
    con.commit()

# If same book has multiple cart entries, consolidate them into one entry 
def consolidateCart(row, quantity):
    global cart
    if row in cart:
        for i in range (len(cart)):
            if (type(cart[i]) == tuple):
                if cart[i] == row:
                    newint = int(cart[i+1])
                    newint+=int(quantity)
                    cart[i+1] = newint       
    else:
        cart.append(row)
        cart.append(quantity)


# main loop for the user to interact with
def main():
    userInput = ''
    while (userInput != "q"):
        if userInput=='1': viewOrder()
        elif userInput=='2': searchBook()
        elif userInput=='3': viewBook() 
        elif userInput=='4': addToCart()
        elif userInput=='5': checkout()
        elif userInput=='6' and userRole == 'admin': addBook()
        elif userInput=='7' and userRole == 'admin': removeBook()
        elif userInput=='8' and userRole == 'admin': viewPublishers()
        elif userInput=='9' and userRole == 'admin': viewReports()
        print('\n')
        print("Books in Store:")
        rows = cur.execute("SELECT isbn, title, author FROM book").fetchall()
        for row in rows:
            prettyBook(row)
            print('\n')

        # Prints commands to the screen
        if(userRole =='guest'):
            for command in user:
                print(command)
        else:
            for command in admin:
                print(command)
        userInput = input("Enter a command: ")

# Asks for user input to either login or create an account
def login():
    global userRole, userID
    print("{:<20} {:>5}".format('Login:',1)+"\n"+"{:<20} {:>5}".format('Create Account:',2))
    option = input("Enter a command: ")
    option = '1'
    while not(option == "1" or option == "2"):
        print("Please enter a valid command")
        option = input("Enter a command: ")

    rows = cur.execute("SELECT * FROM user").fetchall()
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    if (username == "" or password == ""):
        print("\nPlease enter a Username and Password")
        login()
        return
    # Login
    if(option =='1'):
        rows = cur.execute("SELECT * FROM user").fetchall()
        flag = False
        for row in rows:
            if username == row[3] and password == row[4]:
                print("Login Successful")
                flag = True
                userRole = row[5]
                userID = row[0]
                break
        if(not flag):
            print("Error: incorrect login information")
            login()
            return
    # Create an Account
    elif (option =='2'):
        global userid
        shipping = input("Enter shipping information: ")
        billing = input("Enter billing information: ")
        cur.execute("insert into user (shippingInfo,billingInfo,username,password,role) values (?, ?, ?, ?, ?)",
            (shipping, billing, username, password, "guest"))
        userRole = "guest"
        userID = row[0]
        print("Acount Created")
        con.commit()    

con = sqlite3.connect('termProjectDB.db')
cur =con.cursor()


if __name__ == "__main__":
    login()
    main()
