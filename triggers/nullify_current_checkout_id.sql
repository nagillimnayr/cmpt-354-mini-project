-- Nullify `currentCheckoutId` when `ItemInstance` is returned.
CREATE TRIGGER IF NOT EXISTS nullify_current_checkout_id 
AFTER UPDATE ON CheckoutRecord
WHEN 
  OLD.returnDate IS NULL 
  AND 
  NEW.returnDate IS NOT NULL
BEGIN 
  UPDATE ItemInstance
  SET currentCheckoutId = NULL
  WHERE 
    ItemInstance.itemId = NEW.itemId 
    AND 
    ItemInstance.instanceId = NEW.instanceId
  ;
END;
