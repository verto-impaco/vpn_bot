import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, InputFile, CallbackQuery
from utils.subscription_info import get_user_subscription_info, format_subscription_message
import os
from dotenv import load_dotenv

load_dotenv()

# https://unsplash.com/photos/vibrant-alien-landscape-with-purple-grass-and-orange-sky-4oWJo3N86os старая пикча

BOT_TOKEN = os.getenv('BOT_TOKEN')
MY_TG = os.getenv('MY_TG')

if BOT_TOKEN is None:
    raise ValueError("Переменная окружения BOT_TOKEN не установлена")

bot = telebot.TeleBot(BOT_TOKEN)
path_to_image = 'utils/images-_1_.png'


def create_main_menu():
    """Создает главное меню"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("💳 Оплата", callback_data="pay")
    btn2 = InlineKeyboardButton("🆘 Поддержка", callback_data="support")
    btn3 = InlineKeyboardButton(
        "📊 Моя подписка", callback_data="my_subscription")
    keyboard.add(btn1, btn2, btn3)
    return keyboard


def create_back_keyboard():
    """Создает клавиатуру с кнопкой возврата"""
    keyboard = InlineKeyboardMarkup()
    btn_back = InlineKeyboardButton(
        "◀️ Назад в меню", callback_data="back_to_menu")
    keyboard.add(btn_back)
    return keyboard


def send_main_menu(chat_id, message_id=None):
    """Отправляет или обновляет главное меню"""
    with open(path_to_image, 'rb') as photo:
        if message_id:
            try:
                bot.edit_message_media(
                    chat_id=chat_id,
                    message_id=message_id,
                    media=InputMediaPhoto(
                        InputFile(photo), caption='Привет! Это бот сервиса Update'),
                    reply_markup=create_main_menu()
                )
            except Exception as e:
                print(f"Не удалось обновить сообщение: {e}")
                bot.send_photo(
                    chat_id,
                    InputFile(photo),
                    caption='Привет! Это бот сервиса Update',
                    reply_markup=create_main_menu()
                )


def register_handlers(bot: telebot.TeleBot):
    """Регистрирует все обработчики команд"""

    @bot.message_handler(commands=['start'])
    def handle_start(message):
        user_id = message.from_user.id

        with open(path_to_image, 'rb') as photo:
            bot.send_photo(
                message.chat.id,
                photo,
                caption=f"⚙️ID: {user_id}",
                reply_markup=create_main_menu()
            )

    @bot.message_handler(commands=['mysubscription'])
    def handle_subscription(message):
        user_id = message.from_user.id

        # Получаем данные из БД
        info = get_user_subscription_info(user_id)

        # Форматируем и отправляем
        response_text = format_subscription_message(info)
        bot.reply_to(message, response_text)

    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback(call: CallbackQuery):
        if call.message:
            try:
                action = call.data
                if action == 'pay':
                    bot.edit_message_media(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        media=InputMediaPhoto(
                            media="https://as2.ftcdn.net/v2/jpg/05/32/31/97/1000_F_532319706_82p6u1EnEFxiymxxJSJsVZzqXm90Qx7l.webp",
                            caption=f"💳 *Раздел оплаты*\n\nГоспода, автоматическая оплата будет возможно реализованна в будущем, а пока что пишите мне в личные сообщения {MY_TG}",
                            parse_mode="Markdown"
                        ),
                        reply_markup=create_back_keyboard()
                    )
                    bot.answer_callback_query(call.id)

                elif action == 'support':
                    bot.edit_message_media(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        media=InputMediaPhoto(
                            media="https://as2.ftcdn.net/v2/jpg/05/32/31/97/1000_F_532319706_82p6u1EnEFxiymxxJSJsVZzqXm90Qx7l.webp",
                            caption=f"🆘 *Техническая поддержка*\n\nПо всем вопросам обращайтесь: {MY_TG}\n\nВаш ID: {call.from_user.id}",
                            parse_mode="Markdown"
                        ),
                        reply_markup=create_back_keyboard()
                    )
                    bot.answer_callback_query(call.id)

                elif action == 'my_subscription':
                    # Получаем информацию о подписке
                    info = get_user_subscription_info(call.from_user.id)
                    subscription_text = format_subscription_message(info)
                    bot.edit_message_media(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        media=InputMediaPhoto(
                            media="https://as2.ftcdn.net/v2/jpg/05/32/31/97/1000_F_532319706_82p6u1EnEFxiymxxJSJsVZzqXm90Qx7l.webp",
                            caption=f"📊 МОЯ ПОДПИСКА\n\n{subscription_text}\n\nЧтобы приобрести подписку передайте ваш айди ({call.from_user.id}) администратору: {MY_TG}",
                            parse_mode="Markdown"
                        ),
                        reply_markup=create_back_keyboard()
                    )
                    bot.answer_callback_query(call.id)
                # if action == "pay":
                #     bot.answer_callback_query(
                #         call.id, "Вы выбрали раздел Оплата")

                #     bot.delete_message(call.message.chat.id,
                #                        call.message.message_id)

                #     with open(path_to_image, 'rb') as photo:
                #         bot.send_photo(
                #             call.message.chat.id,
                #             photo,
                #             caption="💳 *Раздел оплаты*\n\nВыберите способ оплаты или вернитесь в меню:",
                #             reply_markup=create_back_keyboard(),
                #         )

                # elif call.data == "support":
                #     bot.answer_callback_query(
                #         call.id, "Вы выбрали раздел Поддержка")

                #     bot.delete_message(call.message.chat.id,
                #                        call.message.message_id)

                #     with open(path_to_image, 'rb') as photo:
                #         bot.send_photo(
                #             call.message.chat.id,
                #             photo,
                #             caption=f"🆘 *Техническая поддержка*\n\nПо всем вопросам обращайтесь: {my_tg}\n\nВаш ID: {call.from_user.id}",
                #             reply_markup=create_back_keyboard(),
                #         )

                # elif call.data == "my_subscription":
                #     bot.answer_callback_query(
                #         call.id, "Загрузка информации о подписке")

                #     bot.delete_message(call.message.chat.id,
                #                        call.message.message_id)

                #     # Получаем информацию о подписке
                #     info = get_user_subscription_info(call.from_user.id)
                #     subscription_text = format_subscription_message(
                #         info)  # ← ВАЖНО: используем форматирование

                #     with open(path_to_image, 'rb') as photo:
                #         bot.send_photo(
                #             call.message.chat.id,
                #             photo,
                #             # ← теперь текст красивый
                #             caption=f"📊 МОЯ ПОДПИСКА\n\n{subscription_text}",
                #             reply_markup=create_back_keyboard()
                #         )

                elif call.data == "back_to_menu":
                    bot.answer_callback_query(
                        call.id, "Возврат в главное меню")
                    send_main_menu(call.message.chat.id,
                                   call.message.message_id)

                else:
                    bot.answer_callback_query(call.id, "Неизвестная команда")

            except Exception as e:
                print(f"Ошибка в обработчике callback: {e}")
                bot.answer_callback_query(
                    call.id, "Произошла ошибка. Попробуйте позже.")
        else:
            # Сообщение недоступно (возможно, удалено или это inline режим)
            print("Сообщение недоступно или это inline запрос")
            bot.answer_callback_query(call.id, "Сообщение устарело")


# Регистрируем обработчики
register_handlers(bot)
