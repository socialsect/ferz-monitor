from flask import Flask
import os
import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
from datetime import datetime

EMAIL_FROM = os.environ["EMAIL_FROM"]
EMAIL_TO = ["vinayakxsingh21@gmail.com", "farazmirza1110@gmail.com"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]

urls = [
 "https://ferzconsulting.com/SAMPLE_URL_VINAYAK",
    "https://ferzconsulting.com/",
    "https://ferzconsulting.com/about-us/",
    "https://ferzconsulting.com/services/",
    "https://ferzconsulting.com/products/",
    "https://ferzconsulting.com/methodologies/",
    "https://ferzconsulting.com/articles/",
    "https://ferzconsulting.com/ip-portfolio/",
    "https://ferzconsulting.com/articles/measurable-style/",
    "https://ferzconsulting.com/articles/the-architect-and-the-fire/",
    "https://ferzconsulting.com/articles/the-question-is-the-lock/",
    "https://ferzconsulting.com/articles/deepseek-the-trojan-horse-in-open-source-ai/",
    "https://ferzconsulting.com/articles/transforming-wisdom-into-systems-with-ai/",
    "https://ferzconsulting.com/articles/the-hidden-traps-of-ai-analysis-a-users-guide-to-better-collaboration/",
    "https://ferzconsulting.com/articles/ai-at-a-crossroads-apples-findings-and-the-case-for-deterministic-reasoning-systems/",
    "https://ferzconsulting.com/articles/sovereignty-or-subjugation-the-constitutional-imperative-of-democratic-ai-leadership/",
    "https://ferzconsulting.com/articles/the-fourth-trap-when-ai-becomes-your-confirming-chorus/",
    "https://ferzconsulting.com/articles/a-critical-analysis/",
    "https://ferzconsulting.com/articles/the-darwin-godel-machine-critique-a-critical-analysis-of-self-improving-ai-safety-standards/",
    "https://ferzconsulting.com/privacy-policy/",
    "https://ferzconsulting.com/disclaimer/",
    "https://ferzconsulting.com/contact-us/",
    "https://ferzconsulting.com/products/lasof-ag/",
    "https://ferzconsulting.com/methodologies/mrcf/",
    "https://ferzconsulting.com/methodologies/scm/",
    "https://ferzconsulting.com/products/lasof/",
    "https://ferzconsulting.com/services/within-paradigm-improvements/",
    "https://ferzconsulting.com/services/design-of-ai-governance-models/",
    "https://ferzconsulting.com/services/lasof-implementation/",
    "https://ferzconsulting.com/services/ai-enablement-strategy/",
    "https://ferzconsulting.com/services/ai-consulting/",
    "https://ferzconsulting.com/services/it-innovation-modernization/",
    "https://ferzconsulting.com/services/strategic-advisory-services/",
]

def send_alert(url):
    msg = EmailMessage()
    msg["Subject"] = f"[ALERT] 404 Detected on {url}"
    msg["From"] = EMAIL_FROM
    msg["To"] = ", ".join(EMAIL_TO)
    msg.set_content(
        f"The page at *{url}* is showing '404 – PAGE NOT FOUND' "
        f"at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.\n\nFIX KARDO PLEASE"
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
    return "Ferz Monitor is Live. Go to /scan to check pages."

@app.route("/scan")
def scan():
    for url in urls:
        check_page(url)
    return "Scan complete."
