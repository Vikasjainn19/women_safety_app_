import smtplib
from email.utils import formataddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(name, dest, link):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(1)  # Enable verbose logging
        server.starttls()
        server.login("vikasjainn19@gmail.com", "btdo jroh xqsl mjzq")
        # Safely load email template
        try:
            with open('main_app/templates/main_app/email.html') as email_html:
                email_body = email_html.read().format(name=name, link=link)
        except FileNotFoundError:
            print("HTML template file not found.")
            return

        msg = MIMEMultipart()
        msg['Subject'] = 'EMERGENCY'
        msg.attach(MIMEText(email_body, 'html'))
        msg['From'] = formataddr(("TEAM RESCUE", "vikasjainn19@gmail.com"))
        msg['To'] = dest  # Ensure the 'To' header is correctly set
        
        server.sendmail("vikasjainn19@gmail.com", dest, msg.as_string())
        print(f"Email sent to {dest} successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

