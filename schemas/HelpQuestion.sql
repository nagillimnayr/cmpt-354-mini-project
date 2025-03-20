CREATE TABLE IF NOT EXISTS HelpQuestion (
  questionId INTEGER PRIMARY KEY,
  memberId INTEGER,
  question TEXT NOT NULL,
  datePublished DATE NOT NULL,

  FOREIGN KEY (memberId) REFERENCES Member(memberId)
);
