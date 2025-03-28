CREATE TABLE IF NOT EXISTS ItemInstance (
    itemId INTEGER NOT NULL,
    instanceId INTEGER NOT NULL,
    currentCheckoutId INTEGER UNIQUE DEFAULT NULL, -- nullable, because the item may not be currently checked out.
    -- Unique because no two ItemInstances should have the same CheckoutRecord.

    PRIMARY KEY (itemId, instanceId)
    FOREIGN KEY (itemId) REFERENCES Item(itemId),
    FOREIGN KEY (currentCheckoutId) REFERENCES CheckoutRecord(checkoutId)
);
