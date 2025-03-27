import db

def create_list(name, password_hash, creator_id):
    sql = "INSERT INTO shopping_list (name, password, creator_id) VALUES (?, ?, ?)"
    db.execute(sql, (name, password_hash, creator_id))

def get_lists(user_id):
    sql = "SELECT name FROM shopping_list WHERE creator_id = :user_id"
    return db.query(sql, {"user_id": user_id})