-- Retrieves the name of the member along with the question.
CREATE VIEW IF NOT EXISTS HelpQuestionView(
  questionId, 
  memberId, 
  question, 
  datePublished,
  firstName,
  lastName
) AS 
SELECT 
  questionId, memberId, question, datePublished, firstName, lastName 
FROM 
  HelpQuestion JOIN Member USING(memberId)
;
