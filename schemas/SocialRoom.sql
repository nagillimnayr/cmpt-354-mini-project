CREATE TABLE SocialRoom (
    roomId INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    capacity INTEGER NOT NULL CHECK (capacity > 0)
);
