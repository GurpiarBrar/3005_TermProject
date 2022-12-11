import sqlite3
def createTable():
    # con.execute("DROP TABLE publisher")
    # con.execute("DROP TABLE book")
    # con.execute("DROP TABLE user")
    # con.execute("DROP TABLE orders")
    # con.execute("DROP TABLE partOf")
    con.execute("CREATE TABLE IF NOT EXISTS publisher (name TEXT PRIMARY KEY, email TEXT, address TEXT, phoneNum TEXT NOT NULL, bankingInfo TEXT NOT NULL)" )

    con.execute('''CREATE TABLE IF NOT EXISTS book 
        (isbn INTEGER PRIMARY KEY, title TEXT, author TEXT, genre TEXT, 
        sellPrice INTEGER, PublisherSalesCut INTEGER, copiesSold INTEGER, 
        stock INTEGER, NumberofPages INTEGER, publisher TEXT,
        FOREIGN KEY(publisher) REFERENCES publisher(name))''' )

    con.execute("CREATE TABLE IF NOT EXISTS user (userID INTEGER PRIMARY KEY AUTOINCREMENT, shippingInfo TEXT, billingInfo TEXT, username TEXT NOT NULL, password TEXT NOT NULL, Role TEXT NOT NULL)" )

    con.execute('''CREATE TABLE IF NOT EXISTS orders 
        (orderID INTEGER PRIMARY KEY AUTOINCREMENT, shippingInfo TEXT, billingInfo TEXT, 
        trackingInfo TEXT, userID INTEGER,
        FOREIGN KEY(userID) REFERENCES user(userID))''' )
    con.execute('''CREATE TABLE IF NOT EXISTS partOf 
        (orderID INTEGER, ISBN INTEGER, numberOfCopies INTEGER, 
        PRIMARY KEY (orderID, ISBN),
        FOREIGN KEY(orderID) REFERENCES orders(orderID),
        FOREIGN KEY(ISBN) REFERENCES book(isbn))''' )
    print("Tables Created")



def insert():
    pubslishers=[('Tor Books' , 'Tor@macmillan.com', '432 Commerce Drive', '555-753-9922', 'Chase Bank 778341'),
        ('Penguin Publishing' , 'PenguinPublishing@gmail.com', '145 Laswell Avenue', '555-908-1772', 'Scotia Bank 667213'),
        ('Harper Collins' , 'HarperCollins@gmail.com', '122 Spruce Street', '555-882-1165', 'Bank of America 114435'),
        ('Jump Magazine' , 'jump@shonenjump.jp', '22 Tendo Street', '555-942-1107', 'Bank of Japan 339647')]

    books =[(201, 'The Way of Kings', 'Brandon Sanderson', 'Fantasy', 20, 20, 0, 10, 374, 'Tor Books'),
        (202, 'Words of Radiance', 'Brandon Sanderson', 'Fantasy', 20, 20, 0, 10, 411, 'Tor Books'),
        (203, 'Oathbringer', 'Brandon Sanderson', 'Fantasy', 20, 20, 0, 10, 442, 'Tor Books'),
        (204, 'Skyward', 'Brandon Sanderson', 'Science Fiction', 21, 30, 0, 10, 355, 'Penguin Publishing'),
        (205, 'Starsight', 'Brandon Sanderson', 'Science Fiction', 22, 30, 0, 10, 390, 'Penguin Publishing'),
        (206, 'Cytonic', 'Brandon Sanderson', 'Science Fiction', 25, 40, 0, 10, 500, 'Penguin Publishing'),
        (207, 'Harry Potter and the Sorcerers Stone', 'J.K. Rowling', 'Fantasy', 17, 50, 0, 10, 300, 'Harper Collins'),
        (208, 'Harry Potter and the Chamber of Secrets', 'J.K. Rowling', 'Fantasy', 19, 50, 0, 10, 333, 'Harper Collins'),
        (209, 'Harry Potter and the Prisoner of Azkaban', 'J.K. Rowling', 'Fantasy', 19, 50, 0, 10, 341, 'Harper Collins'),
        (210, 'Hunter X Hunter Volume 1', 'Yoshihiro Togashi', 'Shonen', 13, 30, 0, 10, 223, 'Jump Magazine'),
        (211, 'Hunter X Hunter Volume 2', 'Yoshihiro Togashi', 'Shonen', 13, 30, 0, 10, 226, 'Jump Magazine'),
        (212, 'YuYu Hakusho Volume 1', 'Yoshihiro Togashi', 'Shonen', 15, 30, 0, 10, 215, 'Jump Magazine'),
        (213, 'YuYu Hakusho Volume 2', 'Yoshihiro Togashi', 'Shonen', 15, 30, 0, 10, 229, 'Jump Magazine'),]
    con.execute("INSERT or IGNORE INTO user (shippingInfo,billingInfo,username,password,role) values (?, ?, ?, ?, ?)",
            ('coming later', 'credit card', 'Gurpiar','pass', 'admin'))
    con.execute("INSERT or IGNORE INTO user (shippingInfo,billingInfo,username,password,role) values (?, ?, ?, ?, ?)",
            ('on the way', 'debit card', 'Johnson', 'code', 'guest'))
    for entity in pubslishers:
        con.execute("INSERT or IGNORE INTO publisher (name,email,address,phoneNum,bankingInfo) values (?, ?, ?, ?, ?)",
            entity)
    for entity in books:
        con.execute('''INSERT or IGNORE INTO book (isbn, title, author, genre, 
                sellPrice, PublisherSalesCut, copiesSold, 
                stock, NumberofPages, publisher) values (?, ?, ?, ?, ?,?,?,?,?,?)''',entity)
    print("Values Inserted")

    
    
# Runs the following two methods and commits the changes after completion of each function
with sqlite3.connect('termProjectDB.db') as con:
    createTable()
    insert()


cur =con.cursor()
