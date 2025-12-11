import os
from time import sleep

flag_bot1 = False
flag_bot2 = False

while 1:
    if(not flag_bot1):
        try:
            os.system('python pasutil1/worker.py')
            flag_bot1 = True
        except:
            print("bot 1 error")
            flag_bot1 = False
            sleep(5)

    if(not flag_bot1):
        try:
            os.system('python pasutil_tgbot/bot.py')
            flag_bot2 = True
        except:
            print("bot 2 error")
            flag_bot2 = False
            sleep(5)
    sleep(5)