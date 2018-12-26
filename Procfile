web: gunicorn source.wsgi
worker: celery -A source beat -l info & celery -A source worker -l info


