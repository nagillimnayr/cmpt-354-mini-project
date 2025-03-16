CREATE TABLE IF NOT EXISTS OverdueFine (
    fineId INTEGER PRIMARY KEY,
    checkoutId INTEGER NOT NULL,
    fineTotal DECIMAL(5,2) NOT NULL,
    amountPaid DECIMAL(5,2) NOT NULL DEFAULT 0.00,
    dateIssued DATE NOT NULL,

    FOREIGN KEY (checkoutId) REFERENCES CheckoutRecord(checkoutId)
);
