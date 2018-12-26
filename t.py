from subprocess import call

call(['git', 'add', '-A'])
call(['git', 'commit', '-m', '"changes made"'])
call(['git', 'push', 'origin', 'master'])
call(['git', 'push', 'heroku', 'master'])
