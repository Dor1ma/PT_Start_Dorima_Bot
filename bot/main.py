import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

from remoteMachines.linux import get_release, get_uname, get_uptime, get_df, get_free, get_mpstat, get_w, get_auths, \
    get_critical, \
    get_ps, get_ss, get_apt_list, apt_list_response, get_services, get_repl_logs
from utilities.basic import start, helpCommand
from utilities.email import find_email, email_response, email_store_decision, get_emails
from utilities.password import verify_password, password_response
from utilities.phone import find_phone_number, findPhoneNumbers, phone_store_decision, get_phones

TOKEN = os.getenv('TOKEN')

logging.basicConfig(
    filename='logfile.txt', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    convHandlerFindPhoneNumbers = ConversationHandler(
        entry_points=[CommandHandler('find_phone_number', find_phone_number)],
        states={
            'findPhoneNumbers': [MessageHandler(Filters.text & ~Filters.command, findPhoneNumbers)],
            'phone_store_decision': [MessageHandler(Filters.text & ~Filters.command, phone_store_decision)],
        },
        fallbacks=[]
    )

    convHandlerFindEmailAddresses = ConversationHandler(
        entry_points=[CommandHandler('find_email', find_email)],
        states={
            'email_response': [MessageHandler(Filters.text & ~Filters.command, email_response)],
            'email_store_decision': [MessageHandler(Filters.text & ~Filters.command, email_store_decision)],
        },
        fallbacks=[]
    )

    convHandlerPasswordChecker = ConversationHandler(
        entry_points=[CommandHandler('verify_password', verify_password)],
        states={
            'password_response': [MessageHandler(Filters.text & ~Filters.command, password_response)],
        },
        fallbacks=[]
    )

    dp.add_handler(CommandHandler("get_emails", get_emails))
    dp.add_handler(CommandHandler("get_phones", get_phones))

    convHandlerAptList = ConversationHandler(
        entry_points=[CommandHandler('get_apt_list', get_apt_list)],
        states={
            'apt_list_response': [MessageHandler(Filters.text & ~Filters.command, apt_list_response)],
        },
        fallbacks=[]
    )

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", helpCommand))
    dp.add_handler(convHandlerFindPhoneNumbers)
    dp.add_handler(convHandlerFindEmailAddresses)
    dp.add_handler(convHandlerPasswordChecker)

    dp.add_handler(CommandHandler("get_release", get_release))
    dp.add_handler(CommandHandler("get_uname", get_uname))
    dp.add_handler(CommandHandler("get_uptime", get_uptime))

    dp.add_handler(CommandHandler("get_df", get_df))
    dp.add_handler(CommandHandler("get_free", get_free))
    dp.add_handler(CommandHandler("get_mpstat", get_mpstat))
    dp.add_handler(CommandHandler("get_w", get_w))

    dp.add_handler(CommandHandler("get_auths", get_auths))
    dp.add_handler(CommandHandler("get_critical", get_critical))

    dp.add_handler(CommandHandler("get_ps", get_ps))
    dp.add_handler(CommandHandler("get_ss", get_ss))
    dp.add_handler(convHandlerAptList)
    dp.add_handler(CommandHandler("get_services", get_services))

    dp.add_handler(CommandHandler("get_repl_logs", get_repl_logs))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
