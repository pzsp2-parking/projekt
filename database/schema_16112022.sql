CREATE TABLE IF NOT EXISTS clients (
    username varchar(25) PRIMARY KEY,
    password varchar(255) NOT NULL,
    mail varchar(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS cars (
    registration_nr varchar(7) NOT NULL,
    username varchar(25) NOT NULL,
    FOREIGN KEY (username) REFERENCES clients (username)
);
