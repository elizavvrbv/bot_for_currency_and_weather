from telebot import TeleBot, types
from package.weather import get_weather
from package.currency import get_main_currencies
import logging

level = logging.DEBUG
logger = logging.getLogger("log")
form = "%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s"
logger.setLevel(level)
fh = logging.FileHandler(filename=f"log.txt", encoding="UTF-8")
fh.setFormatter(logging.Formatter(form))
fh.setLevel(level)
logger.addHandler(fh)
logger.debug(f"Logger was initialized")

TOKEN = '5535429972:AAF6gALeYPninEfitow4PPoStDBtL6LkFjU'
bot = TeleBot(TOKEN)


@bot.message_handler(command=["start"])
def start(message):
    logger.debug(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("Погода"),
        types.KeyboardButton("Курс валют")
    )
    logger.debug("{0.first_name}".format(message.from_user))
    bot.send_message(message.chat.id, "Привет, {0.first_name}!".format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    logger.debug(f"Chat ID - {message.chat.id}")
    logger.debug("First Name - {0.first_name}".format(message.from_user))
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text == "Погода":
        loc_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        loc_markup.add(
            types.KeyboardButton(text="Отправить местоположение", request_location=True)
        )
        bot.send_message(message.chat.id, "Нажми на кнопку и передай мне свое местоположение",
                         reply_markup=loc_markup)
    elif message.text == "Курс валют":
        bot.send_message(message.chat.id, get_main_currencies())
    else:
        markup.add(
            types.KeyboardButton("Погода"),
            types.KeyboardButton("Курс валют")
        )
        bot.send_message(message.chat.id, "Мои функции \n Погода - отправляет погоду по текущей геолокации \n "
                                          "Курс валют - отправляет курсы ЦБ РФ по трем основным валютам",
                         reply_markup=markup)


@bot.message_handler(content_types=["location"])
def location(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("Погода"),
        types.KeyboardButton("Курс валют")
    )
    if message.location is not None:
        logger.debug(f"lat - {message.location.latitude}, lon - {message.location.longitude}")
        bot.send_message(message.chat.id, get_weather(message.location.latitude, message.location.longitude),
                         reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Ошибка при получении геолокации")


bot.polling(none_stop=True, interval=0)
