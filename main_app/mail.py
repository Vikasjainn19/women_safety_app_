import os
import smtplib
from email.utils import formataddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from dotenv import load_dotenv  # Import dotenv

# Load environment variables from .env file
load_dotenv()

def send_email(name, dest, link):
    # Fetch email credentials from environment variables
    EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("Error: Email credentials are not set in environment variables.")
        return

    try:
        print("Initializing SMTP server...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(1)  # Enable verbose logging for SMTP communication
        server.starttls()
        print("Starting TLS encryption...")
        
        print("Logging into the email server...")
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        print("Login successful.")

        # Safely load email template
        try:
            template_path = Path('main_app/templates/main_app/email.html')
            print(f"Loading email template from: {template_path}")
            with template_path.open() as email_html:
                email_body = email_html.read().format(name=name, link=link)
            print("Email template loaded and formatted successfully.")
        except FileNotFoundError:
            print("Error: HTML template file not found.")
            return
        except KeyError as e:
            print(f"Error: Missing placeholder in email template: {e}")
            return

        # Construct the email
        print("Constructing the email message...")
        msg = MIMEMultipart()
        msg['Subject'] = 'EMERGENCY'
        msg.attach(MIMEText(email_body, 'html'))
        msg['From'] = formataddr(("TEAM RESCUE", EMAIL_ADDRESS))
        msg['To'] = dest  # Ensure the 'To' header is correctly set
        print(f"Email constructed successfully. Sending to: {dest}")

        # Send the email
        server.sendmail(EMAIL_ADDRESS, dest, msg.as_string())
        print(f"Email sent to {dest} successfully!")
    except smtplib.SMTPAuthenticationError:
        print("Error: Authentication failed. Check your email credentials.")
    except smtplib.SMTPConnectError:
        print("Error: Unable to connect to the SMTP server.")
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        try:
            print("Closing the SMTP server connection...")
            server.quit()
            print("SMTP server connection closed.")
        except Exception as e:
            print(f"Error while closing the SMTP server connection: {e}")