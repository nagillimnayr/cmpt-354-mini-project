CREATE TABLE IF NOT EXISTS Member (
  memberId INTEGER PRIMARY KEY NOT NULL,
  firstName VARCHAR(50) NOT NULL,
  lastName VARCHAR(50) NOT NULL,
  dateOfBirth DATE,
  phoneNumber VARCHAR(25)
);
