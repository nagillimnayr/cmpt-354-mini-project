CREATE TABLE IF NOT EXISTS Personnel (
  personnelId INTEGER PRIMARY KEY,
  memberId INTEGER NOT NULL UNIQUE,
  role VARCHAR(50) NOT NULL,
  dateJoined DATE NOT NULL,
  salary REAL CHECK(salary >= 0),

  FOREIGN KEY (memberId) REFERENCES Member(memberId)
);
