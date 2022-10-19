# Здесь хранятся пользовательские данные.
# Т.к. это словарь в памяти, то при перезапуске он очистится

CONFIG_STORE_FILE = "config/store.json"


class ResponseProduct:
    def __init__(self, name="", price="", url=""):
        self.name = name
        self.price = price
        self.link_url = url

    name = ""
    price = ""
    link_url = ""

    def product_not_found(self) -> bool:
        return self.price is None and self.name is None


class StoreFields:
    STORE = "store"
    URL = "url"
    SELECTOR = "selector"
    CLAZZ = "clazz"
    NAME_CLASS = "class_prod_name"
    PRICE_CLASS = "class_prod_price"
    LINK_URL = "link_url"
    BASE_URL = "base_url"


class ProductKeys:
    EVERY = "every"
    CHANGE = "change"
    LOW = "low"
