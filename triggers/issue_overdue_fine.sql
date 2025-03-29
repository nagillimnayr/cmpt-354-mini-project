-- When a borrowed item is returned, if it is overdue, issue a fine. 
-- Overdue fines are charged at a rate of $1.50 per day late, up to a 
-- maximum of $100. 
CREATE TRIGGER IF NOT EXISTS issue_overdue_fine 
AFTER UPDATE ON CheckoutRecord
WHEN 
  OLD.returnDate IS NULL 
  AND 
  NEW.returnDate IS NOT NULL
  AND 
  JULIANDAY(NEW.returnDate) > JULIANDAY(NEW.dueDate)
BEGIN 
  INSERT INTO OverdueFine(checkoutId, fineTotal) 
  VALUES (
    NEW.checkoutId, 
    MIN(FLOOR(JULIANDAY(NEW.returnDate) - JULIANDAY(NEW.dueDate)) * 1.50, 100.00)
  );
END;
