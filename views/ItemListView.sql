-- Retrieves subset of `Item` information along with counts of the total
-- number of instances, and the number of available copies.
CREATE VIEW IF NOT EXISTS ItemListView
AS 
SELECT 
  itemId, 
  title,
  author,
  format,
  (
    SELECT COUNT(*) 
    FROM ItemInstance 
    WHERE ItemInstance.itemId = Item.itemId
  ) AS numCopies,
  (
    SELECT COUNT(*) 
    FROM ItemInstance 
    WHERE 
      ItemInstance.itemId = Item.itemId
      AND 
      ItemInstance.currentCheckoutId IS NULL
  ) AS availableCopies
FROM Item;
