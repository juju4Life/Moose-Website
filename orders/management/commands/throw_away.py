from django.core.management.base import BaseCommand
from engine.models import TcgGroupPrice
import csv


class Command(BaseCommand):
    def handle(self, *args, **options):
        card_list = set(TcgGroupPrice.objects.exclude(
            expansion__in=[
                'World Championship Decks', 'MagicFest Cards', "Collector's Edition", "Legends", "Arabian Nights",
                "The Dark", "Antiquities", 'Oversize Cards', "Unlimited Edition", "Alpha Edition", "Beta Edition", "APAC Lands",
                "Arena Promos", "Champs Promos", "Duels of the Planeswalkers", "European Lands", "Explorers of Ixalan",
                "Game Day & Store Championship Promos", "Guilds of Ravnica: Mythic Edition", "Guru Lands", "Magic Player Rewards",
                "Magic Premiere Shop", "Media Promos", "Open House Promos", "Portal", "Portal Second Age", "Portal Three Kingdoms",
                "Prerelease Cards", "Signature Spellbook: Jace", "Special Occasion", "Starter 1999", "Starter 2000", "The Dark",
                "Ugin's Fate Promos", "	Unhinged", "Unique and Miscellaneous Promos", "Vanguard", "International Edition", "Promo Pack: Core Set 2020",
                "Art Series: Modern Horizons", "Signature Spellbook: Gideon", "War of the Spark: Mythic Edition", "Duel Decks", "Box Sets",
                "Astral", "Battle Royale Box Set", "Beatdown Box Set", "Deckmasters Garfield vs Finkel", "Premium Deck Series: Slivers",
                "Premium Deck Series: Graveborn", "From the Vault: Dragons", "From the Vault: Exiled", "From the Vault: Relics", "From the Vault: Legends",
                "From the Vault: Realms", "From the Vault: Twenty", "From the Vault: Annihilation", "Duel Decks: Elves vs. Goblins",
                "Duel Decks: Jace vs. Chandra", "Duel Decks: Divine vs. Demonic", "Duel Decks: Garruk vs. Liliana", "Duel Decks: Phyrexia vs. the Coalition",
                "Duel Decks: Elspeth vs. Tezzeret", "Duel Decks: Knights vs. Dragons", "Duel Decks: Ajani vs. Nicol Bolas", "Duel Decks: Venser vs. Koth",
                "Duel Decks: Izzet vs. Golgari", "Duel Decks: Sorin vs. Tibalt", "Duel Decks: Heroes vs. Monsters", "Duel Decks: Jace vs. Vraska",
                "Duel Decks: Speed vs. Cunning"
            ]
        ))

        headers = ['name', 'expansion']
        file = open('case_cards.csv', 'w', newline='')
        writer = csv.DictWriter(f=file, fieldnames=headers)
        cards_to_dict = {}

        for card in card_list:
            cards_to_dict[card.name] = card.expansion

        for k, v in cards_to_dict.items():
            writer.writerow(
                {'name': k, 'expansion': v}
            )












