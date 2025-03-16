CREATE TABLE IF NOT EXISTS MemberAudienceType (
    memberId INTEGER NOT NULL,
    audienceType VARCHAR(50) NOT NULL,
    PRIMARY KEY (memberId, audienceType),

    FOREIGN KEY (memberId) REFERENCES Member(memberId),
    FOREIGN KEY (audienceType) REFERENCES Audience(audienceType)
);
