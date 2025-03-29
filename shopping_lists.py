import db

def create_list(name, password_hash, creator_id):
    sql = "INSERT INTO shopping_list (name, password, creator_id) VALUES (?, ?, ?)"
    db.execute(sql, (name, password_hash, creator_id))

    shopping_list_id = db.execute("SELECT last_insert_rowid()")

    sql_user = "INSERT INTO shopping_list_user (shopping_list_id, user_id) VALUES (?, ?)"
    db.execute(sql_user, (shopping_list_id, creator_id))

def get_lists(user_id):
    sql = """
    SELECT s.id, s.name
    FROM shopping_list s
    LEFT JOIN shopping_list_user slu ON s.id = slu.shopping_list_id
    WHERE s.creator_id = :user_id OR slu.user_id = :user_id
    """
    return db.query(sql, {"user_id": user_id})

def get_list(shopping_list_id):
    sql = """
    SELECT id, name 
    FROM shopping_list 
    WHERE id = ?;
    """
    result = db.query(sql, [shopping_list_id])
    return result[0]

def get_items(shopping_list_id):
    sql = """
    SELECT id, name, quantity 
    FROM item 
    WHERE shopping_list_id = ?;
    """
    return db.query(sql, [shopping_list_id])