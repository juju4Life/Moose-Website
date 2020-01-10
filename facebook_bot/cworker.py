from subprocess import call

call(['celery', '-A', 'source', 'worker', '-l', 'info', '-P', 'eventlet'])

