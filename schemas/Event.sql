CREATE TABLE IF NOT EXISTS Event (
    eventId INTEGER PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    type VARCHAR(50),
    dateTimeStart DATETIME NOT NULL,
    dateTimeEnd DATETIME NOT NULL,
    roomId INTEGER NOT NULL,

    FOREIGN KEY (roomId) REFERENCES SocialRoom(roomId)
);
