CREATE VIEW IF NOT EXISTS PersonnelView(
  personnelId,
  memberId,
  role,
  firstName,
  lastName
) AS 
SELECT 
  personnelId,
  memberId,
  role,
  firstName,
  lastName
FROM 
  Personnel JOIN Member USING(memberId); 
