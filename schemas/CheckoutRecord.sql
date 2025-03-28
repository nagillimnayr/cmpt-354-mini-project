CREATE TABLE IF NOT EXISTS CheckoutRecord (
    checkoutId INTEGER PRIMARY KEY,
    memberId INTEGER NOT NULL,
    itemId INTEGER NOT NULL,
    instanceId INTEGER NOT NULL,
    checkoutDate DATE NOT NULL,
    dueDate DATE NOT NULL,
    returnDate DATE DEFAULT NULL,

    FOREIGN KEY (memberId) 
        REFERENCES Member(memberId)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (itemId, instanceId) 
        REFERENCES ItemInstance(itemId, instanceId)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
