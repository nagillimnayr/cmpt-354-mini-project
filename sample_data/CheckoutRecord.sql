INSERT INTO CheckoutRecord (checkoutId, memberId, itemId, instanceId, checkoutDate, dueDate, returnDate) 
VALUES
  (1, 1, 1, 1, '2025-01-02', '2025-01-16', '2025-01-15'), -- Returned 1 day early
  (2, 2, 2, 3, '2025-01-05', '2025-01-19', '2025-01-22'), -- Returned 3 days late
  (3, 3, 4, 5, '2025-01-08', '2025-01-22', NULL), -- Not yet returned
  (4, 4, 6, 7, '2025-01-12', '2025-01-26', NULL), -- Not yet returned
  (5, 5, 8, 9, '2025-01-15', '2025-01-29', '2025-01-29'), -- Returned on time
  (6, 6, 10, 11, '2025-01-20', '2025-02-03', '2025-02-05'), -- Returned 2 days late
  (7, 7, 12, 13, '2025-01-23', '2025-02-06', '2025-02-09'), -- Returned 3 days late
  (8, 8, 14, 15, '2025-01-26', '2025-02-09', '2025-02-11'), -- Returned 2 days late
  (9, 9, 3, 4, '2025-02-01', '2025-02-15', NULL), -- Not yet returned
  (10, 10, 5, 6, '2025-02-05', '2025-02-19', '2025-02-19'), -- Returned on time
  (11, 11, 7, 8, '2025-02-10', '2025-02-24', NULL), -- Not yet returned
  (12, 12, 9, 10, '2025-02-14', '2025-02-28', NULL), -- Not yet returned
  (13, 13, 11, 12, '2025-02-18', '2025-03-04', NULL), -- Not yet returned
  (14, 14, 13, 14, '2025-02-22', '2025-03-08', NULL), -- Not yet returned
  (15, 15, 15, 15, '2025-03-01', '2025-03-15', NULL); -- Not yet returned
