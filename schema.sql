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

CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE item (
    id INTEGER PRIMARY KEY,
    name TEXT,
    quantity TEXT,
    shopping_list_id INTEGER REFERENCES shopping_list(id),
    category_id INTEGER REFERENCES categories(id),
    added_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE purchased_item (
    id INTEGER PRIMARY KEY,
    name TEXT,
    quantity TEXT,
    shopping_list_id INTEGER REFERENCES shopping_list(id),
    purchased_by_user_id INTEGER REFERENCES users(id),
    price DECIMAL(10, 2),
    purchase_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT OR IGNORE INTO categories (name) VALUES 
('Elintarvikkeet'),
('Käyttötavarat'),
('Muut');