from fbchat_custom import Client
from customer.fix_words import FixWords
from fbchat_custom.models import *
from customer.secrets import Secrets
from .query import GetCards, GetProducts

fix_words = FixWords()
get_cards = GetCards()
get_products = GetProducts()

class ListenBot(Client):
    def onMessage(self, message_object, thread_id, **kwargs):
        text = message_object.text
        def send_msg(msg):
            self.send(Message(text=msg), thread_id=100000214330294, thread_type=ThreadType.USER)
        if text[0:11].lower() == 'bot buylist':
            cards = text[11:].split('&')
            for card in cards:
                if '|' in card:
                    card = card.split('|')
                    card_name = fix_words.fix_name(card[0])
                    card_set = fix_words.fix_set(fix_words.fix_name(card[1]))
                else:
                    card_name = fix_words.fix_name(card)
                    card_set = ''

                if len(card_set) > 0:
                    send_msg("Working on it...")
                    results = get_cards.buylist_by_name_and_set(card_name, card_set)
                    if results == 'error':
                        send_msg("error: {} or {} may be misspelled".format(card_name, card_set))
                    else:
                        send_msg(results)
                else:
                    send_msg("Working on it...")
                    results = get_cards.buylist_by_name(card_name)
                    if results == 'error':
                        send_msg("error: {} not in database".format(card_name))
                    else:
                        send_msg(results)


        elif text[0:10].lower() == 'bot online':
            cards = text[10:].split('&')
            for card in cards:
                if '|' in card:
                    card = card.split('|')
                    card_name = fix_words.fix_name(card[0])
                    card_set = fix_words.fix_set(fix_words.fix_name(card[1]))
                else:
                    card_name = fix_words.fix_name(card)
                    card_set = ''

                if len(card_set) > 0:
                    send_msg("Working on it...")
                    results = get_cards.search_by_name_and_set(card_name, card_set)
                    if results == 'error':
                        send_msg("error: {} or {} may be misspelled".format(card_name, card_set))
                    else:
                        send_msg(results)

                else:
                    send_msg("Working on it...")
                    results = get_cards.search_by_name(card_name)
                    if results == 'error':
                        send_msg("error: {}. Please check your spelling".format(card_name))
                    else:
                        send_msg(results)


        elif text[0:9].lower() == 'bot month':
            search = fix_words.fix_name(text[9:])
            search = search.split('|')
            if len(search) > 0 and len(search) < 3:
                if len(search) > 1:
                    results_message = get_products.by_month(fix_words.fix_name(search[0]), fix_words.fix_name(search[1]))
                    send_msg(results_message)
                else:
                    results_message = get_products.by_month(fix_words.fix_name(search[0]))
                    send_msg(results_message)
            else:
                send_msg('Too many, or too few parameters. Please message "bot help" for help files.')

        elif text[0:7].lower() == 'bot new':
            results_message = get_products.upcoming()
            send_msg(results_message)




        elif text[0:8].lower() == 'bot help':
            send_msg(
                "BOT COMMANDS HELP FILE\n\n"
                "bot buylist CardName1\n"
                "-----\n"
                "bot online CardName1\n"
                "-----\n"
                "bot month E.g. jan OR january\n"
                "-----\n"
                "bot new\n"
                "-----\n"
                "| =\n CardName/SetName - Product/Year Separator E.g. CardName1 | SetName E.g. Month | Year\n\n"
                "& =\n CardName1/CardName2 Separator E.g. CardName1 & CardName2 | SetName\n\n"
            )





