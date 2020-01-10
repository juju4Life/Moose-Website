from facebook_bot.fbchat_custom import *
from customer.secrets import Secrets

class FacebookBot(object):
    def __init__(self):
        self.secret = Secrets()
        self.client = Client(self.secret.facebook_email, self.secret.facebook_password)

    def send_message(self, message):
        if not self.client.isLoggedIn():
            self.client.login(self.secret.facebook_email, self.secret.facebook_password)
        self.client.send(Message(text="{}".format(message)), thread_id=1654976871416889, thread_type=ThreadType.GROUP)
#1654976871416889

    def crazy(self):
        id = 100000214330294
        if not self.client.isLoggedIn():
            self.client.login(self.secret.facebook_email, self.secret.facebook_password)
        messages = self.client.fetchThreadMessages(thread_id=id, limit=10)
        # Since the message come in reversed order, reverse them
        messages.reverse()
        for each in messages:
            print(each.text)


