DROP TABLE if EXISTS accounts;
DROP TABLE if EXISTS messages;

CREATE TABLE accounts (
    id integer PRIMARY KEY AUTOINCREMENT,
	user text NOT NULL,
    password text NOT NULL,
    avatar text
);
CREATE TABLE messages (
	id integer PRIMARY KEY AUTOINCREMENT,
	user text NOT NULL,
	board text NOT NULL,
	body text,
	avatar text
);
