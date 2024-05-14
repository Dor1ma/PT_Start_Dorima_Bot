import os
from pathlib import Path

import paramiko
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from dotenv import load_dotenv

load_dotenv()

host = os.getenv('RM_HOST')
port = os.getenv('RM_PORT')
username = os.getenv('RM_USER')
password = os.getenv('RM_PASSWORD')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(hostname=host, username=username, password=password, port=int(port))
    connection_established = True
except Exception as e:
    print(f"Не удалось установить соединение: {e}")
    connection_established = False


def get_repl_logs(update: Update, context: CallbackContext) -> None:
    if connection_established:
        command = 'docker logs -n 15 bot_project_postgres_primary_1'
        stdin, stdout, stderr = client.exec_command(command)

        stdout_data = stdout.read().decode('utf-8')
        stderr_data = stderr.read().decode('utf-8')

        logs = stderr_data
        update.message.reply_text('\n'.join(logs))

        replication_logs = [line for line in logs.split('\n') if 'replication' in line.lower()]
        if replication_logs:
            update.message.reply_text('\n'.join(replication_logs))
        else:
            update.message.reply_text("Логи репликации не найдены")
    else:
        update.message.reply_text("Соединение не установлено")


def execute_command(command: str, update: Update, _: CallbackContext) -> None:
    if connection_established:
        stdin, stdout, stderr = client.exec_command(command)
        update.message.reply_text(stdout.read().decode())
    else:
        update.message.reply_text("Соединение не установлено.")


def get_release(update: Update, context: CallbackContext) -> None:
    execute_command('lsb_release -a', update, context)


def get_uname(update: Update, context: CallbackContext) -> None:
    execute_command('uname -a', update, context)


def get_uptime(update: Update, context: CallbackContext) -> None:
    execute_command('uptime', update, context)


def get_df(update: Update, context: CallbackContext) -> None:
    execute_command('df -h', update, context)


def get_free(update: Update, context: CallbackContext) -> None:
    execute_command('free -h', update, context)


def get_mpstat(update: Update, context: CallbackContext) -> None:
    execute_command('mpstat', update, context)


def get_w(update: Update, context: CallbackContext) -> None:
    execute_command('w', update, context)


def get_auths(update: Update, context: CallbackContext) -> None:
    execute_command('last -n 10', update, context)


def get_critical(update: Update, context: CallbackContext) -> None:
    execute_command('journalctl -p 2 -n 5', update, context)


def get_ps(update: Update, context: CallbackContext) -> None:
    execute_command('ps aux | head -n 10', update, context)


def get_ss(update: Update, context: CallbackContext) -> None:
    execute_command('ss -tulwn', update, context)


def get_apt_list(update: Update, context):
    update.message.reply_text('Пожалуйста, отправьте название пакета или "all" для вывода всех пакетов.')
    return 'apt_list_response'


def apt_list_response(update: Update, context):
    package_name = update.message.text
    if package_name.lower() == 'all':
        execute_command('dpkg --get-selections', update, context)
    else:
        execute_command(f'dpkg --get-selections | grep {package_name}', update, context)
    return ConversationHandler.END


def get_services(update: Update, context: CallbackContext) -> None:
    execute_command('systemctl list-units --type=service | head -n 10', update, context)
