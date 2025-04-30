import os
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
from_number = os.getenv('TWILIO_FROM_PHONE_NUMBER')

def send_sms_alert(to_number, lat, lon):
    """
    Sends an SMS alert with the given latitude and longitude.
    """
    if not account_sid or not auth_token or not from_number:
        print("Error: Twilio credentials are not set.")
        return

    client = Client(account_sid, auth_token)
    try:
        message_body = f"🚨 Emergency alert! Location 🗺️:\nClick here: https://maps.google.com/?q={lat},{lon}\nPlease check on your loved one."
        print(f"Sending SMS to {to_number} with message: {message_body}")
        message = client.messages.create(
            body=message_body,
            from_=from_number,
            to=to_number
        )
        print(f"SMS sent successfully: {message.sid}")
    except Exception as e:
        print(f"Error sending SMS: {e}")

if __name__ == "__main__":
    # Test data
    test_to_number = "+917247642074"  # Replace with a valid phone number
    test_lat = 23.25256575
    test_lon = 77.47160899999999

    # Call the function
    send_sms_alert(test_to_number, test_lat, test_lon)