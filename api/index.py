import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = "8952622770:AAEtPR3iUsVpQ9Wi3i6kgcsDn64EOIJQ3zU"
ADMIN_CHAT_ID = "8791893329"
TELEGRAM_INIT_URL = f"https://api.telegram.org/bot{TOKEN}"

AUTHORIZED_DEVICES = {}

@app.route('/')
def home():
    return "😈☠️ 𝗠.𝗞 𝗛𝗔𝗖𝗞𝗘𝗥 𝗣𝗥𝗢 𝗦𝗖𝗥𝗜𝗣𝗧𝗦 ☠️😈 - CONTROL SYSTEM ONLINE 🚀"

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
                f"😈☠️ 𝗠.𝗞 𝗛𝗔𝗖𝗞𝗘𝗥 𝗣𝗥𝗢 𝗦𝗖𝗥𝗜𝗣𝗧𝗦 ☠️😈\n\n"
                f"✨ WELCOME, {first_name} 🖤\n\n"
                f"👑 Welcome to the Official Script Access & Control Panel\n\n"
                f"🔐 DEVICE VERIFICATION SYSTEM\n\n"
                f"💻 Open your script dashboard\n"
                f"📋 Copy your Device ID\n"
                f"📩 Send your Device ID here\n"
                f"⏳ Wait for Admin Approval\n\n"
                f"🎯 YOUR ACCESS STARTS HERE\n\n"
                f"👨‍💻 BRAND: 😈☠️ 𝗠.𝗞 𝗛𝗔𝗖𝗞𝗘𝗥 ☠️😈\n"
                f"📲 SUPPORT: @MK_HACKER586\n\n"
                f"🖤 PRECISION • SECURITY • CONTROL 🐺"
            )
            send_main_control_menu(chat_id, welcome_msg)

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
                f"😈☠️ 𝗠.𝗞 𝗛𝗔𝗖𝗞𝗘𝗥 𝗣𝗥𝗢 𝗦𝗖𝗥𝗜𝗣𝗧𝗦 ☠️😈\n\n"
                f"✅ REQUEST RECEIVED\n\n"
                f"💻 Device ID: {device_id}\n\n"
                f"⏳ Status: PENDING\n\n"
                f"🛡️ Your access request is awaiting admin review.\n\n"
                f"👑 BRAND: 😈☠️ 𝗠.𝗞 𝗛𝗔𝗖𝗞𝗘𝗥 ☠️😈"
            )
            send_message(chat_id, user_pending_msg)

            admin_text = (
                f"🚨 NEW SCRIPT ACCESS REQUEST\n\n"
                f"👤 Name: {first_name}\n"
                f"📱 Username: @{username}\n"
                f"🆔 Telegram ID: {chat_id}\n\n"
                f"💻 Device ID: {device_id}\n\n"
                f"⏳ Status: PENDING REVIEW\n\n"
                f"👑 BRAND: 😈☠️ 𝗠.𝗞 𝗛𝗔𝗖𝗞𝗘𝗥 ☠️😈"
            )
            send_admin_approval_keyboard(chat_id=ADMIN_CHAT_ID, text=admin_text, device_id=device_id)

    elif "callback_query" in data:
        callback = data["callback_query"]
        callback_id = callback["id"]
        chat_id = callback["message"]["chat"]["id"]
        data_val = callback["data"]
        
        if data_val == "show_list":
            answer_callback(callback_id, "Loading All Registered Devices...")
            send_devices_list_panel(chat_id, callback["message"]["message_id"])
            return "OK", 200
        elif data_val == "menu_info":
            answer_callback(callback_id, "Send your Device ID in chat to request access.")
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
                edit_message_text(chat_id, callback["message"]["message_id"], f"✅ SCRIPT ACCESS APPROVED\n\n💻 Device ID: {device_id}\nStatus: ACTIVE ✓\n👑 BRAND: 😈☠️ 𝗠.𝗞 𝗛𝗔𝗖𝗞𝗘𝗥 ☠️😈")
                
                user_target_chat = AUTHORIZED_DEVICES[device_id].get("chat_id")
                if user_target_chat:
                    approved_msg = (
                        f"🎉 CONGRATULATIONS! 👑\n\n"
                        f"😈☠️ 𝗠.𝗞 𝗛𝗔𝗖𝗞𝗘𝗥 𝗣𝗥𝗢 𝗦𝗖𝗥𝗜𝗣𝗧𝗦 ☠️😈\n\n"
                        f"✅ YOUR SCRIPT IS NOW ACTIVE\n\n"
                        f"💻 Device ID: {device_id}\n\n"
                        f"🟢 Status: ACTIVE ✓\n\n"
                        f"🚀 Your device is fully authorized and running.\n\n"
                        f"📩 SUPPORT: @MK_HACKER586\n\n"
                        f"🖤 PRECISION • SECURITY • CONTROL"
                    )
                    send_message(user_target_chat, approved_msg)

            elif action == "remove":
                if device_id in AUTHORIZED_DEVICES:
                    AUTHORIZED_DEVICES[device_id]["status"] = "banned"
                
                answer_callback(callback_id, "Script Access Revoked! ❌")
                edit_message_text(chat_id, callback["message"]["message_id"], f"❌ SCRIPT ACCESS REMOVED\n\n💻 Device ID: {device_id}\nStatus: LOCKED ❌\n👑 BRAND: 😈☠️ 𝗠.𝗞 𝗛𝗔𝗖𝗞𝗘𝗥 ☠️😈")

                user_target_chat = AUTHORIZED_DEVICES[device_id].get("chat_id")
                if user_target_chat:
                    revoked_msg = (
                        f"⚠️ ACCESS UPDATE\n\n"
                        f"😈☠️ 𝗠.𝗞 𝗛𝗔𝗖𝗞𝗘𝗥 𝗣𝗥𝗢 𝗦𝗖𝗥𝗜𝗣𝗧𝗦 ☠️😈\n\n"
                        f"🔒 Your script access has been disabled by admin.\n\n"
                        f"💻 Device ID: {device_id}\n\n"
                        f"🔴 Status: LOCKED ❌\n\n"
                        f"👨‍💻 SUPPORT: @MK_HACKER586"
                    )
                    send_message(user_target_chat, revoked_msg)

    return "OK", 200

def send_message(chat_id, text):
    url = f"{TELEGRAM_INIT_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

def send_main_control_menu(chat_id, text):
    url = f"{TELEGRAM_INIT_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "reply_markup": {
            "inline_keyboard": [
                [
                    {"text": "💻 Script Access Status", "callback_data": "menu_info"},
                    {"text": "🛡️ Security Shield", "callback_data": "menu_info"}
                ],
                [
                    {"text": "⚡ Device ID Verifier", "callback_data": "menu_info"},
                    {"text": "🔥 Access Manager", "callback_data": "menu_info"}
                ],
                [
                    {"text": "📋 All Devices List", "callback_data": "show_list"},
                    {"text": "👑 Admin Control Panel", "callback_data": "show_list"}
                ]
            ]
        }
    }
    requests.post(url, json=payload)

def send_admin_approval_keyboard(chat_id, text, device_id):
    url = f"{TELEGRAM_INIT_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
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
        text = "⚠️ No devices registered in the system yet."
        keyboard = [[{"text": "🔄 REFRESH LIST", "callback_data": "show_list"}]]
    else:
        text = "📋 😈☠️ 𝗠.𝗞 𝗛𝗔𝗖𝗞𝗘𝗥 𝗣𝗥𝗢 𝗦𝗖𝗥𝗜𝗣𝗧𝗦 ☠️😈\n\nSelect any device below to view details or remove access:"
        keyboard = []
        for dev_id, info in AUTHORIZED_DEVICES.items():
            status_icon = "🟢" if info['status'] == "active" else "🔴"
            button_text = f"{status_icon} {dev_id} (@{info['username']})"
            keyboard.append([{"text": button_text, "callback_data": f"remove_{dev_id}"}])
        keyboard.append([{"text": "🔄 REFRESH LIST", "callback_data": "show_list"}])
    
    payload = {
        "chat_id": chat_id,
        "text": text,
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
        "text": text
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
