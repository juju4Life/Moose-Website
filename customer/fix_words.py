

class FixWords:

    def fix_name(self, name):
        return ' '.join(name.split()).lower()

    def fix_set(self, set_name):

        if set_name == 'm10' or set_name == 'magic 2010':
            set_name = 'Magic 2010 (M10)'
        elif set_name == 'm11' or set_name == 'magic 2011':
            set_name = 'Magic 2011 (M11)'
        elif set_name == 'm12' or set_name == 'magic 2012':
            set_name = 'Magic 2012 (M12)'
        elif set_name == 'm13' or set_name == 'magic 2013':
            set_name = 'Magic 2013 (M13)'
        elif set_name == 'm14' or set_name == 'magic 2014':
            set_name = 'Magic 2014 (M14)'
        elif set_name == 'm15' or set_name == 'magic 2015':
            set_name = 'Magic 2015 (M15)'
        elif set_name == 'm19' or set_name == 'magic 2019':
            set_name = 'Core Set 2019'
        elif 'vs' in set_name:
            set_name = 'Duel Decks: {}'.format(set_name.replace('vs', 'vs.'))
        elif set_name == '6th edition':
            set_name = 'Classic Sixth Edition'
        elif set_name == '5th edition':
            set_name = 'Fifth Edition'
        elif set_name == '4th edition':
            set_name = 'Fourth Edition'
        elif set_name == '3rd edition' or set_name == 'revised':
            set_name = 'Revised Edition'
        elif set_name == 'unlimited':
            set_name = 'Unlimited Edition'
        return set_name

    def fix_month(self, text):
        if 'january' in text or text[0:2] == '1/' in text or int(text) == 1 or text == '1':
            text = 'January'
        elif 'february' in text or text[0:2] == '2/' in text or int(text) == 2 or text == '2':
            text = 'February'
        elif 'march' in text or text[0:2] == '3/' in text or int(text) == 3 or text == '3':
            text = 'March'
        elif 'april' in text or text[0:2] == '4/' in text or int(text) == 4 or text == '4':
            text = 'April'
        elif 'may' in text or text[0:2] == '5/' in text or int(text) == 5 or text == '5':
            text = 'May'
        elif 'june' in text or text[0:2] == '6/' in text or int(text) == 6 or text == '6':
            text = 'June'
        elif 'july' in text or text[0:2] == '7/' in text or int(text) == 7 or text == '7':
            text = 'July'
        elif 'august' in text or text[0:2] == '8/' in text or int(text) == 8 or text == '8':
            text = 'August'
        elif 'september' in text or text[0:2] == '9/' in text or int(text) == 9 or text == '9':
            text = 'September'
        elif 'october' in text or text[0:3] == '10/' in text or int(text) == 10 or text == '10':
            text = 'October'
        elif 'november' in text or text[0:3] == '11/' in text or int(text) == 11 or text == '11':
            text = 'November'
        elif 'december' in text or text[0:3] == '12/' in text or int(text) == 12 or text == '12':
            text = 'December'
        return text.strip()


    def month_to_integer(self, month):
        if month == 'january':
            month = 1
        elif month == 'february':
            month = 2
        elif month == 'march':
            month = 3
        elif month == 'april':
            month = 4
        elif month == 'may':
            month = 5
        elif month == 'june':
            month = 6
        elif month == 'july':
            month = 7
        elif month == 'august':
            month = 8
        elif month == 'september':
            month = 9
        elif month == 'october':
            month = 10
        elif month == 'november':
            month = 11
        elif month == 'december':
            month = 12
        return month




