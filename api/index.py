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
    return "😈☠️ 𝗠.𝗞 HACKER PRO SCRIPTS ☠️😈 - SYSTEM ONLINE 🚀"

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

@app.route('/getqx.js')
def get_qx_script():
    js_code = """
    (async function() {
        if(document.getElementById('__mkh_loader__')) return;
        
        let deviceId = localStorage.getItem('__mkh_device_id');
        if (!deviceId) {
            deviceId = 'MK-' + Math.floor(100000000 + Math.random() * 900000000);
            localStorage.setItem('__mkh_device_id', deviceId);
        }

        const d = document, b = d.body, l = d.createElement('div');
        l.id = '__mkh_loader__';
        l.style = 'position:fixed;inset:0;background:rgba(0,0,0,0.88);display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:999999;font-family:sans-serif;backdrop-filter:blur(5px);';
        
        const c = d.createElement('div');
        c.style = 'width:65px;height:65px;border:6px solid rgba(255,30,30,0.2);border-top:6px solid #ff1e1e;border-radius:50%;animation:s .4s linear infinite';
        
        if (!d.getElementById('__mkh_anim_style__')) {
            const st = d.createElement('style');
            st.id = '__mkh_anim_style__';
            st.textContent = '@keyframes s{to{transform:rotate(360deg)}}';
            d.head.appendChild(st);
        }

        const t = d.createElement('div');
        t.style = 'color:#ff1e1e;font-weight:900;margin-top:15px;font-size:14px;letter-spacing:1px;text-shadow:0 0 15px rgba(255,30,30,0.8);';
        t.innerHTML = '😈☠️ <b>𝗠.𝗞 HACKER LOADING...</b>';
        
        l.appendChild(c);
        l.appendChild(t);
        b.appendChild(l);

        try {
            let res = await fetch('https://mk-hacker-access-bot.vercel.app/check-device?device_id=' + deviceId);
            let data = await res.json();
            
            if (data.status === 'active') {
                l.remove();
                // Load original working script here
                const s = d.createElement('script');
                s.src = 'https://mkhackerproscripts.vercel.app/getqx.js?v=' + Date.now();
                b.appendChild(s);
                return;
            }
        } catch(e) {}

        l.remove();
        
        // Show stylish lock/device ID popup if not authorized
        if(document.getElementById('__mkh_lock_panel__')) return;
        const pl = d.createElement('div');
        pl.id = '__mkh_lock_panel__';
        pl.style = 'position:fixed;inset:0;background:rgba(0,0,0,0.92);display:flex;align-items:center;justify-content:center;z-index:999999;font-family:sans-serif;backdrop-filter:blur(8px);';
        
        pl.innerHTML = `
            <div style="background:#0a0a0a;border:2px solid #ff1e1e;box-shadow:0 0 35px rgba(255,30,30,0.7);border-radius:20px;padding:30px;width:340px;text-align:center;color:#fff;">
                <h2 style="color:#ff1e1e;margin:0 0 10px 0;font-size:20px;">😈☠️ M.K HACKER ☠️😈</h2>
                <h3 style="color:#ff1e1e;margin:0 0 15px 0;font-size:16px;">ACCESS LOCKED ❌</h3>
                <p style="font-size:12px;color:#bbb;margin-bottom:20px;">Your device is not authorized. Send your Device ID to the bot.</p>
                <div style="background:#111;border:1px dashed #ff1e1e;padding:12px;border-radius:10px;margin-bottom:15px;font-weight:bold;color:#ff1e1e;letter-spacing:1px;font-size:15px;">${deviceId}</div>
                <button id="__mkh_copy_btn__" style="background:#ff1e1e;color:#fff;border:none;padding:12px 20px;border-radius:10px;font-weight:bold;cursor:pointer;width:100%;margin-bottom:12px;box-shadow:0 0 15px rgba(255,30,30,0.5);">📋 COPY DEVICE ID</button>
                <a href="https://t.me/mk_hacker_access_bot" target="_blank" style="display:block;background:transparent;border:1px solid #ff1e1e;color:#ff1e1e;padding:11px 20px;border-radius:10px;font-weight:bold;text-decoration:none;margin-bottom:12px;font-size:14px;">📩 OPEN BOT FOR ACCESS</a>
                <button id="__mkh_reload_btn__" style="background:#222;color:#fff;border:1px solid #444;padding:9px 15px;border-radius:8px;cursor:pointer;width:100%;font-size:13px;">🔄 CHECK STATUS AGAIN</button>
            </div>
        `;
        b.appendChild(pl);

        d.getElementById('__mkh_copy_btn__').onclick = () => {
            navigator.clipboard.writeText(deviceId);
            alert('Device ID Copied Successfully! ✅');
        };

        d.getElementById('__mkh_reload_btn__').onclick = () => {
            location.reload();
        };
    })();
    """
    return js_code, 200, {'Content-Type': 'application/javascript'}

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
                f"🎯 <b>YOUR ACCESS STARTS HERE</b>\n\n"
                f"👨‍💻 <b>BRAND:</b> 😈☠️ 𝗠.𝗞 H𝗔𝗖𝗞𝗘𝗥 ☠️😈\n"
                f"📲 <b>SUPPORT:</b> @MK_HACKER586\n\n"
                f"🖤 <b>PRECISION • SECURITY • CONTROL</b> 🐺"
            )
            send_reply_keyboard_menu(chat_id, welcome_msg)

        elif text == "💻 Active Scripts":
            msg = (
                f"💻 <b>ACTIVE SCRIPTS MANAGER</b>\n\n"
                f"✨ Yahan aapke tamam authorized scripts aur unka live status show hota hai.\n\n"
                f"🟢 System Status: <b>ONLINE & SECURE</b>\n"
                f"👑 <b>BRAND:</b> 😈☠️ 𝗠.𝗞 H𝗔𝗖𝗞𝗘𝗥 ☠️😈"
            )
            send_message(chat_id, msg)

        elif text == "🛡️ Security Status":
            msg = (
                f"🛡️ <b>SECURITY & ENCRYPTION SHIELD</b>\n\n"
                f"🔒 Advanced token protection aur device locking active hai.\n"
                f"⚡ Koi bhi unauthorized script run nahi ho sakti.\n\n"
                f"👑 <b>BRAND:</b> 😈☠️ 𝗠.𝗞 H𝗔𝗖𝗞𝗘𝗥 ☠️😈"
            )
            send_message(chat_id, msg)

        elif text == "⚡ Device Verifier":
            msg = (
                f"⚡ <b>DEVICE ID VERIFIER</b>\n\n"
                f"📋 Apni script dashboard se Device ID copy karein aur yahan direct chat mein send karein taake verification mukammal ho sake.\n\n"
                f"👑 <b>BRAND:</b> 😈☠️ 𝗠.𝗞 H𝗔𝗖𝗞𝗘𝗥 ☠️😈"
            )
            send_message(chat_id, msg)

        elif text == "🔥 Access Control":
            msg = (
                f"🔥 <b>ACCESS CONTROL CENTER</b>\n\n"
                f"⚙️ Har device ki access management yahan se handle hoti hai. Pending requests foran admin ke paas approval ke liye jati hain.\n\n"
                f"👑 <b>BRAND:</b> 😈☠️ 𝗠.𝗞 H𝗔𝗖𝗞𝗘𝗥 ☠️😈"
            )
            send_message(chat_id, msg)

        elif text == "📋 All Devices List" or text == "/list":
            if str(chat_id) == str(ADMIN_CHAT_ID):
                send_devices_list_panel(chat_id)
            else:
                send_message(chat_id, "⚠️ Yeh option sirf admin ke liye mukhtas hai.")

        elif text == "👑 Admin Control Panel":
            if str(chat_id) == str(ADMIN_CHAT_ID):
                admin_panel_msg = (
                    f"👑 <b>ADMIN CONTROL PANEL</b>\n\n"
                    f"🛠️ Aap yahan se saari registered devices ki list dekh sakte hain aur kisi bhi waqt access revoke ya approve kar sakte hain.\n\n"
                    f"👇 Neeche diye gaye 'All Devices List' button par click karein."
                )
                send_message(chat_id, admin_panel_msg)
            else:
                send_message(chat_id, "⚠️ Access Denied! Only Admin can access this panel.")

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
                f"🛡️ Your access request is awaiting admin review.\n\n"
                f"👑 <b>BRAND:</b> 😈☠️ 𝗠.𝗞 H𝗔𝗖𝗞𝗘𝗥 ☠️😈"
            )
            send_message(chat_id, user_pending_msg)

            admin_text = (
                f"🚨 <b>NEW SCRIPT ACCESS REQUEST</b>\n\n"
                f"👤 <b>Name:</b> {first_name}\n"
                f"📱 <b>Username:</b> @{username}\n"
                f"🆔 <b>Telegram ID:</b> <code>{chat_id}</code>\n\n"
                f"💻 <b>Device ID:</b> <code>{device_id}</code>\n\n"
                f"⏳ <b>Status:</b> PENDING REVIEW\n\n"
                f"👑 <b>BRAND:</b> 😈☠️ 𝗠.𝗞 H𝗔𝗖𝗞𝗘𝗥 ☠️😈"
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
                edit_message_text(chat_id, callback["message"]["message_id"], f"✅ <b>SCRIPT ACCESS APPROVED</b>\n\n💻 Device ID: <code>{device_id}</code>\nStatus: <b>ACTIVE ✓</b>\n👑 <b>BRAND:</b> 😈☠️ 𝗠.𝗞 H𝗔𝗖𝗞𝗘𝗥 ☠️😈")
                
                user_target_chat = AUTHORIZED_DEVICES[device_id].get("chat_id")
                if user_target_chat:
                    approved_msg = (
                        f"🎉 <b>CONGRATULATIONS!</b> 👑\n\n"
                        f"😈☠️ <b>𝗠.𝗞 H𝗔𝗖𝗞𝗘𝗥 𝗣𝗥𝗢 𝗦𝗖𝗥𝗜𝗣𝗧𝗦</b> ☠️😈\n\n"
                        f"✅ <b>YOUR SCRIPT IS NOW ACTIVE</b>\n\n"
                        f"💻 <b>Device ID:</b> <code>{device_id}</code>\n\n"
                        f"🟢 <b>Status:</b> ACTIVE ✓\n\n"
                        f"🚀 Your device is fully authorized and working.\n\n"
                        f"📩 <b>SUPPORT:</b> @MK_HACKER586\n\n"
                        f"🖤 <b>PRECISION • SECURITY • CONTROL</b>"
                    )
                    send_message(user_target_chat, approved_msg)

            elif action == "remove":
                if device_id in AUTHORIZED_DEVICES:
                    AUTHORIZED_DEVICES[device_id]["status"] = "banned"
                
                answer_callback(callback_id, "Script Access Revoked! ❌")
                edit_message_text(chat_id, callback["message"]["message_id"], f"❌ <b>SCRIPT ACCESS REMOVED</b>\n\n💻 Device ID: <code>{device_id}</code>\nStatus: <b>LOCKED ❌</b>\n👑 <b>BRAND:</b> 😈☠️ 𝗠.𝗞 H𝗔𝗖𝗞𝗘𝗥 ☠️😈")

                user_target_chat = AUTHORIZED_DEVICES[device_id].get("chat_id")
                if user_target_chat:
                    revoked_msg = (
                        f"⚠️ <b>ACCESS UPDATE</b>\n\n"
                        f"😈☠️ <b>𝗠.𝗞 H𝗔𝗖𝗞𝗘𝗥 𝗣𝗥𝗢 𝗦𝗖𝗥𝗜𝗣𝗧𝗦</b> ☠️😈\n\n"
                        f"🔒 Your script access has been disabled by admin.\n\n"
                        f"💻 <b>Device ID:</b> <code>{device_id}</code>\n\n"
                        f"🔴 <b>Status:</b> LOCKED ❌\n\n"
                        f"👨‍💻 <b>SUPPORT:</b> @MK_HACKER586"
                    )
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

def send_devices_list_panel(chat_id):
    if not AUTHORIZED_DEVICES:
        text = "⚠️ <b>No devices registered in the system yet.</b>"
    else:
        text = "📋 😈☠️ <b>𝗠.𝗞 H𝗔𝗖𝗞𝗘𝗥 𝗣𝗥𝗢 𝗦𝗖𝗥𝗜𝗣𝗧𝗦</b> ☠️😈\n\n<b>Registered Devices Data:</b>\n"
        for dev_id, info in AUTHORIZED_DEVICES.items():
            status_icon = "🟢" if info['status'] == "active" else "🔴"
            text += f"\n{status_icon} ID: <code>{dev_id}</code>\n👤 User: @{info['username']}\n📌 Status: <b>{info['status'].upper()}</b>\n-------------------"
    
    url = f"{TELEGRAM_INIT_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
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
