import telegram
import os
import argparse
from os import listdir
import random
from time import sleep


tg_token = os.environ['TOKEN']

bot = telegram.Bot(token=tg_token)

while True:
    folder='images'
    files=listdir(folder)
    random.shuffle(files)
    for file in files:
        file_path=os.path.join(folder, file)
        with open(file_path, 'rb') as f:
            bot.send_document(chat_id='@NASAImagesbot', document=f)
        sleep(14400)