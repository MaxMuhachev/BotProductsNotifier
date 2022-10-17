# Включаем логирование, чтобы не пропустить важные сообщения
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config.config import load_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Настройка логирования в stdout
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger.error("Starting bot")

# Парсинг файла конфигурации
config = load_config("config/config.ini")
# Объявление и инициализация объектов бота и диспетчера
bot = Bot(token=config["tg_bot"]["token"])
# Диспетчер для бота
dp = Dispatcher(bot, storage=MemoryStorage())