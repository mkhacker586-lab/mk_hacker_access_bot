import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = "8952622770:AAEtPR3iUsVpQ9Wi3i6kgcsDn64EOIJQ3zU"
ADMIN_CHAT_ID = "8791893329"
TELEGRAM_INIT_URL = f"https://api.telegram.org/bot{TOKEN}"

# In-memory storage for authorized devices
AUTHORIZED_DEVICES = {}

@app.route('/')
def home():
    return "😈☠️ 𝗠.𝗞 𝗛𝗔𝗖𝗞𝗘𝗥 𝗔𝗖𝗖𝗘𝗦𝗦 𝗕𝗢𝗧 𝗢𝗡𝗟𝗜𝗡𝗘 🚀"

@app.route('/check-device', methods=['GET', 'POST'])
def check_device():
    device_id = request.args.get('device_id') or (request.json.get('device_id') if request.is_json else None)
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

        if text == "/start" or text == "🔄 Refresh Panel":
            welcome_msg = (
                f"😈☠️ <b>𝗠.𝗞 H𝗔𝗖𝗞𝗘𝗥 𝗣𝗥𝗢 𝗦𝗖𝗥𝗜𝗣𝗧𝗦</b> ☠️😈\n\n"
                f"✨ <b>WELCOME, {first_name}</b> 🖤\n\n"
                f"👑 Welcome to the Official Script Access & Control System\n\n"
                f"🔐 <b>DEVICE VERIFICATION</b>\n\n"
                f"💻 Open your script dashboard\n"
                f"📋 Copy your Device ID\n"
                f"📩 Send your Device ID here\n"
                f"⏳ Wait for Admin Approval\n\n"
                f"👨‍💻 <b>BRAND:</b> 😈☠️ 𝗠.𝗞 H𝗔𝗖𝗞𝗘𝗥 ☠️😈\n"
                f"📲 <b>SUPPORT:</b> @MK_HACKER586"
            )
            send_reply_keyboard_menu(chat_id, welcome_msg)

        elif text.startswith("MK-") or len(text) > 5:
            device_id = text
            AUTHORIZED_DEVICES[device_id] = {
                "status": "pending",
                "username": username,
                "first_name": first_name,
                "chat_id": chat_id
            }
            
            user_pending_msg = (
                f"😈☠️ <b>𝗠.𝗞 H𝗔𝗖𝗞𝗘𝗥 𝗣𝗥𝗢 𝗦𝗖𝗥𝗜𝗣𝗧𝗦</b> ☠️😈\n\n"
                f"✅ <b>REQUEST RECEIVED</b>\n\n"
                f"💻 <b>Device ID:</b> <code>{device_id}</code>\n\n"
                f"⏳ <b>Status:</b> PENDING\n\n"
                f"🛡️ Awaiting admin review."
            )
            send_message(chat_id, user_pending_msg)

            admin_text = (
                f"🚨 <b>NEW SCRIPT ACCESS REQUEST</b>\n\n"
                f"👤 <b>Name:</b> {first_name}\n"
                f"📱 <b>Username:</b> @{username}\n"
                f"🆔 <b>Telegram ID:</b> <code>{chat_id}</code>\n\n"
                f"💻 <b>Device ID:</b> <code>{device_id}</code>\n\n"
                f"⏳ <b>Status:</b> PENDING REVIEW"
            )
            send_inline_approval(chat_id=ADMIN_CHAT_ID, text=admin_text, device_id=device_id)

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
                    AUTHORIZED_DEVICES[device_id] = {"status": "active", "username": "Unknown", "chat_id": chat_id}
                
                answer_callback(callback_id, "Script Access Granted Successfully! ✅")
                edit_message_text(chat_id, callback["message"]["message_id"], f"✅ <b>SCRIPT APPROVED</b>\n\n💻 Device ID: <code>{device_id}</code>\nStatus: <b>ACTIVE ✓</b>")
                
                user_target_chat = AUTHORIZED_DEVICES[device_id].get("chat_id")
                if user_target_chat:
                    approved_msg = (
                        f"🎉 <b>CONGRATULATIONS!</b> 👑\n\n"
                        f"😈☠️ <b>𝗠.𝗞 H𝗔𝗖𝗞𝗘𝗥 𝗣𝗥𝗢 𝗦𝗖𝗥𝗜𝗣𝗧𝗦</b> ☠️😈\n\n"
                        f"✅ <b>YOUR SCRIPT IS NOW ACTIVE</b>\n\n"
                        f"💻 <b>Device ID:</b> <code>{device_id}</code>\n\n"
                        f"🟢 <b>Status:</b> ACTIVE ✓"
                    )
                    send_message(user_target_chat, approved_msg)

            elif action == "remove":
                if device_id in AUTHORIZED_DEVICES:
                    AUTHORIZED_DEVICES[device_id]["status"] = "banned"
                
                answer_callback(callback_id, "Script Access Revoked! ❌")
                edit_message_text(chat_id, callback["message"]["message_id"], f"❌ <b>SCRIPT REMOVED</b>\n\n💻 Device ID: <code>{device_id}</code>\nStatus: <b>LOCKED ❌</b>")

                user_target_chat = AUTHORIZED_DEVICES[device_id].get("chat_id")
                if user_target_chat:
                    revoked_msg = f"⚠️ <b>ACCESS DISABLED</b>\n\n💻 Device ID: <code>{device_id}</code>"
                    send_message(user_target_chat, revoked_msg)

    return "OK", 200

def send_message(chat_id, text):
    url = f"{TELEGRAM_INIT_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    requests.post(url, json=payload)

def send_reply_keyboard_menu(chat_id, text):
    url = f"{TELEGRAM_INIT_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "reply_markup": {
            "keyboard": [
                [{"text": "💻 Active Scripts"}, {"text": "🛡️ Security Status"}],
                [{"text": "⚡ Device Verifier"}, {"text": "🔥 Access Control"}],
                [{"text": "📋 All Devices List"}, {"text": "👑 Admin Control Panel"}],
                [{"text": "🔄 Refresh Panel"}]
            ],
            "resize_keyboard": True,
            "is_persistent": True
        }
    }
    requests.post(url, json=payload)

def send_inline_approval(chat_id, text, device_id):
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
                ]
            ]
        }
    }
    requests.post(url, json=payload)

def edit_message_text(chat_id, message_id, text):
    url = f"{TELEGRAM_INIT_URL}/editMessageText"
    payload = {"chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": "HTML"}
    requests.post(url, json=payload)

def answer_callback(callback_id, text):
    url = f"{TELEGRAM_INIT_URL}/answerCallbackQuery"
    payload = {"callback_query_id": callback_id, "text": text, "show_alert": True}
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
