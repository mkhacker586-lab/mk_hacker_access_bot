import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = "8952622770:AAGjVz5WoH0HG_fArmdHktI1yUZy6yiw6mQ"
ADMIN_CHAT_ID = "8791893329"
TELEGRAM_INIT_URL = f"https://api.telegram.org/bot{TOKEN}"

# System Database Memory / State Storage
AUTHORIZED_DEVICES = {}
USERS_DB = {}
ACTIVITY_LOGS = []

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/', methods=['GET'])
def home():
    return "😈☠️ 𝗠.𝗞 𝗛𝗔𝗖𝗞𝗘𝗥 𝗣𝗥𝗢 𝗦𝗖𝗥𝗜𝗣𝗧𝗦 ☠️😈 - PROFESSIONAL SYSTEM ONLINE 🚀"

@app.route('/check-device', methods=['GET', 'POST', 'OPTIONS'])
def check_device():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
        
    device_id = request.args.get('device_id') or (request.json.get('device_id') if request.is_json else None)
    if not device_id and request.method == 'POST':
        device_id = request.form.get('device_id')
    
    if not device_id:
        return jsonify({"status": "error", "message": "Device ID missing"})
    
    if device_id in AUTHORIZED_DEVICES and AUTHORIZED_DEVICES[device_id]["status"] == "active":
        return jsonify({"status": "active", "message": "Device is Authorized ✓"})
    else:
        return jsonify({"status": "locked", "message": "Device Not Authorized ❌"})

@app.route(f'/{TOKEN}', methods=['POST', 'GET'])
def receive_update():
    if request.method == 'GET':
        return "Bot system active!", 200
        
    data = request.get_json(silent=True)
    if not data:
        return "OK", 200

    if "message" in data:
        message = data["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "").strip()
        user = message.get("from", {})
        username = user.get("username", "Unknown")
        first_name = user.get("first_name", "User")

        # Register User Session
        USERS_DB[chat_id] = {"username": username, "first_name": first_name, "status": "active"}

        if text == "/start" or text == "🔄 Refresh Panel":
            welcome_msg = (
                f"😈☠️ <b>𝗠.𝗞 𝗛𝗔𝗖𝗞𝗘𝗥 𝗣𝗥𝗢 𝗦𝗖𝗥𝗜𝗣𝗧𝗦</b> ☠️😈\n\n"
                f"✨ <b>WELCOME, {first_name}</b> 🖤\n\n"
                f"👑 Official Script Access & Control System\n\n"
                f"🔐 <b>DEVICE VERIFICATION</b>\n"
                f"💻 Copy your Device ID from script dashboard\n"
                f"📩 Send your Device ID here to request access\n\n"
                f"👨‍💻 <b>BRAND:</b> 😈☠️ 𝗠.𝗞 𝗛𝗔𝗖𝗞𝗘𝗥 ☠️😈"
            )
            send_user_menu(chat_id, welcome_msg)

        elif text == "🌐 OPEN SCRIPTS WEBSITE":
            send_message(chat_id, "🚀 <b>Official Dashboard:</b> https://mkhackerproscripts.vercel.app")

        elif text == "🔍 CHECK MY ACCESS" or text == "📂 MY AUTHORIZED SCRIPTS":
            send_message(chat_id, "🛡️ <b>Security Status:</b> Check your script dashboard for live authorization status.")

        elif text == "📱 MY REGISTERED DEVICES":
            send_message(chat_id, f"📱 <b>Your Telegram ID:</b> <code>{chat_id}</code>\n👤 <b>Username:</b> @{username}")

        elif text == "📩 REQUEST VERIFICATION" or text == "📞 CONTACT SUPPORT":
            send_message(chat_id, "📲 <b>Official Support / Admin:</b> @MK_HACKER586")

        elif text == "👑 Admin Control Panel" and str(chat_id) == str(ADMIN_CHAT_ID):
            send_admin_dashboard(chat_id)

        elif text.startswith("MK-") or len(text) > 5:
            device_id = text
            AUTHORIZED_DEVICES[device_id] = {
                "status": "pending",
                "username": username,
                "first_name": first_name,
                "chat_id": chat_id
            }
            ACTIVITY_LOGS.append(f"New Device ID submitted: {device_id} by @{username}")
            
            user_pending_msg = (
                f"😈☠️ <b>𝗠.𝗞 𝗛𝗔𝗖𝗞𝗘𝗥 𝗣𝗥𝗢 𝗦𝗖𝗥𝗜𝗣𝗧𝗦</b> ☠️😈\n\n"
                f"✅ <b>REQUEST RECEIVED</b>\n\n"
                f"💻 <b>Device ID:</b> <code>{device_id}</code>\n\n"
                f"⏳ <b>Status:</b> PENDING REVIEW\n"
                f"🛡️ Awaiting admin approval."
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
        
        if data_val == "admin_dashboard" and str(chat_id) == str(ADMIN_CHAT_ID):
            answer_callback(callback_id, "Dashboard Loaded Successfully!")
            send_admin_dashboard(chat_id)
            return "OK", 200
            
        elif data_val == "admin_users" and str(chat_id) == str(ADMIN_CHAT_ID):
            user_list_text = f"👥 <b>Total Registered Users:</b> {len(USERS_DB)}\n"
            for uid, uinfo in USERS_DB.items():
                user_list_text += f"• ID: <code>{uid}</code> | @{uinfo['username']}\n"
            answer_callback(callback_id, "Users List Fetched")
            send_message(chat_id, user_list_text)
            return "OK", 200

        parts = data_val.split("_", 1)
        if len(parts) == 2:
            action, device_id = parts

            if action == "approve":
                if device_id in AUTHORIZED_DEVICES:
                    AUTHORIZED_DEVICES[device_id]["status"] = "active"
                else:
                    AUTHORIZED_DEVICES[device_id] = {"status": "active", "username": "Unknown", "chat_id": chat_id}
                
                answer_callback(callback_id, "Script Access Granted! ✅")
                edit_message_text(chat_id, callback["message"]["message_id"], f"✅ <b>APPROVED</b>\n\n💻 Device ID: <code>{device_id}</code>\nStatus: <b>ACTIVE ✓</b>")
                
                user_target_chat = AUTHORIZED_DEVICES[device_id].get("chat_id")
                if user_target_chat:
                    approved_msg = (
                        f"🎉 <b>CONGRATULATIONS!</b> 👑\n\n"
                        f"😈☠️ <b>𝗠.𝗞 𝗛𝗔𝗖𝗞𝗘𝗥 𝗣𝗥𝗢 𝗦𝗖𝗥𝗜𝗣𝗧𝗦</b> ☠️😈\n\n"
                        f"✅ <b>YOUR SCRIPT IS NOW ACTIVE</b>\n\n"
                        f"💻 <b>Device ID:</b> <code>{device_id}</code>\n\n"
                        f"🟢 <b>Status:</b> ACTIVE ✓"
                    )
                    send_message(user_target_chat, approved_msg)

            elif action == "remove":
                if device_id in AUTHORIZED_DEVICES:
                    AUTHORIZED_DEVICES[device_id]["status"] = "banned"
                
                answer_callback(callback_id, "Access Revoked! ❌")
                edit_message_text(chat_id, callback["message"]["message_id"], f"❌ <b>REMOVED</b>\n\n💻 Device ID: <code>{device_id}</code>\nStatus: <b>LOCKED ❌</b>")

                user_target_chat = AUTHORIZED_DEVICES[device_id].get("chat_id")
                if user_target_chat:
                    revoked_msg = f"⚠️ <b>ACCESS DISABLED BY ADMIN</b>\n\n💻 Device ID: <code>{device_id}</code>"
                    send_message(user_target_chat, revoked_msg)

    return "OK", 200

def send_message(chat_id, text):
    url = f"{TELEGRAM_INIT_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    requests.post(url, json=payload)

def send_user_menu(chat_id, text):
    url = f"{TELEGRAM_INIT_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "reply_markup": {
            "keyboard": [
                [{"text": "🌐 OPEN SCRIPTS WEBSITE"}, {"text": "🔍 CHECK MY ACCESS"}],
                [{"text": "📂 MY AUTHORIZED SCRIPTS"}, {"text": "📱 MY REGISTERED DEVICES"}],
                [{"text": "📩 REQUEST VERIFICATION"}, {"text": "📞 CONTACT SUPPORT"}],
                [{"text": "🔄 Refresh Panel"}]
            ],
            "resize_keyboard": True,
            "is_persistent": True
        }
    }
    requests.post(url, json=payload)

def send_admin_dashboard(chat_id):
    url = f"{TELEGRAM_INIT_URL}/sendMessage"
    text = (
        f"👑 <b>😈☠️ 𝗠.𝗞 𝗛𝗔𝗖𝗞𝗘𝗥 𝗣𝗥𝗢 𝗦𝗖𝗥𝗜𝗣𝗧𝗦</b> ☠️😈\n"
        f"<b>ADMIN CONTROL CENTER</b>\n\n"
        f"📊 Total Users: <b>{len(USERS_DB)}</b>\n"
        f"💻 Registered Devices: <b>{len(AUTHORIZED_DEVICES)}</b>\n"
        f"🟢 System Status: <b>ONLINE & SECURE</b>"
    )
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "reply_markup": {
            "inline_keyboard": [
                [{"text": "📊 Dashboard", "callback_data": "admin_dashboard"}, {"text": "👥 All Users", "callback_data": "admin_users"}],
                [{"text": "🛡️ Verify IDs", "callback_data": "admin_verify"}, {"text": "🔥 Access Control", "callback_data": "admin_access"}],
                [{"text": "⚙️ Manage Scripts", "callback_data": "admin_scripts"}, {"text": "💻 Devices", "callback_data": "admin_devices"}]
            ]
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
