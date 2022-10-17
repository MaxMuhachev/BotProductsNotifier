from database.connect import init_db_connection, close_conn
from mysql.connector import Error


async def get_product_py_name(config, name):
    query = "SELECT * FROM products WHERE name= '" + str(name) + "'"
    return fetch_one(config, query)


async def get_product_py_id(config, id):
    query = "SELECT name FROM products WHERE id= " + str(id)
    return fetch_one(config, query)


async def get_last_product_id_by_chat_id(config, chat_id):
    query = "SELECT product_id FROM user_track WHERE chat_id= " + str(chat_id) + " ORDER BY date_updated desc LIMIT 1"
    return fetch_one(config, query)


async def find_notif_every_hours(config):
    query = "SELECT chat_id, product_id, p.name, every_hour FROM user_track " + \
            "JOIN products p on user_track.product_id = p.id " + \
            "WHERE every_hour is not NULL AND DATE_ADD(last_notification, INTERVAL every_hour HOUR) <= now() " + \
            "ORDER BY chat_id desc;"
    return fetch_all(config, query)


async def find_notif_low_price(config):
    query = "SELECT chat_id, product_id, p.name, price_low FROM user_track ut " + \
            "JOIN products p on ut.product_id = p.id " + \
            "WHERE ut.price_low is NOT NULL " + \
            "ORDER BY chat_id desc;"
    return fetch_all(config, query)


async def find_notif_change_price(config):
    query = "SELECT chat_id, product_id, p.name FROM user_track ut " + \
            "JOIN products p on ut.product_id = p.id " + \
            "WHERE notification_price_change <> 0 "
    return fetch_all(config, query)


async def get_products_by_chat_id(config, chat_id):
    query = "SELECT p.name, p.id FROM user_track ut " + \
            " JOIN products p ON p.id = ut.product_id " + \
            "WHERE chat_id = " + str(chat_id)
    return fetch_all(config, query)


async def get_product_last_price(config, chat_id, product_id, store: str):
    query = "SELECT price_last_" + store.lower() + " FROM user_track ut " + \
            " JOIN products p ON p.id = ut.product_id " + \
            "WHERE chat_id = " + str(chat_id) + \
            " AND product_id = " + str(product_id) + ""
    return fetch_one(config, query)


async def find_notif_for_update_price(config, chat_id, product_id):
    query = "SELECT chat_id, product_id, p.name FROM user_track ut " + \
            "JOIN products p on ut.product_id = p.id " + \
            "WHERE notification_price_change <> 0 " + \
            " AND chat_id = " + str(chat_id) + \
            " AND product_id = " + str(product_id) + ""
    return fetch_all(config, query)


async def update_product_last_price(config, price, product_id):
    query = "UPDATE products SET price_last = " + price + \
            " WHERE id = " + str(product_id) + ""
    return execute_query(config, query)


async def update_prod_notif_change(config, chat_id, product_id):
    query = "UPDATE user_track SET notification_price_change = true, " + \
            "every_hour = NULL, price_low = NULL" + \
            " WHERE chat_id = " + str(chat_id) + \
            " AND product_id = " + str(product_id) + ""
    return execute_query(config, query)


def update_date_updated(config, product_id):
    query = "UPDATE user_track SET date_updated = now() WHERE product_id = " + str(product_id)

    return execute_query(config, query)


def add_product(config, name):
    query = "INSERT INTO products(name) VALUE ('" + str(name) + "')"

    execute_query(config, query)
    return fetch_one(config, "SELECT * FROM products WHERE name= '" + str(name) + "'")


async def add_watch_product(config, chat_id, product_id):
    query = "INSERT IGNORE INTO user_track(chat_id, product_id) VALUE (" + str(chat_id) + ", " + str(product_id) + ")"
    return execute_query(config, query)


async def update_chat_every_hour(config, chat_id, product_id, every_hour):
    query = "UPDATE user_track SET every_hour = " + every_hour + \
            ", price_low = NULL, notification_price_change = 0 " + \
            " WHERE chat_id = " + str(chat_id) + \
            " AND product_id = " + str(product_id) + ""
    return execute_query(config, query)


async def update_last_notification_time(config, chat_id, product_id):
    query = "UPDATE user_track SET last_notification = now() " + \
            " WHERE chat_id = " + str(chat_id) + \
            " AND product_id = " + str(product_id) + ""
    return execute_query(config, query)


async def delete_user_track(config, chat_id, product_id):
    query = "DELETE FROM user_track " + \
            " WHERE chat_id = " + str(chat_id) + \
            " AND product_id = " + str(product_id) + ""
    return execute_query(config, query)


async def update_low_price(config, chat_id, product_id, price_low):
    query = "UPDATE user_track SET price_low = " + str(price_low) + \
            ", every_hour = NULL, notification_price_change = 0 " + \
            " WHERE chat_id = " + str(chat_id) + \
            " AND product_id = " + str(product_id) + ""
    return execute_query(config, query)


async def update_last_price(config, product_id, store: str, price):
    query = "UPDATE products SET price_last_" + store.lower() + "='" + str(price) + "'" + \
            " WHERE id = " + str(product_id) + ""
    return fetch_one(config, query)


def fetch_all(config, query):
    context = init_db_connection(config)

    cursor = context.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    close_conn(context)
    return result


def fetch_one(config, query):
    context = init_db_connection(config)

    cursor = context.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    close_conn(context)
    return result


def execute_query(config, query):
    context = init_db_connection(config)
    cursor = context.cursor()
    try:
        cursor.execute(query)
        context.commit()
    except Error as err:
        context.rollback()
        print(err)
    finally:
        close_conn(context)
