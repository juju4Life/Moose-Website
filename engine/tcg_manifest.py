class Manifest:

    @staticmethod
    def moose_condition_map(value):

        d = {
            2: "Clean",
            3: "Played",
            4: "Heavily Played",
            6: "Unopened",
        }

        return d[value]

    def game(self, ids):
        game_dict = {
            1: 'Magic the Gathering',
            2: 'Yugioh',
            3: 'Pokemon',
            31: 'Card Sleeves',
            56: 'BUlk Lots',
            16: 'Cardfight Vanguard',
            32: 'Deck Boxes',
            27: 'Dragon Ball Super CCG',
            17: 'Force of WIll',
            29: 'Funko',
            35: 'Playmats',
            14: 'Supplies',
            22: 'TCGplayer',

        }

        return game_dict[ids]

    def printing(self, ids):
        printing_dict = {
            1: 'Normal',
            2: 'Foil',
            7: 'Unlimited',
            8: '1st Edition',
            23: 'Limited',
            10: 'Normal',
            11: 'Holofoil',
            77: 'Reverser Holofoil',
            78: '1st Edition Normal',
            79: '1st Edition Holofoil',
            46: 'Normal',
            81: 'Parallel Foil',
            52: 'Normal',
            87: 'Normal',
            26: 'Normal',
            53: 'Normal',
            31: 'Normal',
            32: 'Foil',
            48: 'Normal',
            56: 'Normal',
            38: 'Normal',


        }

        return printing_dict[ids]

    def language(self, id):
        language_dict = {
            1: 'English',
            2: 'Chinese (S)',
            3: 'Chinese (T)',
            4: 'French',
            5: 'German',
            6: 'Italian',
            7: 'Japanese',
            8: 'Korean',
            9: 'Portuguese',
            10: 'Russian',
            11: 'Spanish',
        }
        return language_dict[id]

    def order_type(self, key):

        manifester = {
            0: 'Unknown',
            1: 'Normal',
            2: 'Direct',
        }

        return manifester[key]

    def order_channel_type(self, key):
        manifester = {
            0: 'Marketplace',
            1: 'Website',
            1000: 'Unknown',
        }

        return manifester[key]

    def order_status_type(self, key):
        manifester = {
            0: 'Unknown',
            1: 'Processing',
            2: 'Ready to Ship',
            3: 'Shipped',
            4: 'Delivered',
            5: 'Cancelled',
        }
        return manifester[key]

    def order_pickup_status(self, key):
        manifester = {
            0: 'Unknown',
            1: 'Received',
            2: 'Pulling',
            3: 'Ready for Pickup',
            4: 'Picked Up',
            5: 'Cancelled',
        }

        return manifester[key]

    def order_delivery_types(self, key):
        manifester = {
            0: 'Unknown',
            1: 'Standard',
            2: 'Expedited',
            3: 'International',
            4: 'In-Store Pickup',
        }

        return manifester[key]

    def order_presale_status_type(self, key):
        manifester = {
            0: 'Unknown',
            1: 'Non-Presale',
            2: 'Presale',
            3: 'Presale: Shippable',
        }

        return manifester[key]

    def order_refund_type(self, key):
        manifester = {
            0: 'Unknown',
            1: 'Full',
            2: 'Partial',
        }

        return manifester[key]


    def condition(self, id):

        condition_dict = {
            1: 'Near Mint',
            2: 'Lightly Played',
            3: 'Moderately Played',
            4: 'Heavily Played',
            5: 'Damaged',
            6: 'Unopened',

        }
        return condition_dict[id]

    def expansion(self, id):

        expansion_dict = {
            2334: "Guilds of Ravnica: Guild Kits",
            2290: "Guilds of Ravnica",
            2251: "Commander 2018",
            2250: "Core Set 2019",
            2247: "Global Series Jiang Yanggu & Mu Yanling",
            2220: "Signature Spellbook: Jace",
            2245: "Battlebond",
            2246: "Commander Anthology Volume II",
            2199: "Dominaria",
            2203: "Challenger Decks",
            2207: "Duel Decks: Elves vs. Inventors",
            2189: "Masters 25",
            2098: "Rivals of Ixalan",
            2092: "Unstable",
            2077: "Explorers of Ixalan",
            2078: "From the Vault: Transform",
            2050: "Iconic Masters",
            2076: "Duel Decks: Merfolk vs. Goblins",
            2084: "Gift Boxes and Promos",
            2087: "League Promos",
            2043: "Ixalan",
            2067: "Standard Showdown Promos",
            2009: "Commander 2017",
            1934: "Hour of Devastation",
            1904: "Archenemy: Nicol Bolas",
            1933: "Commander Anthology",
            1882: "Amonkhet",
            1909: "Masterpiece Series: Amonkhet Invocations",
            2045: "Open House Promos",
            1930: "Welcome Deck 2017",
            1905: "Duel Decks: Mind vs. Might",
            1879: "Modern Masters 2017",
            1857: "Aether Revolt",
            1793: "Planechase Anthology",
            1792: "Commander 2016",
            1791: "Kaladesh",
            1837: "Masterpiece Series: Kaladesh Inventions",
            1835: "Duel Decks: Nissa vs. Ob Nixilis",
            1794: "Conspiracy: Take the Crown",
            1821: "From the Vault: Lore",
            1832: "WMCQ Promo Cards",
            1790: "Eldritch Moon",
            1740: "Eternal Masters",
            1708: "Shadows over Innistrad",
            1765: "Welcome Deck 2016",
            1726: "Duel Decks: Blessed vs. Cursed",
            1693: "Oath of the Gatewatch",
            1673: "Commander 2015",
            1645: "Battle for Zendikar",
            1649: "Zendikar Expeditions",
            1641: "Duel Decks: Zendikar vs. Eldrazi",
            1577: "From the Vault: Angels",
            1512: "Magic Origins",
            1503: "Modern Masters 2015",
            1515: "Dragons of Tarkir",
            1520: "Tarkir Dragonfury Promos",
            1511: "Duel Decks: Elspeth vs. Kiora",
            1497: "Fate Reforged",
            1507: "Ugin's Fate Promos",
            1490: "Duel Decks: Anthology",
            1476: "Commander 2014",
            1356: "Khans of Tarkir",
            1293: "Magic 2015 (M15)",
            1277: "Journey Into Nyx",
            1144: "Theros",
            1524: "Hero's Path Promos",
            569: "Gatecrash",
            370: "Return to Ravnica",
            100: "Scars of Mirrodin",
            69: "Magic 2011 (M11)",
            12: "Archenemy",
            98: "Rise of the Eldrazi",
            122: "Worldwake",
            124: "Zendikar",
            2156: "Buy-A-Box Promos",
            68: "Magic 2010 (M10)",
            1274: "Duels of the Planeswalkers",
            5: "Alara Reborn",
            26: "Conflux",
            103: "Shards of Alara",
            39: "Eventide",
            102: "Shadowmoor",
            77: "Morningtide",
            53: "WPN & Gateway Promos",
            67: "Lorwyn",
            52: "Game Day & Store Championship Promos",
            1: "10th Edition",
            51: "Future Sight",
            54: "Grand Prix Promos",
            83: "Planar Chaos",
            104: "Special Occasion",
            93: "Pro Tour Promos",
            110: "Time Spiral",
            111: "Timeshifted",
            24: "Coldsnap",
            1348: "Coldsnap Theme Deck Reprints",
            28: "Dissension",
            21: "Champs Promos",
            55: "Guildpact",
            369: "Magic Premiere Shop",
            95: "Ravnica",
            4: "9th Edition",
            99: "Saviors of Kamigawa",
            18: "Betrayers of Kamigawa",
            114: "Unhinged",
            20: "Champions of Kamigawa",
            43: "Fifth Dawn",
            27: "Darksteel",
            75: "Mirrodin",
            1874: "Launch Party & Release Event Promos",
            101: "Scourge",
            3: "8th Edition",
            66: "Legions",
            81: "Onslaught",
            63: "Judgment",
            112: "Torment",
            82: "Oversize Cards",
            80: "Odyssey",
            10: "Apocalypse",
            71: "Magic Player Rewards",
            2: "7th Edition",
            85: "Planeshift",
            60: "Invasion",
            94: "Prophecy",
            106: "Starter 2000",
            78: "Nemesis",
            38: "European Lands",
            45: "FNM Promos",
            73: "Mercadian Masques",
            56: "Guru Lands",
            1163: "Unique and Miscellaneous Promos",
            116: "Urza's Destiny",
            61: "JSS/MSS Promos",
            62: "Judge Promos",
            88: "Portal Three Kingdoms",
            23: "Classic Sixth Edition",
            105: "Starter 1999",
            117: "Urza's Legacy",
            72: "Media Promos",
            1275: "Anthologies",
            118: "Urza's Saga",
            9: "APAC Lands",
            113: "Unglued",
            40: "Exodus",
            87: "Portal Second Age",
            107: "Stronghold",
            108: "Tempest",
            92: "Prerelease Cards",
            2198: "World Championship Decks",
            121: "Weatherlight",
            86: "Portal",
            119: "Vanguard",
            44: "Fifth Edition",
            120: "Visions",
            74: "Mirage",
            13: "Arena Promos",
            6: "Alliances",
            57: "Homelands",
            58: "Ice Age",
            46: "Fourth Edition",
            22: "Chronicles",
            41: "Fallen Empires",
            109: "The Dark",
            65: "Legends",
            97: "Revised Edition",
            8: "Antiquities",
            115: "Unlimited Edition",
            1526: "Collector's Edition",
            1527: "International Edition",
            17: "Beta Edition",
            7: "Alpha Edition",
            1276: "Born of the Gods",
            1113: "Magic 2014 (M14)",
            570: "Dragon's Maze",
            364: "Magic 2013 (M13)",
            362: "Avacyn Restored",
            125: "Dark Ascension",
            59: "Innistrad",
            70: "Magic 2012 (M12)",
            79: "New Phyrexia",
            76: "Mirrodin Besieged",
            1111: "Modern Masters",
            11: "Arabian Nights",
            568: "Commander's Arsenal",
            1164: "Commander 2013",
            25: "Commander",
            363: "Planechase 2012",
            84: "Planechase",
            1346: "Magic Modern Event Deck",
            1312: "Conspiracy",
            1477: "Duel Decks: Speed vs. Cunning",
            1166: "Duel Decks: Jace vs. Vraska",
            1145: "Duel Decks: Heroes vs. Monsters",
            601: "Duel Decks: Sorin vs. Tibalt",
            365: "Duel Decks: Izzet vs. Golgari",
            367: "Duel Decks: Venser vs. Koth",
            30: "Duel Decks: Ajani vs. Nicol Bolas",
            36: "Duel Decks: Knights vs. Dragons",
            32: "Duel Decks: Elspeth vs. Tezzeret",
            37: "Duel Decks: Phyrexia vs. the Coalition",
            34: "Duel Decks: Garruk vs. Liliana",
            31: "Duel Decks: Divine vs. Demonic",
            35: "Duel Decks: Jace vs. Chandra",
            33: "Duel Decks: Elves vs. Goblins",
            1475: "From the Vault: Annihilation",
            1141: "From the Vault: Twenty",
            368: "From the Vault: Realms",
            49: "From the Vault: Legends",
            50: "From the Vault: Relics",
            48: "From the Vault: Exiled",
            47: "From the Vault: Dragons",
            90: "Premium Deck Series: Graveborn",
            89: "Premium Deck Series: Fire and Lightning",
            91: "Premium Deck Series: Slivers",
            1311: "Deckmasters Garfield vs Finkel",
            16: "Beatdown Box Set",
            15: "Battle Royale Box Set",
            14: "Astral",
            19: "Box Sets",
            29: "Duel Decks",
            1688: "Fourth Edition (Foreign Black Border)",
            1687: "Fourth Edition (Foreign White Border)",
            1689: "Revised Edition (Foreign Black Border)",
            1690: "Revised Edition (Foreign White Border)",

        }
        try:
            return expansion_dict[id]
        except KeyError:
            return "POK/YUG/New MTG Set"
