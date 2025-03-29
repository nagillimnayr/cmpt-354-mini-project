-- We can't use subqueries inside `CHECK` or `ASSERTION` statements, so we must
-- use a `TRIGGER` to impose constraint on number of `OverdueFine`s for a single
-- `CheckoutRecord`.
-- Maximum of ten overdue fines per checked out item.
CREATE TRIGGER IF NOT EXISTS max_overdue_fines_per_checkout 
BEFORE INSERT ON OverdueFine 
WHEN (
    SELECT COUNT(*)
    FROM OverdueFine AS O
    WHERE O.checkoutId = NEW.checkoutId
  ) >= 10
BEGIN
    SELECT 
    RAISE (ABORT, 'Maximum number of fines reached for this Checkout');
END;
