CREATE TABLE IF NOT EXISTS CheckoutRecord (
    checkoutId INTEGER PRIMARY KEY,
    memberId INTEGER NOT NULL,
    itemId INTEGER NOT NULL,
    instanceId INTEGER NOT NULL,
    librarianId INTEGER NOT NULL,
    checkoutDate DATE NOT NULL,
    dueDate DATE NOT NULL,
    returnDate DATE,

    FOREIGN KEY (memberId) REFERENCES Member(memberId),
    FOREIGN KEY (itemId) REFERENCES Item(itemId),
    FOREIGN KEY (instanceId) REFERENCES ItemInstance(instanceId),
    FOREIGN KEY (librarianId) REFERENCES Librarian(librarianId)
);
