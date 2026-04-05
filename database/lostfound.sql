CREATE DATABASE lostfound;

USE lostfound;

CREATE TABLE users (
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(100),
email VARCHAR(100),
password VARCHAR(100),
points INT DEFAULT 0
);

CREATE TABLE lost_items (
id INT AUTO_INCREMENT PRIMARY KEY,
user_id INT,
item_name VARCHAR(100),
description TEXT,
location VARCHAR(100),
image VARCHAR(200),
status VARCHAR(50) DEFAULT 'lost',
FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE found_items (
id INT AUTO_INCREMENT PRIMARY KEY,
user_id INT,
item_name VARCHAR(100),
description TEXT,
location VARCHAR(100),
image VARCHAR(200),
status VARCHAR(50) DEFAULT 'found',
FOREIGN KEY (user_id) REFERENCES users(id)
);


CREATE TABLE claims (
id INT AUTO_INCREMENT PRIMARY KEY,
item_id INT,
claimer_id INT,
message TEXT,
status VARCHAR(50) DEFAULT 'pending',
FOREIGN KEY (claimer_id) REFERENCES users(id)
);

