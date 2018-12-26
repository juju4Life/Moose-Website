from django.apps import AppConfig


"""class BotConfig(AppConfig):
    name = 'customer'
    def ready(self):
        from customer.facebook_listen import ListenBot
        from customer.secrets import Secrets
        client = ListenBot(Secrets.facebook_email, Secrets.facebook_password)
        while True:
            if not client.onListening():
                if not client.isLoggedIn():
                    client = ListenBot(Secrets.facebook_email, Secrets.facebook_password)
                client.listen(end_time=10)"""