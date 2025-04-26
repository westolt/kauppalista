import db

def log_in(username):
    sql = "SELECT id, password_hash FROM users WHERE username = ?;"
    return db.query(sql, [username])

def create_user(username, password_hash):
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?);"
    db.execute(sql, [username, password_hash])

def create_list(name, password_hash, user_id):
    sql = "INSERT INTO shopping_list (name, password) VALUES (?, ?);"
    db.execute(sql, [name, password_hash])

    shopping_list_id = db.last_insert_id()

    sql_user = "INSERT INTO shopping_list_user (shopping_list_id, user_id) VALUES (?, ?);"
    db.execute(sql_user, [shopping_list_id, user_id])

    return shopping_list_id

def get_list_by_name(name):
    sql = "SELECT id, password FROM shopping_list WHERE name = ?;"
    return db.query(sql, [name])

def join_list(shopping_list_id, user_id):
    sql = "INSERT INTO shopping_list_user (shopping_list_id, user_id) VALUES (?, ?);"
    db.execute(sql, [shopping_list_id, user_id])

def remove_user_from_list(user_id, shopping_list_id):
    sql = "DELETE FROM shopping_list_user WHERE shopping_list_id = ? AND user_id = ?;"
    db.execute(sql, [shopping_list_id, user_id])

def get_lists(user_id):
    sql = """
    SELECT s.id, s.name
    FROM shopping_list s
    JOIN shopping_list_user slu ON s.id = slu.shopping_list_id
    WHERE slu.user_id = ?;
    """
    return db.query(sql, [user_id])

def get_list(shopping_list_id):
    sql = """
    SELECT id, name 
    FROM shopping_list 
    WHERE id = ?;
    """
    result = db.query(sql, [shopping_list_id])
    return result[0]

def add_item_to_list(name, quantity, category_id, shopping_list_id):
    sql = "INSERT INTO item (name, quantity, category_id, shopping_list_id) VALUES (?, ?, ?, ?);"
    db.execute(sql, [name, quantity, category_id, shopping_list_id])

def delete_item(item_id, shopping_list_id):
    sql = "DELETE FROM item WHERE id = ? AND shopping_list_id = ?;"
    db.execute(sql, [item_id, shopping_list_id])

def update_item(name, quantity, item_id, category_id, shopping_list_id):
    sql = "UPDATE item SET name = ?, quantity = ?, category_id = ? WHERE id = ? AND shopping_list_id = ?;"
    db.execute(sql, [name, quantity, category_id, item_id, shopping_list_id])

def get_item(item_id, shopping_list_id):
    sql = "SELECT id, name, quantity FROM item WHERE id = ? AND shopping_list_id = ?;"
    return db.query(sql, [item_id, shopping_list_id])

def get_items(shopping_list_id):
    sql = """
    SELECT id, name, quantity 
    FROM item 
    WHERE shopping_list_id = ?;
    """
    return db.query(sql, [shopping_list_id])

def buy_item(price, buyer, item_id, shopping_list_id):
    item_sql = "SELECT name, quantity FROM item WHERE id = ? AND shopping_list_id = ?"
    item = db.query(item_sql, [item_id, shopping_list_id])[0]

    insert_sql = """
    INSERT INTO purchased_item
    (name, quantity, shopping_list_id, purchased_by_user_id, price)
    VALUES (?, ?, ?, ?, ?)
    """
    db.execute(insert_sql, [item["name"], item["quantity"], shopping_list_id, buyer, price])

    delete_sql = "DELETE FROM item WHERE id = ? AND shopping_list_id = ?"
    db.execute(delete_sql, [item_id, shopping_list_id])

def get_users(shopping_list_id):
    sql = """
    SELECT u.id, u.username
    FROM users u
    JOIN shopping_list_user slu ON u.id = slu.user_id
    WHERE slu.shopping_list_id = ?;
    """
    return db.query(sql, [shopping_list_id])

def get_categories():
    sql = "SELECT name FROM categories ORDER BY name;"
    return db.execute(sql)

def get_users_count(shopping_list_id):
    sql = """
    SELECT COUNT(DISTINCT user_id) as users_count
    FROM shopping_list_user
    WHERE shopping_list_id = ?;
    """
    result = db.query(sql, [shopping_list_id])
    return result[0]["users_count"] if result else 0

def has_user_access(shopping_list_id, user_id):
    sql = "SELECT 1 FROM shopping_list_user WHERE shopping_list_id = ? AND user_id = ?"
    result = db.query(sql, [shopping_list_id, user_id])
    return len(result) > 0

def delete_entire_list(shopping_list_id):
    sql_users = "DELETE FROM shopping_list_user WHERE shopping_list_id = ?"
    db.execute(sql_users, [shopping_list_id])

    sql_items = "DELETE FROM item WHERE shopping_list_id = ?"
    db.execute(sql_items, [shopping_list_id])

    sql_purchased = "DELETE FROM purchased_item WHERE shopping_list_id = ?"
    db.execute(sql_purchased, [shopping_list_id])

    sql_list = "DELETE FROM shopping_list WHERE id = ?"
    db.execute(sql_list, [shopping_list_id])