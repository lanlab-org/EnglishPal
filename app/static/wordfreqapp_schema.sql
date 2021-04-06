CREATE TABLE user(name TEXT PRIMARY KEY, password TEXT, start_date TEXT, expiry_date TEXT);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE IF NOT EXISTS "article" (
	"article_id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"text"	TEXT,
	"source"	TEXT,
	"date"	TEXT,
	"level"	TEXT,
	"question"	TEXT
);
