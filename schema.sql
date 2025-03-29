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
    shopping_list_id INTEGER REFERENCES shopping_list(id),
    user_id INTEGER REFERENCES users(id),
    PRIMARY KEY (shopping_list_id, user_id)
);

CREATE TABLE item (
    id INTEGER PRIMARY KEY,
    name TEXT,
    quantity TEXT,
    shopping_list_id INTEGER REFERENCES shopping_list(id),
    added_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
);