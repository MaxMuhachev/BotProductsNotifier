import configparser


def load_config(path):
    config = configparser.ConfigParser()
    config.sections()
    config.read(path)
    config.sections()
    return config
