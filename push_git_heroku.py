from subprocess import call

call(['git', 'add', '-A'])
call(['git', 'commit', '-m', input("Change Note > ")])
call(['git', 'push', 'origin', 'master'])
call(['git', 'push', 'heroku', 'master'])


