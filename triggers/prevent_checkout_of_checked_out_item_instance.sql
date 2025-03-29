-- Prevent an item instance from being checked out if it is already checked out.
-- If an item instance is available then `currentCheckoutId` will be `NULL`.
CREATE TRIGGER IF NOT EXISTS prevent_checkout_of_checked_out_item_instance 
BEFORE INSERT ON CheckoutRecord
WHEN (
  SELECT currentCheckoutId 
  FROM ItemInstance
  WHERE 
    itemId = NEW.itemId 
    AND
    instanceId = NEW.instanceId
) IS NOT NULL
BEGIN 
  SELECT RAISE (ABORT, 'ERROR: Item is already checked out');
END;
