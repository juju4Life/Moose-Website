import decouple
import requests


class MailGun:
    def __init__(self):
        self.mailgun_domain = decouple.config("MAILGUN_DOMAIN")
        self.mailgun_api_key = decouple.config("MAILGUN_API_KEY")

    def send_mail(self):
        return requests.post(
            f"https://api.mailgun.net/v3/{self.mailgun_domain}/messages",
            auth=("api", self.mailgun_api_key),
            data={"from": f"Excited User <mailgun@{self.mailgun_domain}>",
                  "to":  f"jermol@sandbox884d3d49b0c84f64a6b281d3d42d98e9.mailgun.org",
                  "subject": "Hello",
                  "text": "Testing some Mailgun awesomness!"}
            )


