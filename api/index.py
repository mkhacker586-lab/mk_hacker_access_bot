import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = "8952622770:AAEtPR3iUsVpQ9Wi3i6kgcsDn64EOIJQ3zU"
ADMIN_CHAT_ID = "8791893329"
TELEGRAM_INIT_URL = f"https://api.telegram.org/bot{TOKEN}"

# Database storage for devices
AUTHORIZED_DEVICES = {}

@app.route('/')
def home():
    return "😈☠️ 𝐌.𝐊 𝐇𝐀𝐂𝐊𝐄𝐑 𝐏𝐑𝐎 𝐒𝐂𝐑𝐈𝐏𝐓𝐒 ☠️😈 - ONLINE & ACTIVE 🚀"

# Script dashboard ke liye verification endpoint
@app.route('/check-device', methods=['GET', 'POST'])
def check_device():
    device_id = request.args.get('device_id') or request.json.get('device_id') if request.is_json else None
    if not device_id and request.method == 'POST':
        device_id = request.form.get('device_id')
    
    if not device_id:
        return jsonify({"status": "error", "message": "Device ID missing"})
    
    if device_id in AUTHORIZED_DEVICES and AUTHORIZED_DEVICES[device_id]["status"] == "active":
        return jsonify({"status": "active", "message": "Device is Authorized ✓"})
    else:
        return jsonify({"status": "locked", "message": "Device Not Authorized ❌"})

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
                f"😈☠️ <b>𝐌.𝐊 𝐇𝐀𝐂𝐊𝐄𝐑 𝐏𝐑𝐎 𝐒𝐂𝐑𝐈𝐏𝐓𝐒</b> ☠️😈\n\n"
                f"✨ <b>𝐖𝐄𝐋𝐂𝐎𝐌𝐄, {first_name}</b> 🖤\n\n"
                f"👑 Welcome to the Official Access & Control System\n\n"
                f"🔐 <b>𝐃𝐄𝐕𝐈𝐂𝐄 𝐕𝐄𝐑𝐈𝐅𝐈𝐂𝐀𝐓𝐈𝐎𝐍</b>\n\n"
                f"💻 Open your script dashboard\n"
                f"📋 Copy your Device ID\n"
                f"📩 Send your Device ID here\n"
                f"⏳ Wait for Admin Approval\n\n"
                f"🎯 <b>𝐘𝐎𝐔𝐑 𝐀𝐂𝐂𝐄𝐒𝐒 𝐒𝐓𝐀𝐑𝐓𝐒 𝐇𝐄𝐑𝐄</b>\n\n"
                f"👨‍💻 <b>𝐁𝐑𝐀𝐍𝐃:</b> 😈☠️ 𝐌.𝗞 𝐇𝐀𝐂𝐊𝐄𝐑 ☠️😈\n"
                f"📲 <b>𝐒𝐔𝐏𝐏𝐎𝐑𝐓:</b> @MK_HACKER586\n\n"
                f"🖤 <b>𝐏𝐑𝐄𝐂𝐈𝐒𝐈𝐎𝐍 • 𝐒𝐄𝐂𝐔𝐑𝐈𝐓𝐘 • 𝐂𝐎𝐍𝐓𝐑𝐎𝐋</b> 🐺"
            )
            send_message(chat_id, welcome_msg)

        elif text == "/list" and str(chat_id) == str(ADMIN_CHAT_ID):
            send_devices_list_panel(chat_id)

        elif text.startswith("MK-") or len(text) > 5:
            device_id = text
            AUTHORIZED_DEVICES[device_id] = {
                "status": "pending",
                "username": username,
                "first_name": first_name,
                "chat_id": chat_id
            }
            
            user_pending_msg = (
                f"😈☠️ <b>𝐌.𝐊 𝐇𝐀𝐂𝐊𝐄𝐑 𝐏𝐑𝐎 𝐒𝐂𝐑𝐈𝐏𝐓𝐒</b> ☠️😈\n\n"
                f"✅ <b>𝐑𝐄𝐐𝐔𝐄𝐒𝐓 𝐑𝐄𝐂𝐄𝐈𝐕𝐄𝐃</b>\n\n"
                f"💻 <b>𝐃𝐞𝐯𝐢𝐜𝐞 𝐈𝐃:</b> <code>{device_id}</code>\n\n"
                f"⏳ <b>𝐒𝐭𝐚𝐭𝐮𝐬:</b> 𝐏𝐄𝐍𝐃𝐈𝐍𝐆\n\n"
                f"🛡️ Your access request is awaiting admin review.\n\n"
                f"👑 <b>𝐁𝐑𝐀𝐍𝐃:</b> 😈☠️ 𝐌.𝗞 𝐇𝐀𝐂𝐊𝐄𝐑 ☠️😈"
            )
            send_message(chat_id, user_pending_msg)

            admin_text = (
                f"🚨 <b>𝐍𝐄𝐖 𝐒𝐂𝐑𝐈𝐏𝐓 𝐀𝐂𝐂𝐄𝐒𝐒 𝐑𝐄𝐐𝐔𝐄𝐒𝐓</b>\n\n"
                f"👤 <b>𝐍𝐚𝐦𝐞:</b> {first_name}\n"
                f"📱 <b>𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞:</b> @{username}\n"
                f"🆔 <b>𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 𝐈𝐃:</b> <code>{chat_id}</code>\n\n"
                f"💻 <b>𝐃𝐞𝐯𝐢𝐜𝐞 𝐈𝐃:</b> <code>{device_id}</code>\n\n"
                f"⏳ <b>𝐒𝐭𝐚𝐭𝐮𝐬:</b> 𝐏𝐄𝐍𝐃𝐈𝐍𝐆 𝐑𝐄𝐕𝐈𝐄𝐖\n\n"
                f"👑 <b>𝐁𝐑𝐀𝐍𝐃:</b> 😈☠️ 𝐌.𝗞 𝐇𝐀𝐂𝐊𝐄𝐑 ☠️😈"
            )
            send_inline_keyboard(chat_id=ADMIN_CHAT_ID, text=admin_text, device_id=device_id)

    elif "callback_query" in data:
        callback = data["callback_query"]
        callback_id = callback["id"]
        chat_id = callback["message"]["chat"]["id"]
        data_val = callback["data"]
        
        if data_val == "show_list":
            answer_callback(callback_id, "Loading Active Devices List...")
            send_devices_list_panel(chat_id, callback["message"]["message_id"])
            return "OK", 200

        parts = data_val.split("_", 1)
        if len(parts) == 2:
            action, device_id = parts

            if action == "approve":
                if device_id in AUTHORIZED_DEVICES:
                    AUTHORIZED_DEVICES[device_id]["status"] = "active"
                else:
                    AUTHORIZED_DEVICES[device_id] = {"status": "active", "username": "Unknown", "chat_id": chat_id}
                
                answer_callback(callback_id, "Script Access Granted Successfully! ✅")
                edit_message_text(chat_id, callback["message"]["message_id"], f"✅ <b>SCRIPT ACCESS APPROVED</b>\n\n💻 Device ID: <code>{device_id}</code>\nStatus: <b>ACTIVE ✓</b>\n👑 <b>BRAND:</b> 😈☠️ 𝐌.𝗞 𝐇𝗔𝐂𝐊𝐄𝐑 ☠️😈")
                
                user_target_chat = AUTHORIZED_DEVICES[device_id].get("chat_id")
                if user_target_chat:
                    approved_msg = (
                        f"🎉 <b>𝐂𝐎𝐍𝐆𝐑𝐀𝐓𝐔𝐋𝐀𝐓𝐈𝐎𝐍𝐒!</b> 👑\n\n"
                        f"😈☠️ <b>𝐌.𝐊 𝐇𝐀𝐂𝐊𝐄𝐑 𝐏𝐑𝐎 𝐒𝐂𝐑𝐈𝐏𝐓𝐒</b> ☠️😈\n\n"
                        f"✅ <b>𝐘𝐎𝐔𝐑 𝐒𝐂𝐑𝐈𝐏𝐓 𝐈𝐒 𝐍𝐎𝐖 𝐀𝐂𝐓𝐈𝐕𝐄</b>\n\n"
                        f"💻 <b>𝐃𝐞𝐯𝐢𝐜𝐞 𝐈𝐃:</b> <code>{device_id}</code>\n\n"
                        f"🟢 <b>𝐒𝐭𝐚𝐭𝐮𝐬:</b> 𝐀𝐂𝐓𝐈𝐕𝐄 ✓\n\n"
                        f"🚀 You can now access and run all features seamlessly.\n\n"
                        f"📩 <b>𝐒𝐔𝐏𝐏𝐎𝐑𝐓:</b> @MK_HACKER586\n\n"
                        f"🖤 <b>𝐏𝐑𝐄𝐂𝐈𝐒𝐈𝐎𝐍 • 𝐒𝐄𝐂𝐔𝐑𝐈𝐓𝐘 • 𝐂𝐎𝐍𝐓𝐑𝐎𝐋</b>"
                    )
                    send_message(user_target_chat, approved_msg)

            elif action == "remove":
                if device_id in AUTHORIZED_DEVICES:
                    AUTHORIZED_DEVICES[device_id]["status"] = "banned"
                
                answer_callback(callback_id, "Script Access Revoked! ❌")
                edit_message_text(chat_id, callback["message"]["message_id"], f"❌ <b>SCRIPT ACCESS REMOVED</b>\n\n💻 Device ID: <code>{device_id}</code>\nStatus: <b>LOCKED ❌</b>\n👑 <b>BRAND:</b> 😈☠️ 𝐌.𝐊 𝐇𝐀𝐂𝐊𝐄𝐑 ☠️😈")

                user_target_chat = AUTHORIZED_DEVICES[device_id].get("chat_id")
                if user_target_chat:
                    revoked_msg = (
                        f"⚠️ <b>𝐀𝐂𝐂𝐄𝐒𝐒 𝐔𝐏𝐃𝐀𝐓𝐄</b>\n\n"
                        f"😈☠️ <b>𝐌.𝐊 𝐇𝐀𝐂𝐊𝐄𝐑 𝐏𝐑𝐎 𝐒𝐂𝐑𝐈𝐏𝐓𝐒</b> ☠️😈\n\n"
                        f"🔒 Your script access has been disabled by admin.\n\n"
                        f"💻 <b>𝐃𝐞𝐯𝐢𝐜𝐞 𝐈𝐃:</b> <code>{device_id}</code>\n\n"
                        f"🔴 <b>𝐒𝐭𝐚𝐭𝐮𝐬:</b> 𝐋𝐎𝐂𝐊𝐄𝐃 ❌\n\n"
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
                    {"text": "✅ APPROVE SCRIPT", "callback_data": f"approve_{device_id}"},
                    {"text": "❌ REMOVE SCRIPT", "callback_data": f"remove_{device_id}"}
                ],
                [
                    {"text": "📋 VIEW ALL LIST", "callback_data": "show_list"}
                ]
            ]
        }
    }
    requests.post(url, json=payload)

def send_devices_list_panel(chat_id, message_id=None):
    if not AUTHORIZED_DEVICES:
        text = "⚠️ <b>No devices registered in system yet.</b>"
        keyboard = []
    else:
        text = "📋 <b>😈☠️ 𝐌.𝐊 𝐇𝐀𝐂𝐊𝐄𝐑 𝐏𝐑𝐎 𝐒𝐂𝐑𝐈𝐏𝐓𝐒 𝐋𝐈𝐒𝐓 ☠️😈</b>\n\nSelect a device to remove or manage:"
        keyboard = []
        for dev_id, info in AUTHORIZED_DEVICES.items():
            status_icon = "🟢" if info['status'] == "active" else "🔴"
            button_text = f"{status_icon} {dev_id} (@{info['username']})"
            keyboard.append([{"text": button_text, "callback_data": f"remove_{dev_id}"}])
    
    keyboard.append([{"text": "🔄 REFRESH LIST", "callback_data": "show_list"}])
    
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "reply_markup": {"inline_keyboard": keyboard}
    }
    
    if message_id:
        payload["message_id"] = message_id
        url = f"{TELEGRAM_INIT_URL}/editMessageText"
        requests.post(url, json=payload)
    else:
        url = f"{TELEGRAM_INIT_URL}/sendMessage"
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
