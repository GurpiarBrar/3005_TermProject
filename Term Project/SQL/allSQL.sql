
CREATE TABLE IF NOT EXISTS publisher (name TEXT PRIMARY KEY, email TEXT, address TEXT, phoneNum TEXT NOT NULL, bankingInfo TEXT NOT NULL)

CREATE TABLE IF NOT EXISTS book 
        (isbn INTEGER PRIMARY KEY, title TEXT, author TEXT, genre TEXT, 
        sellPrice INTEGER, PublisherSalesCut INTEGER, copiesSold INTEGER, 
        stock INTEGER, NumberofPages INTEGER, publisher TEXT,
        FOREIGN KEY(publisher) REFERENCES publisher(name))

CREATE TABLE IF NOT EXISTS user (userID INTEGER PRIMARY KEY AUTOINCREMENT, shippingInfo TEXT, billingInfo TEXT, username TEXT NOT NULL, password TEXT NOT NULL, Role TEXT NOT NULL)
CREATE TABLE IF NOT EXISTS orders 
        (orderID INTEGER PRIMARY KEY AUTOINCREMENT, shippingInfo TEXT, billingInfo TEXT, 
        trackingInfo TEXT, userID INTEGER,
        FOREIGN KEY(userID) REFERENCES user(userID))
CREATE TABLE IF NOT EXISTS partOf 
        (orderID INTEGER, ISBN INTEGER, numberOfCopies INTEGER, 
        PRIMARY KEY (orderID, ISBN),
        FOREIGN KEY(orderID) REFERENCES orders(orderID),
        FOREIGN KEY(ISBN) REFERENCES book(isbn))

Select genre, sum(copiesSold) as copies, sum(copiesSold * sellPrice) as gross, sum((copiesSold * sellPrice)-copiesSold * sellPrice * (PublisherSalesCut)/100) as publisher
        From book
        Group By genre

Select publisher, sum(copiesSold) as copies, sum(copiesSold * sellPrice) as gross, sum((copiesSold * sellPrice)-copiesSold * sellPrice * (PublisherSalesCut)/100) as pub
        From book
        Group By publisher
-- Inserts are done by a for loop and an array of values
-- It would be easier to view the initDB insert function to view those sql statements