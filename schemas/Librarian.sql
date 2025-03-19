CREATE TABLE IF NOT EXISTS Librarian (
  librarianId INTEGER PRIMARY KEY,
  memberId INTEGER NOT NULL UNIQUE,
  isVolunteer BOOLEAN NOT NULL,
  dateJoined DATE NOT NULL,

  FOREIGN KEY (memberId) REFERENCES Member(memberId)
);
