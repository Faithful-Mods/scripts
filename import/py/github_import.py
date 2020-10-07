import os
import sys
import base64
from github import Github
from github import InputGitTreeElement
from github import BadCredentialsException
from getpass import getpass

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

EXIT_FAIL   = 1
EXIT_SUCESS = 0

def main(AskedBranch):
	onlyfiles = next(os.walk('resources'))[1]
	NBFiles   = len(onlyfiles) # and not onlyfans :)

	## CHECK IF FILES IN /RESOURCES HAVE BEEN ADDED
	if NBFiles == 0:
		print(bcolors.FAIL + 'You need to place all your mods resource in the /resources folder following this : "/resources/<asset_name>/..."\nEx: /resources/botania/...' + bcolors.ENDC)
		return EXIT_FAIL

	## LOGIN TO GITHUB API WITH TOKEN
	# try to load token from settings, ask user if not found
	try:
		with open('../user_settings/token_github.txt','r') as token_file:
			token = token_file.read()
	except FileNotFoundError:
		token = getpass('Give your GitHub token to continue: ')
		print('Token saved under /user_settings into token_github.txt')
		with open('../user_settings/token_github.txt', 'a') as token_file:
			token_file.write(token)

	# load to github API
	g = Github(token)

	# load repos -> need authentification in github API -> if fail : wrong token
	try:
		# looping in /resources for all files
		for FileName in onlyfiles:
			print('Watching :',FileName)

			# try to find an existing repository
			try:
				repo = g.get_repo(f"Faithful-Mods/{FileName}")
			except:
				print('[x] -> Repository not found, creating one...')

				# Information used in mods.json (mods list) & GitHub repos:
				MOD_NAME    = input('      - Mod Name       : ')
				MOD_URL     = input('      - CurseForge URL : ')
				MOD_NAME_CF = MOD_URL.replace('https://www.curseforge.com/minecraft/mc-mods/','')
				print('      - CurseForge img :',MOD_NAME_CF)

				# Create a new repository: 
				organization = g.get_organization("Faithful-Mods")
				organization.create_repo(
					FileName, 
					description=f"Official {MOD_NAME} Faithful Resource Pack", 
					homepage=MOD_URL, 
					private=True, 
					delete_branch_on_merge=False
				)

				repo = g.get_repo(f"Faithful-Mods/{FileName}")
				# initial commit : used to create a default branch -> allow us to add a new branch (if not: the repo is "empty")
				repo.create_file("initialcommit.txt", "initial commit", "")
				init = repo.get_contents("initialcommit.txt")
				repo.delete_file(init.path, "remove useless file", init.sha, branch='main')

			print('[v] -> Repository found, checking branches...')

			# try to find the right branch : if not found -> create a new one
			try:
				repo.get_branch(branch=AskedBranch)
			except:
				print('[x] -> Branch not found, creating one...')
				# Why GitHub ??!
				try:
					sb = repo.get_branch('main') # since 1st october 2020, every new repo as main as default branch instead of master
				except:
					sb = repo.get_branch('master')

				repo.create_git_ref(ref='refs/heads/' + AskedBranch, sha=sb.commit.sha)

			print('[v] -> Branch found, looking for files to push...')

			file_list  = ['resources\\pack.mcmeta','resources\\pack.png']
			file_names = ['pack.mcmeta','pack.png']

			# get all files inside mod resource pack
			for root, dirs, files in os.walk(f'resources\\{FileName}'):
				for file_name in files:
					file_list.append(os.path.join(root, file_name)) #path
					file_names.append(file_name)                    #names

			for i in range(0,len(file_list)):
				print(f'       Found file : {file_names[i]} in {file_list[i]}')

			commit_message = 'upload files'
			master_ref     = repo.get_git_ref(ref='refs/heads/' + AskedBranch)
			master_sha     = master_ref.object.sha
			base_tree      = repo.get_git_tree(master_sha)

			element_list = list()

			for entry in file_list:
				with open(entry, 'rb') as input_file:
					data = input_file.read()

					##### PNG FILES ARE NOT TAKEN INTO ACCOUNT #####

				element = InputGitTreeElement(entry, '100644', 'blob', data)
				element_list.append(element)
			
			tree   = repo.create_git_tree(element_list, base_tree)
			parent = repo.get_git_commit(master_sha)
			commit = repo.create_git_commit(commit_message, tree, [parent])
			master_ref.edit(commit.sha)

	except BadCredentialsException:
		print(bcolors.FAIL + 'Wrong Token has been given, change it in your local files : /user_settings/token_github.txt' + bcolors.ENDC)
		return EXIT_FAIL
	else:
		return EXIT_SUCESS

main(sys.argv[1])