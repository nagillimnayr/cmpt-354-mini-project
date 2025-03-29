-- If a member has any overdue items borrowed, or any outstanding fines, they 
-- should not be allowed to borrow any new items until all overdue items 
-- have been returned and all fines have been paid.
CREATE TRIGGER IF NOT EXISTS prevent_checkout_if_member_has_overdue_items 
BEFORE INSERT ON CheckoutRecord
WHEN 
  (
    SELECT COUNT(*) 
    FROM BorrowedItemsView 
    WHERE 
      NEW.memberId = BorrowedItemsView.memberId 
      AND 
      CheckoutRecord.returnDate IS NULL
  ) > 0 
  OR 
  (
    SELECT COUNT(*) 
    FROM OutstandingFinesView
    WHERE OutstandingFinesView.memberId = NEW.memberId
  ) > 0
BEGIN 
  SELECT RAISE (ABORT, 'ERROR: Member has overdue items or outstanding fines');
END;
