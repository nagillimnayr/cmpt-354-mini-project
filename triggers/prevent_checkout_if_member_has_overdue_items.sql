-- If a member has any overdue items borrowed, they  should not be allowed to 
-- borrow any new items until all overdue items have been returned.
CREATE TRIGGER IF NOT EXISTS prevent_checkout_if_member_has_overdue_items 
BEFORE INSERT ON CheckoutRecord
WHEN 
  (
    SELECT COUNT(*) 
    FROM CheckoutRecord 
    WHERE 
      NEW.memberId = CheckoutRecord.memberId 
      AND 
      -- Borrowed item has not been returned.
      CheckoutRecord.returnDate IS NULL
      AND 
      -- It is past due date of borrowed item.
      JULIANDAY(DATE(current_date, 'localtime')) >= JULIANDAY(CheckoutRecord.dueDate)
  ) > 0 
BEGIN 
  SELECT RAISE (ABORT, 'ERROR: Member has overdue items');
END;
