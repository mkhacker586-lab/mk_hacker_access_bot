import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = "8990305636:AAFdelMPhGWQcE3SRons9w4g7fL5cfLb6W8"
ADMIN_CHAT_ID = "8791893329"
TELEGRAM_INIT_URL = f"https://api.telegram.org/bot{TOKEN}"

# Database Storage for Admin Control & Management
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
    return "😈☠️ 𝗠.𝗞 𝗛𝗔𝗖𝗞𝗘𝗥 𝗣𝗥𝗢 𝗦𝗖𝗥𝗜𝗣𝗧𝗦 ☠️😈 - ADMIN CONTROL CENTER ONLINE 🚀"

@app.route('/check-device', methods=['GET', 'POST', 'OPTIONS'])
def check_device():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
        
    try:
        data = request.get_json(silent=True) or {}
        device_id = request.args.get('device_id') or data.get('device_id')
        if not device_id and request.method == 'POST':
            device_id = request.form.get('device_id')
        
        if not device_id:
            return jsonify({"status": "error", "message": "Device ID missing"})
        
        if device_id in AUTHORIZED_DEVICES and AUTHORIZED_DEVICES[device_id]["status"] == "active":
            return jsonify({"status": "active", "message": "Device is Authorized ✓"})
        else:
            return jsonify({"status": "locked", "message": "Device Not Authorized ❌"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route(f'/{TOKEN}', methods=['POST', 'GET'])
def receive_update():
    if request.method == 'GET':
        return "Bot system active!", 200
        
    try:
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

            # STRICT ADMIN RESTRICTION: Sirf aur sirf Admin access kar sakta hai!
            if str(chat_id) != str(ADMIN_CHAT_ID):
                send_message(chat_id, "⚠️ <b>ACCESS DENIED</b>\n\nThis is a private administrative system for <b>M.K HACKER</b>.")
                return "OK", 200

            USERS_DB[chat_id] = {"username": username, "first_name": first_name, "status": "active"}

            if text == "/start" or text == "👑 Admin Dashboard" or text == "🔄 Refresh Panel":
                send_admin_dashboard(chat_id)

            elif text == "👥 All Users":
                user_list_text = f"👥 <b>TOTAL REGISTERED USERS ({len(USERS_DB)})</b>\n\n"
                for uid, uinfo in USERS_DB.items():
                    user_list_text += f"• ID: <code>{uid}</code> | @{uinfo['username']}\n"
                send_message(chat_id, user_list_text)

            elif text == "🛡️ Verify IDs":
                send_message(chat_id, "🛡️ <b>ID Verification Center</b>\n\nSend any User Device ID (e.g. MK-XXXX) or Telegram ID here to review and approve/remove access.")

            elif text == "🔥 Access Control":
                active_count = sum(1 for d in AUTHORIZED_DEVICES.values() if d["status"] == "active")
                send_message(chat_id, f"🔥 <b>Access Control Center</b>\n\nActive Authorized Devices: <b>{active_count}</b>\nUse inline buttons on verification requests to grant or revoke access.")

            elif text == "⚙️ Manage Scripts":
                send_message(chat_id, "⚙️ <b>Scripts Manager</b>\n\nAll M.K Hacker Pro Scripts are currently active and synced with your dashboard.")

            elif text == "💻 Devices":
                device_list_text = f"💻 <b>REGISTERED DEVICES ({len(AUTHORIZED_DEVICES)})</b>\n\n"
                for did, dinfo in AUTHORIZED_DEVICES.items():
                    device_list_text += f"• <code>{did}</code> ➔ Status: <b>{dinfo['status'].upper()}</b>\n"
                send_message(chat_id, device_list_text)

            elif text == "📋 Activity Logs":
                log_text = "📋 <b>RECENT ACTIVITY LOGS</b>\n\n"
                if ACTIVITY_LOGS:
                    for log in ACTIVITY_LOGS[-10:]:
                        log_text += f"• {log}\n"
                else:
                    log_text += "No activity recorded yet."
                send_message(chat_id, log_text)

            elif text == "🚨 Alerts":
                send_message(chat_id, "🚨 <b>System Alerts:</b> All security systems are online and secure.")

            elif text == "🛠️ Settings":
                send_message(chat_id, "🛠️ <b>System Settings:</b> Admin profile and webhook connections are fully synced.")

            elif text == "📥 Export Reports":
                send_message(chat_id, f"📥 <b>Export Report</b>\n\nTotal Users: {len(USERS_DB)}\nTotal Devices: {len(AUTHORIZED_DEVICES)}\nSystem Status: SECURE")

            elif text.startswith("MK-") or len(text) > 3:
                device_id = text
                AUTHORIZED_DEVICES[device_id] = {
                    "status": "pending",
                    "username": username,
                    "first_name": first_name,
                    "chat_id": chat_id
                }
                ACTIVITY_LOGS.append(f"Manual ID added: {device_id}")
                
                admin_text = (
                    f"🚨 <b>NEW SCRIPT ACCESS REQUEST</b>\n\n"
                    f"💻 <b>Device ID:</b> <code>{device_id}</code>\n\n"
                    f"⏳ <b>Status:</b> PENDING REVIEW"
                )
                send_inline_approval(chat_id=ADMIN_CHAT_ID, text=admin_text, device_id=device_id)

        elif "callback_query" in data:
            callback = data["callback_query"]
            callback_id = callback["id"]
            chat_id = callback["message"]["chat"]["id"]
            data_val = callback["data"]
            
            if str(chat_id) != str(ADMIN_CHAT_ID):
                answer_callback(callback_id, "Unauthorized!")
                return "OK", 200

            if data_val == "admin_dashboard":
                answer_callback(callback_id, "Dashboard Loaded!")
                send_admin_dashboard(chat_id)
                return "OK", 200

            parts = data_val.split("_", 1)
            if len(parts) == 2:
                action, device_id = parts

                if action == "approve":
                    if device_id in AUTHORIZED_DEVICES:
                        AUTHORIZED_DEVICES[device_id]["status"] = "active"
                    else:
                        AUTHORIZED_DEVICES[device_id] = {"status": "active", "username": "Admin", "chat_id": chat_id}
                    
                    ACTIVITY_LOGS.append(f"Approved device: {device_id}")
                    answer_callback(callback_id, "Access Granted! ✅")
                    edit_message_text(chat_id, callback["message"]["message_id"], f"✅ <b>APPROVED BY ADMIN</b>\n\n💻 Device ID: <code>{device_id}</code>\nStatus: <b>ACTIVE ✓</b>")

                elif action == "remove":
                    if device_id in AUTHORIZED_DEVICES:
                        AUTHORIZED_DEVICES[device_id]["status"] = "banned"
                    else:
                        AUTHORIZED_DEVICES[device_id] = {"status": "banned", "username": "Admin", "chat_id": chat_id}
                    
                    ACTIVITY_LOGS.append(f"Removed device: {device_id}")
                    answer_callback(callback_id, "Access Revoked! ❌")
                    edit_message_text(chat_id, callback["message"]["message_id"], f"❌ <b>REMOVED BY ADMIN</b>\n\n💻 Device ID: <code>{device_id}</code>\nStatus: <b>LOCKED ❌</b>")
    except Exception as e:
        print(f"Error: {e}")

    return "OK", 200

def send_message(chat_id, text):
    try:
        url = f"{TELEGRAM_INIT_URL}/sendMessage"
        payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
        requests.post(url, json=payload, timeout=5)
    except Exception:
        pass

def send_admin_dashboard(chat_id):
    try:
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
                "keyboard": [
                    [{"text": "📊 Dashboard"}, {"text": "👥 All Users"}],
                    [{"text": "🛡️ Verify IDs"}, {"text": "🔥 Access Control"}],
                    [{"text": "⚙️ Manage Scripts"}, {"text": "💻 Devices"}],
                    [{"text": "📋 Activity Logs"}, {"text": "🚨 Alerts"}],
                    [{"text": "🛠️ Settings"}, {"text": "📥 Export Reports"}],
                    [{"text": "🔄 Refresh Panel"}]
                ],
                "resize_keyboard": True,
                "is_persistent": True
            }
        }
        requests.post(url, json=payload, timeout=5)
    except Exception:
        pass

def send_inline_approval(chat_id, text, device_id):
    try:
        url = f"{TELEGRAM_INIT_URL}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "reply_markup": {
                "inline_keyboard": [
                    [
                        {"text": "✅ APPROVE", "callback_data": f"approve_{device_id}"},
                        {"text": "❌ REMOVE", "callback_data": f"remove_{device_id}"}
                    ]
                ]
            }
        }
        requests.post(url, json=payload, timeout=5)
    except Exception:
        pass

def edit_message_text(chat_id, message_id, text):
    try:
        url = f"{TELEGRAM_INIT_URL}/editMessageText"
        payload = {"chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": "HTML"}
        requests.post(url, json=payload, timeout=5)
    except Exception:
        pass

def answer_callback(callback_id, text):
    try:
        url = f"{TELEGRAM_INIT_URL}/answerCallbackQuery"
        payload = {"callback_query_id": callback_id, "text": text, "show_alert": True}
        requests.post(url, json=payload, timeout=5)
    except Exception:
        pass
