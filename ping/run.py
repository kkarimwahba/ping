import requests
import smtplib
from email.mime.text import MIMEText
import time

# Server details
server_ip = "91.99.75.25"
api_url = "http://api.thedesigngrit.com"
phone_numbers = ["01020180941", "01115570635"]
emails = ["karimwahba53@gmail.com", "khaledamrahmed0@gmail.com"]

# Email configuration
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_user = "your_email@gmail.com"  # Replace with your email
smtp_password = "your_email_password"  # Replace with your email password

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = smtp_user
    msg['To'] = ", ".join(emails)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, emails, msg.as_string())

def check_server():
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return True
    except requests.exceptions.RequestException:
        return False
    return False

def main():
    while True:
        if check_server():
            message = "The server is running!"
            send_email("Server Status Alert", message)
            print("Email sent!")
        else:
            print("Server is down.")
        
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()