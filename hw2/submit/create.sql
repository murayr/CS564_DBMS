-- Drop tables in reverse order of dependency
DROP TABLE IF EXISTS Bid;
DROP TABLE IF EXISTS Category;
DROP TABLE IF EXISTS Item;
DROP TABLE IF EXISTS AuctionUser;

-- Create AuctionUser table
CREATE TABLE AuctionUser (
    UserID VARCHAR(255) PRIMARY KEY,
    Rating INTEGER NOT NULL,
    Location VARCHAR(255),
    Country VARCHAR(255)
);

-- Create Item table
CREATE TABLE Item (
    ItemID VARCHAR(255) PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Currently DECIMAL(10,2) NOT NULL,
    Buy_Price DECIMAL(10,2),
    First_Bid DECIMAL(10,2) NOT NULL,
    Number_of_Bids INTEGER NOT NULL,
    Location VARCHAR(255),
    Country VARCHAR(255),
    Started DATETIME NOT NULL,
    Ends DATETIME NOT NULL,
    SellerID VARCHAR(255) NOT NULL,
    Description TEXT,
    FOREIGN KEY (SellerID) REFERENCES AuctionUser(UserID)
);

-- Create Category table (many-to-many relationship with Item)
CREATE TABLE Category (
    ItemID VARCHAR(255),
    Category VARCHAR(255),
    PRIMARY KEY (ItemID, Category),
    FOREIGN KEY (ItemID) REFERENCES Item(ItemID)
);

-- Create Bid table
CREATE TABLE Bid (
    ItemID VARCHAR(255),
    BidderID VARCHAR(255),
    Time DATETIME NOT NULL,
    Amount DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (ItemID, BidderID, Time),
    FOREIGN KEY (ItemID) REFERENCES Item(ItemID),
    FOREIGN KEY (BidderID) REFERENCES AuctionUser(UserID)
);
