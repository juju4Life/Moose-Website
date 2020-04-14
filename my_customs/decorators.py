import traceback
import functools
from django.core.mail import send_mail


def report_error(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            traceback_str = ''.join(traceback.format_tb(e.__traceback__))
            print(traceback_str)
            print("Exception: ", e)
            subject = f'Error for function {func.__name__}'
            message = f'Error {e} for function: {func.__name__}"\nTraceback: {traceback_str}'
            email_from = 'tcgfirst.com'
            email_to = ('jermol.jupiter@gmail.com',)
            send_mail(subject, message, email_from, email_to)

    return wrapper


def offset(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        api_call = kwargs.get('func')
        unique_identifier = kwargs.get('group_id')
        api_check = api_call(unique_identifier)
        final_list = []

        success = api_check['success']

        if success is True:
            total_items = api_check['totalItems']

            offset_num = 0
            while total_items > 0:
                data = api_call(unique_identifier, offset=offset_num)
                final_list += data['results']
                total_items -= 100
                offset_num += 100
            return final_list

    return wrapper


def time_it(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        pass





