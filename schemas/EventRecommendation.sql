CREATE TABLE EventRecommendation (
    eventId INTEGER NOT NULL,
    audienceType VARCHAR(50) NOT NULL,
    PRIMARY KEY (eventId, audienceType),

    FOREIGN KEY (eventId) REFERENCES Event(eventId),
    FOREIGN KEY (audienceType) REFERENCES Audience(audienceType)
);
