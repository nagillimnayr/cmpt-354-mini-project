-- Fines should be issued only upon the return of an overdue item.
-- If fine is issued for an item that has not been returned, abort.
CREATE TRIGGER IF NOT EXISTS prevent_fine_for_unreturned_item
BEFORE INSERT ON OverdueFine
WHEN 
  (
    SELECT CheckoutRecord.returnDate
    FROM CheckoutRecord
    WHERE CheckoutRecord.checkoutId = NEW.checkoutId
  ) IS NULL 
BEGIN
  SELECT 
    RAISE (
      ABORT,
      'Fines can only be issued upon the return of an overdue item.'
    );
END;
