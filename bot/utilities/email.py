import os
import re
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ConversationHandler


def find_email(update: Update, context):
    update.message.reply_text('Пожалуйста, отправьте текст для поиска email-адресов.')
    return 'email_response'


def email_response(update: Update, context):
    text = update.message.text
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    if emails:
        found_emails = '\n'.join(emails)
        update.message.reply_text(f'Найдены следующие email-адреса:\n{found_emails}\nВозможно, некоторые из них ранее не встречались. '
                                  f'Хотите проверить это и в случае чего записать новые адреса в базу данных? Ответьте "да" или "нет".')
        context.user_data['emails'] = emails
        return 'email_store_decision'
    else:
        update.message.reply_text('Email-адреса не найдены.')
        return ConversationHandler.END


def email_store_decision(update: Update, context):
    decision = update.message.text.lower()
    answer = ""
    if decision == 'да':
        for email in context.user_data['emails']:
            load_dotenv()

            dbUser = os.getenv('DB_USER')
            host = os.getenv('DB_HOST')
            password = os.getenv('DB_PASSWORD')
            db = os.getenv('DB_DATABASE')

            try:
                connection = psycopg2.connect(user=dbUser,
                                              host=host,
                                              password=password,
                                              database=db)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM emails WHERE email=%s", (email,))
                if cursor.fetchone() is None:
                    cursor.execute("INSERT INTO emails (email) VALUES (%s)", (email,))
                    answer += email + " "
                connection.commit()
            except psycopg2.Error as e:
                update.message.reply_text('Ошибка на стороне сервера: не удалось добавить в базу данных')
                return ConversationHandler.END

        if answer != "":
            update.message.reply_text('Следующие email-адреса оказались уникальными и были успешно записаны в базу данных:\n' + answer)
        else:
            update.message.reply_text('Все найденные email-адреса уже находятся в базе данных')
    elif decision == 'нет':
        update.message.reply_text('Email-адреса не были записаны в базу данных.')
    else:
        update.message.reply_text('Неизвестный ответ. Пожалуйста, ответьте "да" или "нет".')
        return 'email_store_decision'
    return ConversationHandler.END
