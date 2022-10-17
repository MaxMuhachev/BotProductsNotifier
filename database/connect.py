import mysql.connector


def init_db_connection(config):
    context = mysql.connector.connect(
        host=config["Database"]["host"],
        port=config["Database"]["port"],
        user=config["Database"]["username"],
        password=config["Database"]["password"],
        database=config["Database"]["database"])
    return context


def close_conn(context):
    # Разрываем подключение.
    context.close()
