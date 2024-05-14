import os
import re
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ConversationHandler


def find_phone_number(update: Update, context):
    update.message.reply_text('Введите текст для поиска телефонных номеров: ')
    return 'findPhoneNumbers'


def findPhoneNumbers(update: Update, context):
    user_input = update.message.text
    phoneNumRegex = re.compile( r'\+7\d{10}|8\d{10}|8\(\d{3}\)\d{7}|8 \d{3} \d{3} \d{2} \d{2}|8 \(\d{3}\) \d{3} \d{2} \d{2}|8-\d{3}-\d{3}-\d{2}-\d{2}')
    phoneNumberList = phoneNumRegex.findall(user_input)

    if not phoneNumberList:
        update.message.reply_text('Телефонные номера не найдены')
    else:
        found_phoneNumbers = '\n'.join(phoneNumberList)
        update.message.reply_text(f'Найдены следующие номера телефонов:\n{found_phoneNumbers}\nВозможно, некоторые из них ранее не встречались. '
                                  f'Хотите проверить это и в случае чего записать новые адреса в базу данных? Ответьте "да" или "нет"')
        context.user_data['phoneNumbers'] = phoneNumberList
        return 'phone_store_decision'
    return ConversationHandler.END


def phone_store_decision(update: Update, context):
    decision = update.message.text.lower()
    if decision == 'да':
        answer = ""
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

            for phoneNumber in context.user_data['phoneNumbers']:
                cursor.execute("SELECT * FROM phones WHERE phone_number=%s", (phoneNumber,))
                if cursor.fetchone() is None:
                    cursor.execute("INSERT INTO phones (phone_number) VALUES (%s)", (phoneNumber,))
                    answer += phoneNumber + " "
            connection.commit()
        except psycopg2.Error as e:
            update.message.reply_text('Ошибка на стороне сервера: не удалось добавить в базу данных')
            return ConversationHandler.END

        if answer != "":
            update.message.reply_text('Следующие номера телефонов оказались уникальными и были успешно записаны в базу данных:\n' + answer)
        else:
            update.message.reply_text('Все найденные номера телефонов уже находятся в базе данных')
    elif decision == 'нет':
        update.message.reply_text('Номера телефонов не были записаны в базу данных')
    else:
        update.message.reply_text('Неизвестный ответ. Пожалуйста, ответьте "да" или "нет"')
        return 'phone_store_decision'
    return ConversationHandler.END
