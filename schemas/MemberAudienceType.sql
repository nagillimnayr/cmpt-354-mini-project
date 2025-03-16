-- Many-to-Many Relationship between Members and Audiences. 
-- A member can be a part of many audiences, and an audience can have
-- many members.
CREATE TABLE IF NOT EXISTS MemberAudienceType (
    memberId INTEGER NOT NULL,
    audienceType VARCHAR(50) NOT NULL,
    PRIMARY KEY (memberId, audienceType),

    FOREIGN KEY (memberId) REFERENCES Member(memberId),
    FOREIGN KEY (audienceType) REFERENCES Audience(audienceType)
);
