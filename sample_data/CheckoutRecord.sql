-- These `CheckoutRecords` should all be initially unreturned. They
-- will be returned in `UPDATE` statements to ensure that fines are 
-- automatically created by our triggers.
INSERT INTO CheckoutRecord (checkoutId, memberId, itemId, instanceId, checkoutDate, dueDate) 
VALUES
  (1,  1,  1,  1, '2025-01-02', '2025-01-16'),  
  (2,  2,  2,  1, '2025-01-05', '2025-01-19'), 
  (3,  3,  4,  1, '2025-01-08', '2025-01-22'), -- Not yet returned
  (4,  4,  6,  1, '2025-01-12', '2025-01-26'), -- Not yet returned
  (5,  5,  8,  1, '2025-01-15', '2025-01-29'), 
  (6,  6,  10, 1, '2025-01-20', '2025-02-03'), 
  (7,  7,  12, 1, '2025-01-23', '2025-02-06'), 
  (8,  8,  14, 1, '2025-01-26', '2025-02-09'), 
  (9,  9,  3,  1, '2025-02-01', '2025-02-15'), -- Not yet returned
  (10, 10, 5,  1, '2025-02-05', '2025-02-19'), 
  (11, 11, 7,  1, '2025-02-10', '2025-02-24'), -- Not yet returned
  (12, 12, 9,  1, '2025-02-14', '2025-02-28'), -- Not yet returned
  (13, 13, 11, 1, '2025-02-18', '2025-03-04'), -- Not yet returned
  (14, 14, 13, 1, '2025-02-22', '2025-03-08'), -- Not yet returned
  (15, 15, 15, 1, '2025-03-01', '2025-03-15'); -- Not yet returned

-- `UPDATE` statements to activate triggers, which will automatically create 
-- fines for overdue items.

-- Returned 1 day early
UPDATE CheckoutRecord 
SET returnDate = '2025-01-15'  
WHERE checkoutId = 1;

-- Returned 3 days late
UPDATE CheckoutRecord 
SET returnDate = '2025-01-22'  
WHERE checkoutId = 2;

-- Returned on time
UPDATE CheckoutRecord 
SET returnDate = '2025-01-29'  
WHERE checkoutId = 5;

-- Returned 2 days late
UPDATE CheckoutRecord 
SET returnDate = '2025-02-05'  
WHERE checkoutId = 6;

-- Returned 3 days late
UPDATE CheckoutRecord 
SET returnDate = '2025-02-09'  
WHERE checkoutId = 7;

-- Returned 2 days late
UPDATE CheckoutRecord 
SET returnDate = '2025-02-11'
WHERE checkoutId = 8;

-- Returned on time
UPDATE CheckoutRecord 
SET returnDate = '2025-02-19'
WHERE checkoutId = 10;


-- `UPDATE`s to pay off `OverdueFine`s

-- Fully paid off
UPDATE OutstandingFinesView
SET amountPaid = (
  SELECT fineTotal 
  FROM OutstandingFinesView 
  WHERE checkoutId = 2
)
WHERE checkoutId = 2;

-- Partially paid off
UPDATE OutstandingFinesView
SET amountPaid = FLOOR((
  SELECT fineTotal 
  FROM OutstandingFinesView 
  WHERE checkoutId = 3
) * 0.25)
WHERE checkoutId = 3;

-- Fully paid off
UPDATE OutstandingFinesView
SET amountPaid = (
  SELECT fineTotal 
  FROM OutstandingFinesView 
  WHERE checkoutId = 6
)
WHERE checkoutId = 6;

-- Partially paid off
UPDATE OutstandingFinesView
SET amountPaid = FLOOR((
  SELECT fineTotal 
  FROM OutstandingFinesView 
  WHERE checkoutId = 7
) * 0.5)
WHERE checkoutId = 7;

-- Fully paid off
UPDATE OutstandingFinesView
SET amountPaid = (
  SELECT fineTotal 
  FROM OutstandingFinesView 
  WHERE checkoutId = 8
)
WHERE checkoutId = 8;
