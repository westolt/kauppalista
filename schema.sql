CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE shopping_list (
    id INTEGER PRIMARY KEY,
    name TEXT,
    password TEXT,
    creator_id INTEGER REFERENCES users(id),
    creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE shopping_list_user (
    shopping_list_id INTEGER,
    user_id INTEGER,
    PRIMARY KEY (shopping_list_id, user_id),
    FOREIGN KEY (shopping_list_id) REFERENCES shopping_list(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);