-- Set `currentCheckoutId` of `ItemInstance` when instance is checked out.
CREATE TRIGGER IF NOT EXISTS set_current_checkout_id 
AFTER INSERT ON CheckoutRecord
WHEN 
  NEW.returnDate IS NULL        
BEGIN 
  UPDATE ItemInstance
  SET currentCheckoutId = NEW.checkoutId
  WHERE 
    itemId = NEW.itemId 
    AND
    instanceId = NEW.instanceId;
END;
