CREATE TABLE IF NOT EXISTS EventAttendance (
    eventId INTEGER NOT NULL,
    memberId INTEGER NOT NULL,
    PRIMARY KEY (eventId, memberId),

    FOREIGN KEY (eventId) REFERENCES Event(eventId),
    FOREIGN KEY (memberId) REFERENCES Member(memberId)
);
