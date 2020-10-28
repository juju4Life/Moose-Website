
from decouple import config
from twilio.rest import Client


class Twilio:

    def __init__(self):
        self.account_sid = config('TWILIO_ACCOUNT_SID')
        self.auth_token = config('TWILIO_AUTH_TOKEN')
        self.phone_number = config('TWILIO_PHONE_NUMBER')

    def get_client(self):
        client = Client(self.account_sid, self.auth_token)
        return client

    def send_message(self, phone_number, message_body):
        message = self.get_client().messages.create(
            to=f"+1{phone_number}",
            from_=self.phone_number,
            body=message_body,
        )

        return message











