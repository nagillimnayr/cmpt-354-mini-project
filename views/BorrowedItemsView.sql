-- Retrieves records for unreturned items for a `Member`.
CREATE VIEW IF NOT EXISTS BorrowedItemsView
AS 
SELECT *
FROM 
  ItemInstanceView 
  JOIN 
  CheckoutRecord 
  ON currentCheckoutId = checkoutId AND returnDate IS NULL;
