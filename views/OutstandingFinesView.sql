CREATE VIEW IF NOT EXISTS OutstandingFinesView
AS
SELECT *
FROM 
  OverdueFine JOIN CheckoutRecord USING(checkoutId)
WHERE 
  OverdueFine.amountPaid < OverdueFine.fineTotal;
