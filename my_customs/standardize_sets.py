
class Standardize:

    def expansion(self, set_):
        set_name = set_.strip()

        if set_name == 'Shadows Over Innistrad':
            set_name = 'Shadows over Innistrad'

        if '[F6]' in set_name:
            set_name = set_name.replace('[F6]', '').strip()
        elif '[F5]' in set_name:
            set_name = set_name.replace('[F5]', '').strip()
        elif '[F4]' in set_name:
            set_name = set_name.replace('[F4]', '').strip()
        elif '[F3]' in set_name:
            set_name = set_name.replace('[F3]', '').strip()
        elif '[F2]' in set_name:
            set_name = set_name.replace('[F2]', '').strip()
        elif '[F1]' in set_name:
            set_name = set_name.replace('[F1]', '').strip()

        if 'Promo' in set_name or 'Promotional Cards' in set_name or 'Promos' in set_name:
            set_name = 'Promotional'.strip()

        if 'foils' in set_name.lower():
            set_name = set_name.replace('Foils', '').replace('foils', '').replace('FOILS', '').strip()
        elif '(foil)' in set_name.lower():
            set_name = set_name.replace('(Foil)', '').strip()
        elif 'foil' in set_name.lower():
            set_name = set_name.replace('Foil', '').replace('foil', '').replace('FOIL', '').strip()

        if 'DD: ' in set_name:
            set_name = set_name.replace('DD:', 'Duel Decks:').replace('/', 'vs.')

        if "vs." in set_name and "Anthologies" not in set_name and "Anthology" not in set_name and "Duel Decks: " not in set_name:
            set_name = f"Duel Decks: {set_name}"

        if '(M)' in set_name:
            set_name = set_name.replace('(M)','').strip()
        elif '(R)' in set_name:
            set_name = set_name.replace('(R)','').strip()
        elif '(U)' in set_name:
            set_name = set_name.replace('(U)','').strip()
        elif '(C)' in set_name:
            set_name = set_name.replace('(C)','').strip()
        elif '(S)' in set_name:
            set_name = set_name.replace('(S)','').strip()
        elif '(L)' in set_name:
            set_name = set_name.replace('(L)','').strip()

        if set_name == 'Magic 2010' or set_name == '2010 Core Set' or set_name == 'Magic 2010 Core Set' or set_name == 'Magic 2010 / M10':
            set_name = 'Magic 2010 (M10)'
        elif set_name == 'Magic 2011' or set_name == '2011 Core Set' or set_name == 'Magic 2011 Core Set' or set_name == 'Magic 2011 / M11':
            set_name = 'Magic 2011 (M11)'
        elif set_name == 'Magic 2012' or set_name == '2012 Core Set' or set_name == 'Magic 2012 Core Set' or set_name == 'Magic 2012 / M12':
            set_name = 'Magic 2012 (M12)'
        elif set_name == 'Magic 2013' or set_name == '2013 Core Set' or set_name == 'Magic 2013 Core Set' or set_name == 'Magic 2013 / M13':
            set_name = 'Magic 2013 (M13)'
        elif set_name == 'Magic 2014' or set_name == '2014 Core Set' or set_name == 'Magic 2014 Core Set' or set_name == 'Magic 2014 / M14':
            set_name = 'Magic 2014 (M14)'
        elif set_name == 'Magic 2015' or set_name == '2015 Core Set' or set_name == 'Magic 2015 Core Set' or set_name == 'Magic 2015 / M15':
            set_name = 'Magic 2015 (M15)'
        elif set_name == 'Modern Masters (2013 Edition)':
            set_name = 'Modern Masters'
        elif set_name == 'Modern Masters (2015 Edition)' or set_name == 'Modern Masters 2015 Edition':
            set_name = 'Modern Masters 2015'
        elif set_name == 'Modern Masters (2017 Edition)':
            set_name = 'Modern Masters 2017'
        elif set_name == 'Unlimited':
            set_name = 'Unlimited Edition'
        elif set_name == '6th Edition':
            set_name = 'Classic Sixth Edition'
        elif set_name == '5th Edition':
            set_name = 'Fifth Edition'
        elif set_name == '4th Edition':
            set_name = 'Fourth Edition'
        elif set_name == '3rd Edition' or set_name == '3rd Edition-Revised':
            set_name = 'Revised Edition'
        elif set_name == 'Alpha':
            set_name = 'Alpha Edition'
        elif set_name == 'Beta':
            set_name = 'Beta Edition'
        elif set_name == 'Unlimited':
            set_name = 'Unlimited Edition'
        elif set_name == 'Commander Anthology 2' or set_name == 'Commander Anthology Vol. II':
            set_name = 'Commander Anthology Volume II'
        elif set_name == 'Modern Event Deck':
            set_name = 'Magic Modern Event Deck'
        elif set_name == 'Archenemy - Nicol Bolas':
            set_name = 'Archenemy: Nicol Bolas'
        elif set_name == 'Conspiracy - Take the Crown':
            set_name = 'Conspiracy: Take the Crown'
        elif set_name == 'Portal 1':
            set_name = 'Portal'
        elif set_name == 'Portal 3 Kingdoms' or set_name == 'Portal 3K' or set_name == 'Portal: Three Kingdoms':
            set_name = 'Portal Three Kingdoms'
        elif set_name == 'Portal II' or set_name == 'Portal: Second Age':
            set_name = 'Portal Second Age'
        elif set_name == 'Premium Deck Series: Fire & Lightning':
            set_name = 'Premium Deck Series: Fire and Lightning'
        elif set_name == 'Third Edition/Revised' or set_name == '3rd Edition/Revised' or set_name == 'Revised':
            set_name = 'Revised Edition'
        elif set_name == 'Commander (2011 Edition)':
            set_name = 'Commander'
        elif set_name == 'Commander (2013 Edition)':
            set_name = 'Commander 2013'
        elif set_name == 'Commander (2014 Edition)':
            set_name = 'Commander 2014'
        elif set_name == 'Commander (2015 Edition)':
            set_name = 'Commander 2015'
        elif set_name == 'Commander (2016 Edition)':
            set_name = 'Commander 2016'
        elif set_name == 'Commander (2017 Edition)':
            set_name = 'Commander 2017'
        elif set_name == 'Commander (2018 Edition)':
            set_name = 'Commander 2018'
        elif set_name == 'Commander (2019 Edition)':
            set_name = 'Commander 2019'
        elif set_name == 'Conspiracy (2014 Edition)':
            set_name = 'Conspiracy'
        elif set_name == 'Planechase (2009 Edition)' or set_name == "Planechase 2009":
            set_name = 'Planechase'
        elif set_name == 'Planechase (2012 Edition)':
            set_name = 'Planechase 2012'
        elif set_name == 'Ravnica: City of Guilds':
            set_name = 'Ravnica'
        elif set_name == 'Shadows Over Innistrad':
            set_name = 'Shadows over Innistrad'
        elif set_name == 'Journey Into Nyx':
            set_name = 'Journey into Nyx'
        elif set_name == 'ColdSnap':
            set_name = 'Coldsnap'
        elif set_name == 'Coldsnap Theme Decks':
            set_name = 'Coldsnap Theme Deck Reprints'
        elif set_name == 'Duel Decks: Elspeth Vs Tezzeret':
            set_name = 'Duel Decks: Elspeth vs. Tezzeret'
        elif set_name == 'Duel Decks:  Blessed vs. Cursed':
            set_name = 'Duel Decks: Blessed vs. Cursed'
        elif set_name == 'Duel Deck Anthology':
            set_name = 'Duel Decks: Anthology'
        elif set_name == 'From the Vault:  Lore':
            set_name = 'From the Vault: Lore'
        elif set_name == "Collectors' Edition":
            set_name = "Collector's Edition"
        elif set_name == "Collectors Ed":
            set_name = "Collector's Edition"
        elif set_name == "Collectors Ed Intl":
            set_name = "International Edition"
        elif set_name == "Collectors' Edition - International":
            set_name = "International Edition"
        elif set_name == "Masterpiece Series: Inventions":
            set_name = "Masterpiece Series: Kaladesh Inventions"
        elif set_name == "Core Set 2019 / M19":
            set_name = 'Core Set 2019'
        elif set_name == "Masterpiece Series: Mythic Edition":
            set_name = "Guilds of Ravnica: Mythic Edition"
        elif set_name == "Ravnica Allegiance: Mythic Edition":
            set_name = "Guilds of Ravnica: Mythic Edition"
        elif set_name == "Masterpiece Series: Expeditions":
            set_name = "Zendikar Expeditions"
        elif set_name == "Ultimate Box Topper":
            set_name = "Ultimate Masters: Box Toppers"
        elif set_name == "Conspiracy Take the Crown":
            set_name = "Conspiracy: Take the Crown"
        elif set_name == "Masterpiece Series: Invocations":
            set_name = "Masterpiece Series: Amonkhet Invocations"
        elif set_name == "Modern Event Deck 2014":
            set_name = "Magic Modern Event Deck"
        elif set_name == "Time Spiral - Timeshifted":
            set_name = "Timeshifted"
        elif set_name == "World Championships" or set_name == "World Championship":
            set_name = "World Championship Decks"
        elif set_name in ["Guild Kit: Dimir", "Guild Kit: Izzet", "Guild Kit: Golgari", "Guild Kit: Boros", "Guild Kit: Selesnya"]:
            set_name = "Guilds of Ravnica: Guild Kits"
        elif set_name in ["Guild Kit: Azorius", "Guild Kit: Orzhov", "Guild Kit: Rakdos", "Guild Kit: Gruul", "Guild Kit: Simic"]:
            set_name = "Ravnica Allegiance: Guild Kits"
        elif set_name == "Global Series Jiang Yanggu and Mu Yanling":
            set_name = "Global Series Jiang Yanggu & Mu Yanling"
        elif set_name == "f the Spark":
            set_name = "War of the Spark"
        elif set_name == "asters":
            set_name = "Ultimate Masters"
        elif set_name == 'n Horizons':
            set_name = 'Modern Horizons'

        if 'Duel Decks' in set_name and '.' not in set_name and 'Anthology' not in set_name:
            set_name = set_name.replace('vs', 'vs.')
        elif 'Duel Decks' in set_name and 'Anthology' in set_name and ':' not in set_name or "Duel Decks Anthology" in set_name:
            set_name = 'Duel Decks: Anthology'

        elif 'FTV:' in set_name:
            set_name = set_name.replace('FTV', 'From the Vault')

        if 'Vs.' in set_name:
            set_name = set_name.replace('Vs.', 'vs.')

        if set_name == 'Duel Decks: Phyrexia vs. The Coalition':
            set_name = 'Duel Decks: Phyrexia vs. the Coalition'

        return set_name.strip()

    def name(self, name):
        if '- FOIL' in name:
            name = name.replace('- FOIL', '').strip()

        if '//' not in name and '/' in name:
            end = name.find('/')
            name = name[0:end].strip()

        if "(Ultimate Masters Box Topper)" in name:
            name = name.replace("(Ultimate Masters Box Topper)", "")

        '''if  '(' in name:
            count = 0
            while count <len(name):
                if name[count] == '(':
                    name = name[0:count]
                else:
                    count += 1'''

        return name.strip()

    def condition(self, value):

        map_c = {
            'NM-M': 'near_mint',
            'SP': 'near_mint',
            'PLD-SP': 'played',
            'POOR': 'heavily_played',
            'DESTROYED': 'very_heavily_played'
        }

        return map_c[value]

    def is_foil(self, value):

        map_foil = {
            'Foil': True,
            'Normal': False,
        }

        return map_foil[value]
