import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

import telebot
import threading

bot = telebot.TeleBot('')

vk_session = vk_api.VkApi(token="");
session_api = vk_session.get_api()
chat_id=153
user_id=215439475

current_message_id = 0

stop_words = ['арарат', 'проверяют', 'комендант', 'коменда', 'заведующая', 'оксана', 'проверяет']

def getLastMessages():
    lastMessage = session_api.messages.getHistory(count=5, peer_id=2000000000+chat_id, user_id=user_id)
    history = lastMessage['items']

    global current_message_id
    for message in history:
        
        if current_message_id >= int(message['conversation_message_id']):
            break
        current_message_id = int(message['conversation_message_id'])

        text = str(message['text'])

        for word in stop_words:
            if text.count(word) > 0:
                return "Идет проверка на чистоту!"

    return ""


users_involved = set()


def f():
  threading.Timer(1.0, f).start()  # Перезапуск через 5 секунд
  i = getLastMessages()
  if i != "" :
    global users_involved
    for id in users_involved :
        bot.send_message(id, i);

f()


@bot.message_handler(content_types=['text'])
def start(message):
    global users_involved
    if message.text == '/start':
        users_involved.add(message.from_user.id)
        bot.send_message(message.from_user.id, "Оповещения включены");
    else:
        users_involved.remove(message.from_user.id)
        bot.send_message(message.from_user.id, 'Оповещения отключены');



bot.polling(none_stop=True, interval=0)
