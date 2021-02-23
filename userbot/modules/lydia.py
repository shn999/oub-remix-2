# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
# credit goes to @snapdragon and @devpatel_73 for making it work on this userbot.

#   Copyright 2019 - 2020-2021 DarkPrinc3

#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at

#       http://www.apache.org/licenses/LICENSE-2.0

#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


from coffeehouse.lydia import LydiaAI
from coffeehouse.api import API
import asyncio
from telethon import events
import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

import coffeehouse as cf

import asyncio
import io
from userbot.modules.sql_helper.lydia_sql import get_s, get_all_s, add_s, remove_s
from time import time
import coffeehouse
from userbot import LYDIA_API_KEY
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, bot
from userbot.events import register
from telethon import events
from coffeehouse.lydia import LydiaAI
from coffeehouse.api import API


# Non-SQL Mode
ACC_LYDIA = {}
SESSION_ID = {}

if LYDIA_API_KEY:
    api_key = LYDIA_API_KEY
    api_client = API(api_key)
    lydia = LydiaAI(api_client)

@register(outgoing=True, pattern="^.rlda$")
async def rlda(event):
    if event.fwd_from:
        return
    await event.edit("Processing...")
    try:
        session = lydia.create_session()
        session_id = session.id
        reply = await event.get_reply_message()
        msg = reply.text
        text_rep = session.think_thought((session_id, msg))
        await event.edit("**Hiii**: {0}".format(text_rep))
    except Exception as e:
        await event.edit(str(e))

@register(outgoing=True, pattern="^.elda$")
async def elda(event):
    if event.fwd_from:
        return
    await event.edit("Running on Non-SQL mode for now...")
    await asyncio.sleep(3)
    await event.edit("Processing...")
    reply_msg = await event.get_reply_message()
    if reply_msg:
        session = lydia.create_session()
        session_id = session.id
        if reply_msg.sender_id is None:
            return await event.edit("Invalid user type.")
        ACC_LYDIA.update({str(event.chat_id) + " " + str(reply_msg.sender_id): session})
        SESSION_ID.update(
            {str(event.chat_id) + " " + str(reply_msg.sender_id): session_id}
        )
        await event.edit(
            "EDITH successfully (re)enabled for user: {} in chat: {}".format(
                str(reply_msg.sender_id), str(event.chat_id)
            )
        )
    else:
        await event.edit("Reply to a user to activate EDITH AI on them")

@register(outgoing=True, pattern="^.dlda$")
async def dlda(event):
    if event.fwd_from:
        return
    await event.edit("Running on Non-SQL mode for now...")
    await asyncio.sleep(3)
    await event.edit("Processing...")
    reply_msg = await event.get_reply_message()
    try:
        del ACC_LYDIA[str(event.chat_id) + " " + str(reply_msg.sender_id)]
        del SESSION_ID[str(event.chat_id) + " " + str(reply_msg.sender_id)]
        await event.edit(
            "EDITH successfully disabled for user: {} in chat: {}".format(
                str(reply_msg.sender_id), str(event.chat_id)
            )
        )
    except Exception:
        await event.edit("This person does not have EDITH AI activated on him/her.")


@register(incoming=True, disable_edited=True)
async def user(event):
    user_text = event.text
    try:
        session = ACC_LYDIA[str(event.chat_id) + " " + str(event.sender_id)]
        session_id = SESSION_ID[str(event.chat_id) + " " + str(event.sender_id)]
        msg = event.text
        async with event.client.action(event.chat_id, "typing"):
            text_rep = session.think_thought((session_id, msg))
            wait_time = 0
            for i in range(len(text_rep)):
                wait_time = wait_time + 0.1
            await asyncio.sleep(wait_time)
            await event.reply(text_rep)
    except (KeyError, TypeError):
        return

      
CMD_HELP.update({
    "lydia":
    ".elda <username/reply>\
\nUsage: add's lydia auto chat request in the chat.\
\n\n.dlda <username/reply>\
\nUsage: remove's lydia auto chat request in the chat.\
\n\n.rlda <username/reply>\
\nUsage: starts lydia repling to perticular person in the chat.\
\n Note:  get your value from https://coffeehouse.intellivoid.net."
})
