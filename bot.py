import os
import requests
from flask import Flask, request

app = Flask(__name__)

# Aapke Credentials
TOKEN = "8952622770:AAEtPR3iUsVpQ9Wi3i6kgcsDn64EOIJQ3zU"
ADMIN_CHAT_ID = "8791893329"
TELEGRAM_INIT_URL = f"https://api.telegram.org/bot{TOKEN}"

AUTHORIZED_DEVICES = {}

@app.route('/')
def home():
    return "😈 M.K HACKER PRO BOT IS ONLINE & RUNNING 🚀"

@app.route(f'/{TOKEN}', methods=['POST'])
def receive_update():
    data = request.get_json()
    if not data:
        return "OK", 200

    if "message" in data:
        message = data["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "").strip()
        user = message.get("from", {})
        username = user.get("username", "Unknown")
        first_name = user.get("first_name", "User")

        if text == "/start":
            welcome_msg = (
                f"😈 <b>𝐌.𝐊 𝐇𝐀𝐂𝐊𝐄𝐑 𝐏𝐑𝐎</b> ☠️\n\n"
                f"✨ <b>𝐖𝐄𝐋𝐂𝐎𝐌𝐄, {first_name}</b> 🖤\n\n"
                f"👑 Welcome to the Official Access System\n\n"
                f"🔐 <b>𝐃𝐄𝐕𝐈𝐂𝐄 𝐕𝐄𝐑𝐈𝐅𝐈𝐂𝐀𝐓𝐈𝐎𝐍</b>\n\n"
                f"💻 Open your script dashboard\n"
                f"📋 Copy your Device ID\n"
                f"📩 Send your Device ID here\n"
                f"⏳ Wait for Admin Approval\n\n"
                f"🎯 <b>𝐘𝐎𝐔𝐑 𝐀𝐂𝐂𝐄𝐒𝐒 𝐒𝐓𝐀𝐑𝐓𝐒 𝐇𝐄𝐑𝐄</b>\n\n"
                f"👨‍💻 <b>𝐃𝐄𝐕𝐄𝐋𝐎𝐏𝐄𝐑:</b> M.K HACKER\n"
                f"📲 <b>𝐒𝐔𝐏𝐏𝐎𝐑𝐓:</b> @MK_HACKER586\n\n"
                f"🖤 <b>𝐏𝐑𝐄𝐂𝐈𝐒𝐈𝐎𝐍 • 𝐒𝐄𝐂𝐔𝐑𝐈𝐓𝐘 • 𝐂𝐎𝐍𝐓𝐑𝐎𝐋</b> 🐺"
            )
            send_message(chat_id, welcome_msg)

        elif text.startswith("MK-") or len(text) > 5:
            device_id = text
            AUTHORIZED_DEVICES[device_id] = {
                "status": "pending",
                "username": username,
                "chat_id": chat_id
            }
            
            user_pending_msg = (
                f"😈 <b>𝐌.𝐊 𝐇𝐀𝐂𝐊𝐄𝐑 𝐏𝐑𝐎</b>\n\n"
                f"✅ <b>𝐑𝐄𝐐𝐔𝐄𝐒𝐓 𝐑𝐄𝐂𝐄𝐈𝐕𝐄𝐃</b>\n\n"
                f"💻 <b>𝐃𝐞𝐯𝐢𝐜𝐞 𝐈𝐃:</b> <code>{device_id}</code>\n\n"
                f"⏳ <b>𝐒𝐭𝐚𝐭𝐮𝐬:</b> 𝐏𝐄𝐍𝐃𝐈𝐍𝐆\n\n"
                f"🛡️ Your access request is awaiting admin review.\n\n"
                f"🔔 You will receive a notification when your request is reviewed.\n\n"
                f"👑 <b>𝐌.𝐊 𝐇𝐀𝐂𝐊𝐄𝐑 𝐒𝐘𝐒𝐓𝐄𝐌</b>"
            )
            send_message(chat_id, user_pending_msg)

            admin_text = (
                f"🚨 <b>𝐍𝐄Ｗ 𝐀𝐂𝐂𝐄𝐒𝐒 𝐑𝐄𝐐𝐔𝐄𝐒𝐓</b>\n\n"
                f"👤 <b>𝐍𝐚𝐦𝐞:</b> {first_name}\n"
                f"📱 <b>𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞:</b> @{username}\n"
                f"🆔 <b>𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 𝐈𝐃:</b> <code>{chat_id}</code>\n\n"
                f"💻 <b>𝐃𝐞𝐯𝐢𝐜𝐞 𝐈𝐃:</b> <code>{device_id}</code>\n\n"
                f"⏳ <b>𝐒𝐭𝐚𝐭𝐮𝐬:</b> 𝐏𝐄𝐍𝐃𝐈𝐍𝐆 𝐑𝐄𝐕𝐈𝐄𝐖\n\n"
                f"👑 <b>𝐀𝐃𝐌𝐈𝐍 𝐀𝐂𝐓𝐈𝐎𝐍 𝐑𝐄𝐐𝐔𝐈𝐑𝐄𝐃</b>\n\n"
                f"⚠️ Please review the request before approving access.\n\n"
                f"😈 <b>𝐌.𝐊 𝐇𝐀𝐂𝐊𝐄𝐑 𝐏𝐑𝐎</b>"
            )
            send_inline_keyboard(chat_id=ADMIN_CHAT_ID, text=admin_text, device_id=device_id)

    elif "callback_query" in data:
        callback = data["callback_query"]
        callback_id = callback["id"]
        chat_id = callback["message"]["chat"]["id"]
        data_val = callback["data"]
        
        parts = data_val.split("_", 1)
        if len(parts) == 2:
            action, device_id = parts

            if action == "approve":
                if device_id in AUTHORIZED_DEVICES:
                    AUTHORIZED_DEVICES[device_id]["status"] = "active"
                else:
                    AUTHORIZED_DEVICES[device_id] = {"status": "active"}
                
                answer_callback(callback_id, "Access Granted Successfully! ✅")
                edit_message_text(chat_id, callback["message"]["message_id"], f"✅ <b>ACCESS APPROVED</b>\n\n💻 Device ID: <code>{device_id}</code>\nStatus: <b>ACTIVE ✓</b>")
                
                user_target_chat = AUTHORIZED_DEVICES[device_id].get("chat_id")
                if user_target_chat:
                    approved_msg = (
                        f"🎉 <b>𝐂𝐎𝐍𝐆𝐑𝐀𝐓𝐔𝐋𝐀𝐓𝐈𝐎𝐍𝐒!</b> 👑\n\n"
                        f"😈 <b>𝐌.𝐊 𝐇𝐀𝐂𝐊𝐄𝐑 𝐏𝐑𝐎</b>\n\n"
                        f"✅ <b>𝐘𝐎𝐔𝐑 𝐀𝐂𝐂𝐄𝐒𝐒 𝐈𝐒 𝐀𝐏𝐏𝐑𝐎𝐕𝐄𝐃</b>\n\n"
                        f"💻 <b>𝐃𝐞𝐯𝐢𝐜𝐞 𝐈𝐃:</b> <code>{device_id}</code>\n\n"
                        f"🟢 <b>𝐒𝐭𝐚𝐭𝐮𝐬:</b> 𝐀𝐂𝐓𝐈𝐕𝐄\n\n"
                        f"🚀 Your device has been authorized. You can now use the features enabled for your account.\n\n"
                        f"📩 <b>𝐒𝐮𝐩𝐩𝐨𝐫𝐭:</b> @MK_HACKER586\n\n"
                        f"🖤 Stay Smart. Stay Secure. 😈"
                    )
                    send_message(user_target_chat, approved_msg)

            elif action == "remove":
                if device_id in AUTHORIZED_DEVICES:
                    AUTHORIZED_DEVICES[device_id]["status"] = "banned"
                
                answer_callback(callback_id, "Access Revoked! ❌")
                edit_message_text(chat_id, callback["message"]["message_id"], f"❌ <b>ACCESS REMOVED / BLOCKED</b>\n\n💻 Device ID: <code>{device_id}</code>\nStatus: <b>LOCKED ❌</b>")

                user_target_chat = AUTHORIZED_DEVICES[device_id].get("chat_id")
                if user_target_chat:
                    revoked_msg = (
                        f"⚠️ <b>𝐀𝐂𝐂𝐄𝐒𝐒 𝐔𝐏𝐃𝐀𝐓𝐄</b>\n\n"
                        f"😈 <b>𝐌.𝐊 𝐇𝐀𝐂𝐊𝐄𝐑 𝐏𝐑𝐎</b>\n\n"
                        f"🔒 Your device access is currently disabled.\n\n"
                        f"💻 <b>𝐃𝐞𝐯𝐢𝐜𝐞 𝐈𝐃:</b> <code>{device_id}</code>\n\n"
                        f"🔴 <b>𝐒𝐭𝐚𝐭𝐮𝐬:</b> 𝐋𝐎𝐂𝐊𝐄𝐃\n\n"
                        f"📩 If you believe this is a mistake, contact support to request a review.\n\n"
                        f"👨‍💻 <b>𝐒𝐔𝐏𝐏𝐎𝐑𝐓:</b> @MK_HACKER586"
                    )
                    send_message(user_target_chat, revoked_msg)

    return "OK", 200

def send_message(chat_id, text):
    url = f"{TELEGRAM_INIT_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    requests.post(url, json=payload)

def send_inline_keyboard(chat_id, text, device_id):
    url = f"{TELEGRAM_INIT_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "reply_markup": {
            "inline_keyboard": [
                [
                    {"text": "✅ APPROVE ACCESS", "callback_data": f"approve_{device_id}"},
                    {"text": "❌ REMOVE ACCESS", "callback_data": f"remove_{device_id}"}
                ]
            ]
        }
    }
    requests.post(url, json=payload)

def edit_message_text(chat_id, message_id, text):
    url = f"{TELEGRAM_INIT_URL}/editMessageText"
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": "HTML"
    }
    requests.post(url, json=payload)

def answer_callback(callback_id, text):
    url = f"{TELEGRAM_INIT_URL}/answerCallbackQuery"
    payload = {
        "callback_query_id": callback_id,
        "text": text,
        "show_alert": True
    }
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
