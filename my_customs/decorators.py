from django.core.mail import send_mail


def report_error(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            subject = f'Error for function {func.__name__}'
            message = f'Error {e} for function {func.__name__}'
            email_from = 'tcgfirst.com'
            email_to = 'jermol.jupiter.com'
            send_mail(subject, message, email_from, email_to)
    return wrapper
