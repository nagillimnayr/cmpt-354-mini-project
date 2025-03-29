-- Trigger to allow updating `OverdueFine`s through the `OutstandingFinesView`.
CREATE TRIGGER IF NOT EXISTS pay_outstanding_fine
  INSTEAD OF UPDATE OF amountPaid ON OutstandingFinesView 
BEGIN 
  UPDATE OverdueFine
  SET amountPaid = NEW.amountPaid
  WHERE OverdueFine.fineId = NEW.fineId;
END;
