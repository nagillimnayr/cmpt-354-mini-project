-- If a member has any outstanding fines, they should not be allowed to borrow 
-- any new items until all fines have been paid.
CREATE TRIGGER IF NOT EXISTS prevent_checkout_if_member_has_outstanding_fines 
BEFORE INSERT ON CheckoutRecord
WHEN 
  (
    SELECT COUNT(*) 
    FROM OutstandingFinesView
    WHERE 
      NEW.memberId = OutstandingFinesView.memberId 
  ) > 0 
BEGIN 
  SELECT RAISE (ABORT, 'Member has outstanding fines');
END;
