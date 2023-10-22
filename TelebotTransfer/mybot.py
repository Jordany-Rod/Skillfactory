import telebot
from config import keys, TOKEN
from extensions import ConvertionExeption, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def echo_test(message: telebot.types.Message):
    text = 'Чтобы начать работу введите комманду боту в следующем формате: \n<имя валюты, цену которой он хочет узнать>\
 <имя валюты, в которой надо узнать цену первой валюты>\
 <количество первой валюты>\n Увидеть весь список валют можно через: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(massage: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(massage, text)

@bot.message_handler(content_types=['text',])
def get_price(massage: telebot.types.Message):
    try:
        values = massage.text.split(' ')

        if len(values) != 3:
            raise ConvertionExeption('Неверно указаны параметры.')

        quote, base, amount = values
        total_base = APIException.convert(quote, base, amount)
    except ConvertionExeption as e:
        bot.reply_to(massage, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(massage, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(massage.chat.id, text)

bot.polling(none_stop=True)
