import mysql.connector


def initDbConnection(config):
    context = mysql.connector.connect(
        host=config["Database"]["host"],
        port=config["Database"]["port"],
        user=config["Database"]["username"],
        password=config["Database"]["password"],
        database=config["Database"]["database"])
    return context


def closeConn(context):
    # Разрываем подключение.
    context.close()
