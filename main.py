import telebot
from database.db_session import init_db
from handlers.message_handlers import register_handlers
import os
from dotenv import load_dotenv

load_dotenv()


def main():
    BOT_TOKEN = os.getenv('BOT_TOKEN')

    if BOT_TOKEN is None:
        raise ValueError("BOT_TOKEN не найден в переменных окружения")
    # Инициализация базы данных (создание таблиц)
    print("🔄 Инициализация базы данных...")
    init_db()
    print("✅ База данных готова")

    # Создание бота
    bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)

    # Регистрация обработчиков
    register_handlers(bot)

    # Запуск поллинга
    print("🚀 Бот запущен и ожидает сообщения...")
    bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    main()
