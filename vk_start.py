import os
from random import randint
from requests import *
import vk
from auth import VK_API_ACCESS_TOKEN, VK_API_VERSION, GROUP_ID

session = vk.Session(access_token = VK_API_ACCESS_TOKEN)
api = vk.API(session, v = VK_API_VERSION)

longPoll = api.groups.getLongPollServer(group_id = GROUP_ID)
server, key, ts = longPoll['server'], longPoll['key'], longPoll['ts']

while True:
    longPoll = post('%s'%server, data = {'act': 'a_check',
                                         'key': key,
                                         'ts': ts,
                                         'wait': 25}).json()


    if longPoll['updates'] and len(longPoll['updates']) != 0:
        for update in longPoll['updates']:
            if update['type'] == 'message_new':
                print(update)
                api.messages.markAsRead(peer_id = update['object']['from_id'])

                name = api.users.get(user_ids = update['object']['from_id'])[0]['first_name']

                pfile = post(api.photos.getMessagesUploadServer(peer_id = update['object']['from_id'])['upload_url'], files = {'photo': open('python.jpg', 'rb')}).json()
                photo = api.photos.saveMessagesPhoto(server = pfile['server'], photo = pfile['photo'], hash = pfile['hash'])[0]

                api.messages.send(user_id = update['object']['from_id'], random_id = randint(-2147483648, 2147483647), message = 'Привет, %s &#128521;'%name)


    ts = longPoll['ts']
