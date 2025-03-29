-- Nullify `currentCheckoutId` when `ItemInstance` is returned.
CREATE TRIGGER IF NOT EXISTS nullify_current_checkout_id 
AFTER UPDATE ON CheckoutRecord
WHEN 
  NEW.returnDate IS NOT NULL
BEGIN 
  UPDATE ItemInstance
  SET currentCheckoutId = NULL
  WHERE 
    itemId = NEW.itemId 
    AND
    instanceId = NEW.instanceId;
END;
