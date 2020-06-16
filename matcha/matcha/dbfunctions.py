from matcha import sql

def register_user(conn, cur, user):
    with conn:
        cur.execute("INSERT INTO employees VALUES (:first, :last, :pay)", {'first': user.first, 'last': user.last, 'pay': user.pay})