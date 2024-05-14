import re

from telegram import Update
from telegram.ext import ConversationHandler


def verify_password(update: Update, context):
    update.message.reply_text('Пожалуйста, отправьте пароль для проверки.')
    return 'password_response'


def password_response(update: Update, context):
    password = update.message.text
    if re.fullmatch(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
        update.message.reply_text('Пароль сложный.')
    else:
        update.message.reply_text('Пароль простой.')

    return ConversationHandler.END