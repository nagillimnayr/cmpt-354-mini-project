CREATE TABLE Event (
    eventId INTEGER PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    type VARCHAR(50),
    dateTimeStart TIMESTAMP NOT NULL,
    dateTimeEnd TIMESTAMP NOT NULL,
    roomId INTEGER NOT NULL,

    FOREIGN KEY (roomId) REFERENCES SocialRoom(roomId)
);
