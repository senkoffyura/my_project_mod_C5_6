import telebot
from config import keys, TOKEN
from extensions import ConvertionExseption, СurrencyConverter


bot = telebot.TeleBot(TOKEN)

# Обрабатывается сообщение, содержащие команду '/start /help'
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду в следующем формате: \n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\nУвидеть список всех доступных валют: /value'
    bot.reply_to(message, text)

# Обрабатывается сообщение, содержащие команду '/value'.
@bot.message_handler(commands=['value'])
def handle_value(message: telebot.types.Message):
    text = "Доступные валюты:"
    for i in keys.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

# обработка текстового запроса
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        value = message.text.split(' ')

        if len(value) != 3:
            raise ConvertionExseption('Слишком много параметров')

        base, quote, amount = value
        # получение актуального курса запрошенной валюты
        currency_exchange_rate = СurrencyConverter.get_price(base, quote, amount)

    except ConvertionExseption as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Неудалось обработать команду\n{e}')
    else:
        # конвертация валют
        total_base = str(round(float(currency_exchange_rate)*float(amount),2))
        text = f'Цена {amount} {base} в {quote} - {total_base} при обменном курсе {base} к {quote} - {currency_exchange_rate}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)