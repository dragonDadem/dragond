# bot.py
from twilio.rest import Client
import requests
from flask import Flask, request, send_file
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Twilio credentials
account_sid = 'AC6e859b6f530ee41d42413fe3caed1863'
auth_token = 'fed5aea7df65ca3a9426f7f1c4b11fcf'
from_whatsapp = '+14155238886'

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.form.get("Body")
    from_number = request.form.get("From")

    response = MessagingResponse()

    if incoming_msg.startswith("http"):
        file_url = incoming_msg.strip()
        save_path = "downloaded_file.txt"  # Replace with actual file type if needed

        # Download the file
        if download_file(file_url, save_path):
            response.message("روح قود مع الملف")
            response.message().media(f"{request.host_url}{save_path}")
        else:
            response.message("فشل تحميل الملف. تحقق من الرابط.")
    else:
        response.message("يرجى إرسال رابط صالح.")

    return str(response)

def send_whatsapp_message(account_sid, auth_token, from_whatsapp, to_whatsapp, message_body, media_url=None):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_=f'whatsapp:{from_whatsapp}',
        to=f'whatsapp:{to_whatsapp}',
        body=message_body,
        media_url=media_url
    )
    return message.sid

def download_file(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        return True
    return False

if __name__ == "__main__":
    app.run(debug=True)

# requirements.txt
twilio
flask
requests
