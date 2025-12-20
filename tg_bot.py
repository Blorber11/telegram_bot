import telebot
import random
from bot_logic import gen_pass, flip_coin
from telebot import types
from telebot.types import ReactionTypeEmoji

PRICES = {
    'Бантик для подарка': 1,   
    'Обёртка для подарка': 45,   
    'Елочка на новый год': 200,  
    'Подарок': 350,
    'Неизвестность...': 400,
}


bot = telebot.TeleBot("8386218517:AAErHnxkacLOMe5PRvVY6Y_LOHfgAV9zYXY")

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Вот команды, доступные в боте: /hello , /bye , /generation (создает пароль длиной 10 символов), /flipcoin (подкидывает монету), /buy ( купить несуществующий подарок :) )")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет, чтобы увидеть все команды, отправь /help")
    
@bot.message_handler(commands=['hello'])
def send_hello(message):
    bot.reply_to(message, "Привет! Как дела?")
    
@bot.message_handler(commands=['bye'])
def send_bye(message):
    bot.reply_to(message, "Пока! Удачи!")

@bot.message_handler(commands=['generation'])
def passsing(message):
    a=gen_pass(10)
    bot.reply_to(message, a)

@bot.message_handler(commands=['flipcoin'])
def coin(message):
    b=flip_coin()
    bot.reply_to(message, b)

#@bot.message_handler(func=lambda message: True)
#def echo_all(message):
#    bot.reply_to(message, message.text)

@bot.message_handler(commands=['buy'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    
    buttons = [types.KeyboardButton(product) for product in PRICES.keys()]
    
    markup.add(*buttons)
    
    
    bot.reply_to(message, 
                 "Привет, что хочешь купить?",
                 reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in PRICES.keys())
def handle_product_selection(message):
    
    product = message.text
    price = PRICES[product]
    
    
    prices = [types.LabeledPrice(label=product, amount=price)]
    
    
    bot.send_invoice(
        message.chat.id,  
        title=f"Покупка {product}", 
        description=f"Купить {product}",  
        provider_token='',  
        currency='XTR',  
        prices=prices,  
        start_parameter='stars-payment',  
        invoice_payload=product  
    )


@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout_query(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@bot.message_handler(content_types=['successful_payment'])
def handle_successful_payment(message):
    
    product = message.successful_payment.invoice_payload
    bot.reply_to(message, 
                 f"Поздравляю, вы купили {product}")


@bot.message_handler(func=lambda message: True)
def send_reaction(message):
    emo = ["❤️‍🔥"]  
    bot.set_message_reaction(message.chat.id, message.id, [ReactionTypeEmoji(random.choice(emo))], is_big=False)


@bot.message_reaction_handler(func=lambda message: True)
def get_reactions(message):
    bot.reply_to(message, f"You changed the reaction from {[r.emoji for r in message.old_reaction]} to {[r.emoji for r in message.new_reaction]}")

bot.polling()
