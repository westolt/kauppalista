import db

def log_in(username):
    sql = "SELECT id, password_hash FROM users WHERE username = ?;"
    return db.query(sql, [username])

def create_user(username, password_hash):
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?);"
    db.execute(sql, [username, password_hash])

def create_list(name, password_hash, creator_id):
    sql = "INSERT INTO shopping_list (name, password, creator_id) VALUES (?, ?, ?);"
    db.execute(sql, [name, password_hash, creator_id])

    shopping_list_id = db.execute("SELECT last_insert_rowid()")

    sql_user = "INSERT INTO shopping_list_user (shopping_list_id, user_id) VALUES (?, ?);"
    db.execute(sql_user, [shopping_list_id, creator_id])

def get_list_by_name(name):
    sql = "SELECT id, password FROM shopping_list WHERE name = ?;"
    return db.query(sql, [name])

def join_list(shopping_list_id, user_id):
    sql = "INSERT INTO shopping_list_user (shopping_list_id, user_id) VALUES (?, ?);"
    db.execute(sql, [shopping_list_id, user_id])

def get_lists(user_id):
    sql = """
    SELECT s.id, s.name
    FROM shopping_list s
    LEFT JOIN shopping_list_user slu ON s.id = slu.shopping_list_id
    WHERE s.creator_id = ? OR slu.user_id = ?;
    """
    return db.query(sql, [user_id, user_id])

def get_list(shopping_list_id):
    sql = """
    SELECT id, name 
    FROM shopping_list 
    WHERE id = ?;
    """
    result = db.query(sql, [shopping_list_id])
    return result[0]

def add_item_to_list(name, quantity, shopping_list_id):
    sql = "INSERT INTO item (name, quantity, shopping_list_id) VALUES (?, ?, ?);"
    db.execute(sql, [name, quantity, shopping_list_id])

def delete_item(item_id, shopping_list_id):
    sql = "DELETE FROM item WHERE id = ? AND shopping_list_id = ?;"
    db.execute(sql, [item_id, shopping_list_id])

def update_item(name, quantity, item_id, shopping_list_id):
    sql = "UPDATE item SET name = ?, quantity = ? WHERE id = ? AND shopping_list_id = ?;"
    db.execute(sql, [name, quantity, item_id, shopping_list_id])

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

def get_users(shopping_list_id):
    sql = """
    SELECT u.id, u.username
    FROM users u
    JOIN shopping_list_user slu ON u.id = slu.user_id
    WHERE slu.shopping_list_id = ?;
    """
    return db.query(sql, [shopping_list_id])