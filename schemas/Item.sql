CREATE TABLE IF NOT EXISTS Item (
    itemId INTEGER PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    author VARCHAR(100),
    format VARCHAR(50),
    publishDate DATE,
    publisher VARCHAR(100)
);
