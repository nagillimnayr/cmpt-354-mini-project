CREATE TABLE IF NOT EXISTS ItemInstance (
    instanceId INTEGER NOT NULL,
    itemId INTEGER NOT NULL,
    currentCheckoutId INTEGER, -- nullable, because the item may not be currently checked out

    PRIMARY KEY (instanceId, itemId)
    FOREIGN KEY (itemId) REFERENCES Item(itemId),
    FOREIGN KEY (currentCheckoutId) REFERENCES CheckoutRecord(checkoutId)
);
