"""
Server Monitoring Script
Checks if the server IP, API subdomain, and domain are online.
Sends email alerts ONLY when at least one target is UP.
"""

import smtplib
import socket
import time
from email.mime.text import MIMEText
import requests

# ========================
# Monitored Targets
# ========================
TARGETS = {
    "Server IP": "91.99.79.25",  # checked with socket
    "API Subdomain": "https://api.thedesigngrit.com",
    "Main Domain": "https://thedesigngrit.com"
}

# ========================
# Email Configuration
# ========================
EMAILS = ["karimwahba53@gmail.com", "khaledamrahmed0@gmail.com", "khaledamrahmed0@gmail.com"]
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "karimwahba53@gmail.com"     # Replace with your Gmail
SMTP_PASS = "reok azbe omwl vgwe"                           # Use Gmail App Password


def send_email(subject: str, body: str) -> None:
    """Send an email notification to all configured recipients."""
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = ", ".join(EMAILS)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, EMAILS, msg.as_string())
        print("✅ Email sent successfully.")
    except smtplib.SMTPException as e:
        print(f"❌ Failed to send email: {e}")


def check_target(name: str, url: str) -> bool:
    """Check if a given target (IP/domain/subdomain) is online."""
    try:
        if name == "Server IP":  # check socket reachability
            socket.create_connection((url, 80), timeout=5)
            print(f"✅ {name} ({url}) is UP.")
            return True
        else:  # check with HTTP request
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ {name} ({url}) is UP.")
                return True
            else:
                print(f"⚠️ {name} ({url}) returned {response.status_code}.")
                return False
    except (requests.exceptions.RequestException, socket.error) as e:
        print(f"❌ {name} ({url}) is DOWN. Error: {e}")
        return False


def main() -> None:
    """Continuously monitor all targets every 60 seconds."""
    already_notified = False  # avoid spamming

    while True:
        up_targets = []

        for name, url in TARGETS.items():
            if check_target(name, url):
                up_targets.append(name)

        if up_targets and not already_notified:
            body = "✅ The following targets are UP and running:\n" + "\n".join(up_targets)
            send_email("✅ Server Status: UP", body)
            already_notified = True
        elif not up_targets:
            print("🌍 No targets are UP right now.")
            already_notified = False  # reset so when it comes back up we notify again

        print("🔄 Waiting 60 seconds before next check...\n")
        time.sleep(60)


if __name__ == "__main__":
    main()
