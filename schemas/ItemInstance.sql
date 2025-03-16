CREATE TABLE IF NOT EXISTS ItemInstance (
    instanceId INTEGER NOT NULL,
    itemId INTEGER NOT NULL,
    currentCheckoutId INTEGER UNIQUE, -- nullable, because the item may not be currently checked out.
    -- Unique because no two ItemInstances should have the same CheckoutRecord.

    PRIMARY KEY (instanceId, itemId)
    FOREIGN KEY (itemId) REFERENCES Item(itemId),
    FOREIGN KEY (currentCheckoutId) REFERENCES CheckoutRecord(checkoutId)
);
