import telebot
from config import TOKEN, dict_names
from extentions import Converter, Convert_exception

bot = telebot.TeleBot(TOKEN)

def return_instruction():   #возвращает инструкцию пользователя
    return f"Для конвертации валюты введи команду в формате:\n" \
           f"<название валюты> <в какую валюту перевести> <сумма> без скобочек\n" \
           f"Для вывода списка доступных валют набери команду /values\n" \
           f"Для помощи не забудь ввести команду /help"


# Обрабатываются сообщения, содержащие команду '/start'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Привет, {message.chat.username}!\n"
                                      f"Я - бот-помощник в конвертации валют "+return_instruction())

@bot.message_handler(commands=['values'])
def send_welcome(message):
    bot.send_message(message.chat.id, '\n'.join(dict_names.keys()))

# Обрабатываются сообщения, содержащие команду '/help'.
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, return_instruction())


# Обрабатываются текстовые сообщения
@bot.message_handler(content_types=['text'])
def handle_docs_text(message: telebot.types.Message):
    try:
        values = message.text.lower().split()
        if len(values) != 3:
            raise Convert_exception('В сообщении должно быть три параметра\n')
        else:
            quote, base, amount = values
        price = Converter.get_price(quote, base, amount)
    except Convert_exception as e:
        bot.reply_to(message, f'Ошибка ввода\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        if quote == base:   #Конвертация одинаковых валют возможна и без api
            bot.send_message(message.chat.id, f'Цена {amount} {quote} => {base} составит {amount}')
        else:

            bot.send_message(message.chat.id, f'Цена {amount} {quote} => {base} составит {price}')


bot.polling(none_stop=True)
