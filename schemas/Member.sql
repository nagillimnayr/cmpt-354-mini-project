CREATE TABLE IF NOT EXISTS Member (
  memberId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  firstName VARCHAR(64) NOT NULL,
  lastName VARCHAR(64) NOT NULL,
  dateOfBirth DATE,
  phoneNumber VARCHAR(25)
);
