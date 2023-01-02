import telebot
import json
import requests
from config import *
from apscheduler.schedulers.background import BackgroundScheduler

sched = BackgroundScheduler()
bot = telebot.TeleBot(TOKEN)

def updateList():
    r = requests.get(API).text
    resp = json.loads(r)

    with open ('dota.json', 'w', encoding="utf-8") as f:
        json.dump(resp, f,ensure_ascii=False, indent=4)


    bot.send_message(CHAT_ID, "Таблица обновлена", parse_mode='html')

with open('dota.json', encoding = 'utf8') as text:
        resp = json.load(text, strict=False)['leaderboard']


@bot.message_handler(commands=['top_ten'])
def topten(message):

    ans = "<b><u>Топ 10 Европы:</u></b>\n"

    for id in range(10):
        ans +=f'<b>{resp[id]["rank"]}</b>. {resp[id]["name"]}\n'

    print(message.chat.id)

    bot.send_message(message.chat.id, ans, parse_mode='html')




@bot.message_handler(commands=['list_kg'])
def list(message):


    ans = "<b><u>Топ Кыргызских🇰🇬 дотеров:</u></b>\n"


    for playerRow in resp:

        if (playerRow["name"] in FLAGLESS_GUYS):
                ans +=f'<b>{playerRow["rank"]}</b>. {playerRow["name"]}\n'

        elif ('country' in playerRow):
            if (playerRow['country'] == 'kg'):
                ans +=f'<b>{playerRow["rank"]}</b>. {playerRow["name"]}\n'

    bot.send_message(message.chat.id, ans, parse_mode='html')

sched.add_job(updateList, trigger="cron", hour = 21, minute = 28)
sched.start()
bot.polling(non_stop=True)
