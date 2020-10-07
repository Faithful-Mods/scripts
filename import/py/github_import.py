import os
import sys
import json
import base64
import requests
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

	# login to github API
	g = Github(token)

	# load repos -> need authentification in github API -> if fail : wrong token
	try:
		# looping in /resources for all files
		for FileName in onlyfiles:

			EXIST_ALREADY_REPO   = True
			EXIST_ALREADY_BRANCH = True

			print('Watching :',FileName)

			# try to find an existing repository
			try:
				repo = g.get_repo(f"Faithful-Mods/{FileName}")
			except:
				EXIST_ALREADY_REPO = False
				print('[' + bcolors.FAIL + 'x' + bcolors.ENDC + '] -> Repository not found, creating one...')

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
				# initial commit
				repo.create_file("initialcommit.txt", "initial commit", "")
				init = repo.get_contents("initialcommit.txt")

			print('[' + bcolors.OKGREEN + 'v' + bcolors.ENDC + '] -> Repository found, looking for branch...')

			# try to find the right branch : if not found -> create a new one
			try:
				repo.get_branch(branch=AskedBranch)
			except:
				EXIST_ALREADY_BRANCH = False

				print('[' + bcolors.FAIL + 'x' + bcolors.ENDC + '] -> Branch not found, creating one...')

				try:
					sb = repo.get_branch(repo.default_branch)
				except:
					print(bcolors.FAIL + 'Something went wrong when getting default branch' + bcolors.ENDC)
					return EXIT_FAIL
	
				repo.create_git_ref(ref='refs/heads/' + AskedBranch, sha=sb.commit.sha)
				# create a new branch : copied from default branch : need to be cleaned
				url = f"https://api.github.com/repos/Faithful-Mods/{FileName}/git/trees/{AskedBranch}?recursive=1"
				res = requests.get(url).json()
				
				### NEED TO FIND A WAY TO DELETE ALL FILES IN THE SAME COMMIT : LESS TIME CONSUMER
				## it actually make a commit for each deleted file
				for file in res["tree"]:
					if file["path"] != 'pack.png':
						try:
							repo.delete_file(file["path"], "remove files from the main branch", file["sha"], branch=AskedBranch)
						except:
							pass
				
			print('[' + bcolors.OKGREEN + 'v' + bcolors.ENDC + '] -> Branch found, looking for files to push...')

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

			master_ref = repo.get_git_ref(f'heads/{AskedBranch}')

			master_sha   = master_ref.object.sha
			base_tree    = repo.get_git_tree(master_sha)
			element_list = list()

			for i, entry in enumerate(file_list):
				print(f'       Adding file n°{i+1} : {entry}')
				
				if entry.endswith('.png'):
					with open(entry, 'rb') as input_file:
						data = input_file.read()

					blob = repo.create_git_blob(str(base64.b64encode(data)).replace("b'","").replace("'",""), 'base64')
				
				else:
					with open(entry, encoding='utf-8', errors='ignore') as input_file:
						data = input_file.read()
					
					blob = repo.create_git_blob(str(data),'utf-8')

				if entry == 'resources\\pack.mcmeta'or entry == 'resources\\pack.png':
					entry = entry.replace('resources\\', '')

				element = InputGitTreeElement(path=entry.replace('resources','assets').replace('\\','/'), mode='100644', type='blob', sha=blob.sha)
				element_list.append(element)

			print(bcolors.OKBLUE + '       Sending commit' + bcolors.ENDC)
			tree = repo.create_git_tree(element_list, base_tree)
			parent = repo.get_git_commit(master_sha)
			commit = repo.create_git_commit(commit_message, tree, [parent])
			master_ref.edit(commit.sha)
			
			try:
				#delete initial commit when the repo has been created
				repo.delete_file(init.path, "remove useless file", init.sha, branch=AskedBranch)
			except:
				pass

			try:
				#delete initial commit when the repo has been created
				repo.delete_file(init.path, "remove useless file", init.sha, branch=repo.default_branch)
			except:
				pass


			# the branch doesn't exist and have been created : adding it to mods list file 
			if EXIST_ALREADY_BRANCH == False:
				# only branch need to be added:
				if EXIST_ALREADY_REPO == True:
					ModData = { "isNew": False, "branch": AskedBranch }
				else:
					ModData = { "isNew": True, "name": [ MOD_NAME, FileName, MOD_NAME_CF ], "branch": AskedBranch }

				with open('resources/mods.json', 'r+') as ModList:
					if ModList.read() != '':
						ModList.write(',\n')
					json.dump(ModData, ModList)

			# update repo topics :
			

			#os.remove(f'resources/{FileName}')

	except BadCredentialsException:
		print(bcolors.FAIL + 'Wrong Token has been given, change it in your local files : /user_settings/token_github.txt' + bcolors.ENDC)
		return EXIT_FAIL
	else:
		return EXIT_SUCESS

main(sys.argv[1])