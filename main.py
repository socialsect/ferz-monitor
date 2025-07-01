from flask import Flask
from threading import Thread
import os
import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
from datetime import datetime

EMAIL_FROM = os.environ.get("EMAIL_FROM")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
EMAIL_TO = ["vinayakxsingh21@gmail.com", "farazmirza1110@gmail.com"]

urls = [
    "https://ferzconsulting.com/",
    "https://ferzconsulting.com/about-us/",
    # ... (rest of the URLs)
    "https://ferzconsulting.com/services/strategic-advisory-services/",
]

def send_alert(url):
    msg = EmailMessage()
    msg["Subject"] = f"[ALERT] 404 Detected on {url}"
    msg["From"] = EMAIL_FROM
    msg["To"] = ", ".join(EMAIL_TO)
    msg.set_content(
        f"The page at *{url}* is showing '404 – PAGE NOT FOUND' at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.\n\nFIX KARDO PLEASE"
    )
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_FROM, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print(f"[EMAIL SENT] 404 alert for {url}")
    except Exception as e:
        print(f"[ERROR] Failed to send email for {url}: {e}")

def check_page(url):
    try:
        res = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(res.text, "html.parser")
        h1 = soup.find("h1")
        if h1 and "404" in h1.text.strip().lower():
            print(f"[ALERT] 404 found on: {url}")
            send_alert(url)
        else:
            print(f"[OK] {url}")
    except Exception as e:
        print(f"[ERROR] Could not check {url}: {e}")

app = Flask(__name__)

@app.route("/")
def home():
    return "Ferz Monitor is running. Go to /scan to check pages."

@app.route("/scan")
def scan():
    for url in urls:
        check_page(url)
    return "Scan complete."

def run_server():
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    Thread(target=run_server).start()
