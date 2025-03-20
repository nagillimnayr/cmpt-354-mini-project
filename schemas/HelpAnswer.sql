CREATE TABLE IF NOT EXISTS HelpAnswer (
  answerId INTEGER PRIMARY KEY,
  personnelId INTEGER,
  answer TEXT NOT NULL,
  datePublished DATE NOT NULL,
  questionId INTEGER NOT NULL,

  FOREIGN KEY (personnelId) REFERENCES Personnel(personnelId),
  FOREIGN KEY (questionId) REFERENCES HelpQuestion(questionId)
);
