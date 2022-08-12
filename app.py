import os
from binance import Client
from telebot import TeleBot, types
from flask import Flask, request

TOKEN = '5509203861:AAEWFddFGfz_WxaFyN6GwLGguF3xOxFlR44'
APP_NAME = 'BVIP'

bot = TeleBot(TOKEN)
server = Flask(__name__)
client = Client()

@bot.message_handler(commands=['start'], chat_types=['private'])
def startPrivate(msg : types.Message):
    bot.send_message(
        msg.chat.id,
        '<b>Welcome To BIB BOT \n\nUsage : /p btc</b>'.format(msg.from_user.first_name),
        parse_mode='html',
        reply_to_message_id=msg.id,
        disable_web_page_preview=True
    )

@bot.message_handler(func= lambda msg : msg.text.startswith('/p'))
def getPrice(msg):
    symbol = msg.text.split('/p ')
    if len(symbol) == 1:
        bot.send_message(msg.chat.id, '*Example : /p BTC*', parse_mode='markdown')
        return
    try:
        symbol_ = symbol[1].upper()
        result = client.get_ticker(symbol = f'{symbol_}USDT')
        current_price = result['lastPrice']
        price_change = result['priceChange']
        price_change_percentage = result['priceChangePercent']

        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton(text='SIGNUP ON BIB',url='https://www.bibvip.net/register?inviteCode=0Mwsw9' )
        )
        markup.add(
            types.InlineKeyboardButton(text='FEATURES',url='https://www.bibvip.com/en_US/futures' )
        )
        markup.add(
            types.InlineKeyboardButton(text='BIB CHAT',url='https://t.me/BIB_Global' )
        )
        markup.add(
            types.InlineKeyboardButton(text='BIB META',url='https://t.me/bibmetachannel' )
        )
        text_to_send = f'*💎 {symbol_} Price Today*\n\n➛ Price: *{str(current_price)}$*\n📉 Price Change: *{str(price_change)}$*\n🔴 Change Percent: *{str(price_change_percentage)}%*'

        bot.send_message(
            msg.chat.id,
            text_to_send,
            parse_mode='markdown',
            reply_markup=markup
        )
    except:
        bot.send_message(msg.chat.id, '*❌ This currency is not supported or either it is wrong!*', parse_mode='markdown')


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/setWebhook")
def webhook():
    if not APP_NAME or not TOKEN:
        return 'Setup TOKEN & URL environment variable from heroku dashboard.'
    bot.remove_webhook()
    bot.set_webhook(url= f'https://{APP_NAME}.herokuapp.com/{TOKEN}')
    return "Webhook Done!", 200

@server.route("/")
def home():
    return "<h1>Server Running!</h1>", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
