-- Retrieves `Item` information for an `ItemInstance`.
CREATE VIEW IF NOT EXISTS ItemInstanceView
AS 
SELECT *
FROM ItemInstance JOIN Item USING(itemId); 
