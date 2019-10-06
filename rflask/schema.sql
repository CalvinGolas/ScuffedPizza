DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL,
    phoneNumber TEXT NOT NULL,
    stateID TEXT NOT NULL,
    deliveryLocation TEXT NOT NULL,
    zipCode TEXT NOT NULL,
    creditCard TEXT NOT NULL,
    expirationDate TEXT NOT NULL,
    cvv TEXT NOT NULL,
    city TEXT NOT NULL
);