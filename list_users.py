import db

def get_user(user_id):
    sql = """
    SELECT id, username
    FROM users u
    JOIN shopping_list_user slu ON u.id = slu.user_id
    WHERE user_id = ?;
    """
    result = db.query(sql, [user_id])
    return result[0] if result else None

def purchased_items_by_user(user_id, shopping_list_id):
    sql = """
    SELECT name, quantity, price, purchase_time
    FROM purchased_item
    WHERE purchased_by_user_id = ? AND shopping_list_id = ?
    ORDER BY purchase_time;
    """
    return db.query(sql, [user_id, shopping_list_id])

def total(user_id, shopping_list_id):
    sql = """
    SELECT SUM(price) as total_price
    FROM purchased_item
    WHERE purchased_by_user_id = ? AND shopping_list_id = ?;
    """
    result = db.query(sql, [user_id, shopping_list_id])
    return result[0]["total_price"] if result and result[0]["total_price"] else 0