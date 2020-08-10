import decouple
import requests


class MailGun:
    def __init__(self):
        self.mailgun_domain = decouple.config("MAILGUN_DOMAIN")
        self.mailgun_api_key = decouple.config("MAILGUN_API_KEY")

    def send_mail(self, recipient_list, subject, message):
        info = requests.post(
            f"https://api.mailgun.net/v3/{self.mailgun_domain}/messages",
            auth=("api", self.mailgun_api_key),
            data={
                "from": f"MooseLoot <mailgun@{self.mailgun_domain}>",
                "to": recipient_list,
                "subject": subject,
                "text": message
            }
        )

        return info

    def get_logs(self, recipient):

        params = {
            "begin": "Fri, 3 May 2013 09:00:00 -0000",
            "ascending": "yes",
            "limit": 25,
            "pretty": "yes",
            "recipient": recipient,
        }

        return requests.get(
            f"https://api.mailgun.net/v3/{self.mailgun_domain}/events",
            auth=("api", self.mailgun_api_key), params=params)

    def create_route(self):
        data = {
            "priority": 0,
            "description": "Sample route",
            "expression": f"match_recipient('.*@{self.mailgun_domain}')",
            "action": ["forward('https://tcgfirst.com/mail/incoming/')", "stop()"]
        }

        r = requests.post("https://api.mailgun.net/v3/routes", auth=("api", self.mailgun_api_key), data=data)

        return r





