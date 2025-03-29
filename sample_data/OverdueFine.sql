INSERT INTO OverdueFine (checkoutId, fineTotal, amountPaid, dateIssued) 
VALUES
  (2, 5.00, 5.00, '2025-01-23'), -- Brian paid his fine after returning on 2025-01-22
  (3, 7.50, 5.00, '2025-01-23'), -- Catherine partially paid
  (6, 10.00, 10.00, '2025-02-06'), -- Paid immediately after late return
  (7, 4.00, 4.00, '2025-02-10'), -- Paid after returning on 2025-02-09
  (8, 6.50, 6.50, '2025-02-12'), -- Paid after returning on 2025-02-11
  (10, 2.00, 2.00, '2025-02-20'), -- Paid immediately after returning
  (12, 5.00, 0.00, '2025-03-01'), -- Still unpaid
  (13, 3.50, 3.50, '2025-03-05'), -- Paid immediately
  (14, 7.00, 7.00, '2025-03-09'), -- Paid immediately
  (15, 9.50, 9.50, '2025-03-16'), -- Paid immediately
  (1, 2.50, 2.50, '2025-01-17'), -- Alice had a minor fine, paid immediately
  (5, 1.50, 1.50, '2025-01-30'), -- Paid immediately
  (9, 8.00, 0.00, '2025-02-16'), -- Still unpaid
  (11, 4.00, 2.00, '2025-02-25'), -- Partially paid
  (4, 5.00, 5.00, '2025-01-27'); -- David's fine was paid
