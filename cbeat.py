from subprocess import call

call(['celery', '-A', 'source', 'beat', '-l', 'info'])

