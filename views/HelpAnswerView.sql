-- Retrieves the answer along with the name of the personnel and their role.
CREATE VIEW IF NOT EXISTS HelpAnswerView 
AS 
SELECT 
  answerId, questionId, personnelId, answer, datePublished, firstName, lastName, role 
FROM 
  HelpAnswer JOIN PersonnelView USING(personnelId)
;
