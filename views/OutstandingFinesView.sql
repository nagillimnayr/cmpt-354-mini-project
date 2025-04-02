CREATE VIEW IF NOT EXISTS OutstandingFinesView
AS
SELECT 
  *,
  (fineTotal - amountPaid) AS balance
FROM 
  OverdueFine JOIN CheckoutRecord USING(checkoutId)
WHERE 
  OverdueFine.amountPaid < OverdueFine.fineTotal;
