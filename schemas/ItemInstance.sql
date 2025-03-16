CREATE TABLE IF NOT EXISTS ItemInstance (
    instanceId INTEGER PRIMARY KEY,
    itemId INTEGER NOT NULL,
    currentCheckoutId INTEGER, -- nullable, because the item may not be currently checked out
    FOREIGN KEY (itemId) REFERENCES Item(itemId),
    FOREIGN KEY (currentCheckoutId) REFERENCES CheckoutRecord(checkoutId)
);
