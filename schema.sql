CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE shopping_list (
    id INTEGER PRIMARY KEY,
    name TEXT,
    password TEXT,
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
    for_user_id INTEGER REFERENCES users(id),
    added_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE category (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE item_category (
    item_id INTEGER REFERENCES item(id),
    category_id INTEGER REFERENCES category(id),
    PRIMARY KEY (item_id, category_id)
);