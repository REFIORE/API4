import telegram
import os
from os import listdir
import random
from time import sleep
from dotenv import load_dotenv



def main():
    load_dotenv()
    sleep=14400
    chat_id = os.environ['CHAT_ID']
    tg_token = os.environ['TG_TOKEN']
    bot = telegram.Bot(token=tg_token)
    while True:
        folder='images'
        files=listdir(folder)
        random.shuffle(files)
        for file in files:
            file_path=os.path.join(folder, file)
            with open(file_path, 'rb') as f:
                bot.send_document(chat_id=chat_id, document=f)
            sleep(sleep)


if __name__ == '__main__':
    main()