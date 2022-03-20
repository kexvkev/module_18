import telebot
import telebot.types
from config import keys,TOKEN
from utils import ConvertionException,CryptoConverter


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def testing(message : telebot.types.Message):
    bot.send_message(message.chat.id , 'Чтобы начать работу введите команду боту в следующем формате:/n <имя валюты>'' \
<в какую валюту перевести>\n Увидеть список доступных валют: /values')
@bot.message_handler(commands=['values'])
def value(message:telebot.types.Message):
    text=bot.send_message(message.chat.id,'Доступные валюты:')
    for key in keys.keys():
        text= '\n'.join(dict(keys))
    bot.reply_to(message,text)
@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    quote, base, amount = (message.text.split(' '))
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров.')

        total_base=CryptoConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message,f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message,f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id,text)


bot.polling(none_stop=True)
