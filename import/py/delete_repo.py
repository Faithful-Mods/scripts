import os
import sys
from github import Github
from github import BadCredentialsException
from getpass import getpass

try:
	with open('../user_settings/token_github.txt','r') as token_file:
		token = token_file.read()
except FileNotFoundError:
	token = getpass('Give your GitHub token to continue: ')
	print('Token saved under /user_settings into token_github.txt')
	with open('../user_settings/token_github.txt', 'a') as token_file:
		token_file.write(token)

# login to github API
g = Github(token)

repo = g.get_repo(f"Faithful-Mods/{sys.argv[1]}")
repo.delete()

print(f'Sucessfully deleted : {sys.argv[1]}')