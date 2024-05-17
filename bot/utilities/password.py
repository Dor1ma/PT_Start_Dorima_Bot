import re

from telegram import Update
from telegram.ext import ConversationHandler


def verify_password(update: Update, context):
    update.message.reply_text('Пожалуйста, отправьте пароль для проверки.')
    return 'password_response'


def password_response(update: Update, context):
    password = update.message.text
    if re.match(r'^(?=.*[A-Z])'    
        r'(?=.*[a-z])'        
        r'(?=.*\d)'           
        r'(?=.*[!@#$%^&*()?])'  
        r'.{8,}$', password):
        update.message.reply_text('Пароль сложный.')
    else:
        update.message.reply_text('Пароль простой.')

    return ConversationHandler.END