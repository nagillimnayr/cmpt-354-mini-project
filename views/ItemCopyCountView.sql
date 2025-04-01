-- Retrieves `Item` information along with counts of the total
-- number of copies, and the number of available copies.
CREATE VIEW IF NOT EXISTS ItemCopyCountView
AS 
SELECT DISTINCT 
  *,
  (
    SELECT COUNT(*) 
    FROM ItemInstance 
    WHERE ItemInstance.itemId = Item.itemId
  ) AS totalCopies,
  (
    SELECT COUNT(*) 
    FROM ItemInstance 
    WHERE 
      ItemInstance.itemId = Item.itemId
      AND 
      ItemInstance.currentCheckoutId IS NULL
  ) AS availableCopies
FROM 
  Item;
