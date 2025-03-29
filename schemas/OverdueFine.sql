CREATE TABLE IF NOT EXISTS OverdueFine (
    fineId INTEGER PRIMARY KEY,
    checkoutId INTEGER NOT NULL UNIQUE, -- Maximum one fine per `CheckoutRecord`
    fineTotal DECIMAL(5,2) NOT NULL,
    amountPaid DECIMAL(5,2) NOT NULL DEFAULT 0.00,

    FOREIGN KEY (checkoutId) 
        REFERENCES CheckoutRecord(checkoutId)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    
    CHECK (amountPaid <= fineTotal)
);
