import io
import sys
import requests

from origamibot import OrigamiBot as Bot
from origamibot.listener import Listener

from image import process_img


def get_img_file(bot_token: str, file_id: str) -> io.BytesIO:
    url = f'https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}'
    response = requests.get(url)
    file_path = response.json()['result']['file_path']

    file_url = f'https://api.telegram.org/file/bot{bot_token}/{file_path}'
    response = requests.get(file_url)
    return response.content


class BotsCommands:
    def __init__(self, bot: Bot):
        self._bot = bot

    def start(self, message):
        self._bot.send_message(
            message.chat.id,
            'mam (iMAge Manipultaion) - бот для наложения фильтров на '
            'изображения. Для начала работы бота отправьте ему изображение, '
            'после этого вы получите его обработанную версию.'
        )


class MessageListener(Listener):
    def __init__(self, bot):
        self._bot = bot

    def on_message(self, message):
        if message.photo:
            img_bytes = get_img_file(self._bot.token, message.photo[-1].file_id)
            img_bytes = process_img(img_bytes)
            self._bot.send_photo(message.chat.id, img_bytes)

    def on_command_failure(self, message, err=None):
        if err is None:
            self._bot.send_message(
                message.chat.id,
                'Command failed to bind arguments!'
            )
        else:
            self._bot.send_message(
                message.chat.id,
                f'Error in command:\n{err}'
            )


if __name__ == '__main__':
    token = (sys.argv[1] if len(sys.argv) > 1 else input('Enter bot token: '))
    bot = Bot(token)
    bot.add_listener(MessageListener(bot))
    bot.add_commands(BotsCommands(bot))
    bot.start()
    while True:
        pass
