from django.core.mail import send_mail
import functools


def report_error(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print("Exception: ", e)
            subject = f'Error for function {func.__name__}'
            message = f'Error {e} for function: :{func.__name__}"\nfilename: {func.__code__.co_filename}'
            email_from = 'tcgfirst.com'
            email_to = ('jermol.jupiter@gmail.com', )
            send_mail(subject, message, email_from, email_to)
    return wrapper
