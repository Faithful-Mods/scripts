import os
import sys
import json
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

def GetToken():
	try:
		with open('../user_settings/token_github.txt','r') as token_file:
			token = token_file.read()
	except FileNotFoundError:
		token = getpass('Give your GitHub token to continue: ')
		print('Token saved under /user_settings into token_github.txt')
		with open('../user_settings/token_github.txt', 'a') as token_file:
			token_file.write(token)

	return token

def UpdateTopics(USER,FILENAME):
	TOPICS = list()
	TOPICS.append(FILENAME)

	REPOSITORY = USER.get_repo(f'Faithful-Mods/{FILENAME}')
	BRANCHES = REPOSITORY.get_branches()

	for BRANCH in BRANCHES:
		if BRANCH.name != 'main':
			TOPICS.append(BRANCH.name.replace('.','-'))

	REPOSITORY.replace_topics(TOPICS)

	return EXIT_SUCESS

def CommitToGitHub(USER,FILENAME,ASKED_BRANCH):

	MOD_NAME    = ''
	MOD_NAME_CF = ''

	## FIRST : TEST IF REPO EXIST
	try:
		USER.get_repo(f"Faithful-Mods/{FILENAME}")
	except:
		print('[' + bcolors.FAIL + 'x' + bcolors.ENDC + '] -> Repository not found, creating one...')

		# Information used in mods.json (mods list) & GitHub repos:
		MOD_NAME    = input('      - Mod Name       : ')
		MOD_URL     = input('      - CurseForge URL : ')
		MOD_NAME_CF = MOD_URL.replace('https://www.curseforge.com/minecraft/mc-mods/','')
		print('      - CurseForge img :',MOD_NAME_CF)

		# Create a new repository: 
		ORGANIZATION = USER.get_organization("Faithful-Mods")
		ORGANIZATION.create_repo(
			FILENAME, 
			description=f"Official {MOD_NAME} Faithful Resource Pack", 
			homepage=MOD_URL, 
			private=False, 
			delete_branch_on_merge=False
		)

		# create default branch with first commit :
		REPOSITORY = USER.get_repo(f'Faithful-Mods/{FILENAME}')
		REPOSITORY.create_file("initialcommit", "", "")
		
		# reload
		print('[' + bcolors.OKBLUE + 'o' + bcolors.ENDC + '] -> Reloading...')
		CommitToGitHub(USER,FILENAME,ASKED_BRANCH)
	else:
		print('[' + bcolors.OKGREEN + 'v' + bcolors.ENDC + '] -> Repository found, checking branches...')
		REPOSITORY = USER.get_repo(f'Faithful-Mods/{FILENAME}')

		## THEN : test if the asked branch exist:
		try:
			REPOSITORY.get_branch(branch=ASKED_BRANCH)
		except:
			print('[' + bcolors.FAIL + 'x' + bcolors.ENDC + '] -> Branch not found, creating one...')
			DEFAULT_BRANCH = REPOSITORY.get_branch(REPOSITORY.default_branch)
			REPOSITORY.create_git_ref(ref='refs/heads/' + ASKED_BRANCH, sha=DEFAULT_BRANCH.commit.sha)

			# reload
			print('[' + bcolors.OKBLUE + 'o' + bcolors.ENDC + '] -> Reloading...')
			CommitToGitHub(USER,FILENAME,ASKED_BRANCH)
		else:
			print('[' + bcolors.OKGREEN + 'v' + bcolors.ENDC + '] -> Branch found, commit files to branch...')
			
			## FINALLY : UPLOAD FILES INTO ASSET MOD FILE TO GITHUB
			FILESLIST = ['resources\\pack.mcmeta','resources\\pack.png']
			FILESNAME = ['pack.mcmeta','pack.png']

			# get all files inside mod resource pack
			for PATH, _, FILES in os.walk(f'resources\\{FILENAME}'):
				for FILE in FILES:
					FILESLIST.append(os.path.join(PATH, FILE)) #path into path list
					FILESNAME.append(FILE)                     #name into names list

					print(f'       Found : {FILE} in {PATH+FILE}')

			BRANCH_REF  = REPOSITORY.get_git_ref(f'heads/{ASKED_BRANCH}')
			BRANCH_SHA  = BRANCH_REF.object.sha
			BRANCH_TREE = REPOSITORY.get_git_tree(BRANCH_SHA)

			ELEMENTS_LIST = list()

			for i, ENTRY in enumerate(FILESLIST):
				print(f'       Adding file n°{i+1} : {ENTRY}')
					
				if ENTRY.endswith('.png'):
					with open(ENTRY, 'rb') as FILE:
						DATA = FILE.read()
					BLOB = REPOSITORY.create_git_blob(str(base64.b64encode(DATA)).replace("b'","").replace("'",""), 'base64')
						
				else:
					with open(ENTRY, 'r') as FILE:
						DATA = FILE.read()
					BLOB = REPOSITORY.create_git_blob(str(DATA),'utf-8')

				if ENTRY == 'resources\\pack.mcmeta'or ENTRY == 'resources\\pack.png':
					ENTRY = ENTRY.replace('resources\\', '')

				ELEMENTS_LIST.append(InputGitTreeElement(path=ENTRY.replace('resources','assets').replace('\\','/'), mode='100644', type='blob', sha=BLOB.sha))
					
			print(bcolors.OKBLUE + '       Sending commit' + bcolors.ENDC)
				
			NEW_BRANCH_TREE = REPOSITORY.create_git_tree(ELEMENTS_LIST, BRANCH_TREE)
			COMMIT = REPOSITORY.create_git_commit('Upload files from script', NEW_BRANCH_TREE, [REPOSITORY.get_git_commit(BRANCH_SHA)])
			BRANCH_REF.edit(COMMIT.sha)

			print(bcolors.OKGREEN + '       Commit sucessfully sent' + bcolors.ENDC)

			try:
				REPOSITORY.delete_file("initialcommit", "", REPOSITORY.get_contents("initialcommit").sha, branch=ASKED_BRANCH)
			except:
				pass

	return REPOSITORY, MOD_NAME, MOD_NAME_CF


############ EXPERIMENTAL : NEVER TESTED ############
def AddToModList(REPOSITORY,PATH,MC_VERSION,MOD_NAME,MOD_NAME_CF,MOD_ASSET_NAME):
	with open(PATH, 'r') as FILE:
		data = json.loads(FILE.read())

	BRANCHES = REPOSITORY.get_branches()
	totalmod = len(data)
	modpos = -1
	verpos = -1

	for i in range(0,totalmod):
		# check if MOD_ASSET_NAME is already in the mods list:
		if data[i]['name'][1] == MOD_ASSET_NAME:
			modpos = i
			break
	
	# IF MODLIST DOES NOT HAVE MOD YET:
	if modpos == -1:

		print('mod not found in modlist, commit needed...')

		# add versions:
		versions = []
		for BRANCH in BRANCHES:
			if BRANCH.name != 'main':
				versions.append(BRANCH.name)
		versions.reverse()

		# add mod to modlist json
		data.append({"name": [ MOD_NAME, MOD_ASSET_NAME, MOD_NAME_CF ], "versions": versions, "repository": "Faithful-Mods"})

		# sort mod list :
		tmp = []
		for i in range(0,totalmod+1):
			tmp.append(data[i])
		tmp = sorted(tmp)
		data = [tmp]
		print(data)

		# DOES NOT WORK YET	data = sorted(dict(data))

		commit = True

	# IF MODLIST ALREADY HAVE THE MOD :
	else:
		print('mod found in modlist, checking minecraft versions...')

		# THEN CHECK IF MOD MODLIST ALREADY HAVE MC VERSION
		for i in range(0,len(data[modpos]['versions'])):
			if data[modpos]['versions'][i] == MC_VERSION:
				print('minecraft version found, commit not needed')
				verpos = i
				commit = False
				break

		# MODLIST DOES NOT HAVE MC VERSION FOR THAT MOD:
		if verpos == -1 :
			print('minecraft version not found, commit needed')
			commit = True

			versions = []
			for BRANCH in BRANCHES:
				if BRANCH.name != 'main':
					versions.append(BRANCH.name)
			versions.reverse()
			data[modpos]['versions'] = versions

	if commit == True:
		with open(PATH, 'w') as FILE:
			json.dump(data, FILE)

		# UPDATE mods.json IN REPOSITORY
		USER = Github(GetToken())
		WEBSITE_REPOSITORY = USER.get_repo('Faithful-Mods/faithful-mods.github.io')
		BRANCH_REF  = WEBSITE_REPOSITORY.get_git_ref(f'heads/master')
		BRANCH_SHA  = BRANCH_REF.object.sha
		BRANCH_TREE = WEBSITE_REPOSITORY.get_git_tree(BRANCH_SHA)

		ELEMENTS_LIST = list()
			
		with open(PATH, 'r') as FILE:
			DATA = FILE.read()
		BLOB = WEBSITE_REPOSITORY.create_git_blob(str(DATA),'utf-8')
		ELEMENTS_LIST.append(InputGitTreeElement(path='data/modsTESTSCRIPT.json', mode='100644', type='blob', sha=BLOB.sha))

		print('Adding mod to modlist')
		NEW_BRANCH_TREE = WEBSITE_REPOSITORY.create_git_tree(ELEMENTS_LIST, BRANCH_TREE)
		COMMIT = WEBSITE_REPOSITORY.create_git_commit(f'Added {MOD_ASSET_NAME} mods for {MC_VERSION}', NEW_BRANCH_TREE, [WEBSITE_REPOSITORY.get_git_commit(BRANCH_SHA)])
		BRANCH_REF.edit(COMMIT.sha)
		print('Mod added to modlist')

	return EXIT_SUCESS

def main(BRANCH,PATH):

	## GET FILES IN /RESOURCES FOLDER
	FILESLIST = next(os.walk('resources'))[1]
	NB_FILES  = len(FILESLIST)

	# if there is no file in the directory
	if NB_FILES == 0:
		print(bcolors.FAIL + 'You need to place all your mods resource in the /resources folder following this : "/resources/<asset_name>/..."\nEx: /resources/botania/...' + bcolors.ENDC)
		return EXIT_FAIL

	## LOGIN TO GITHUB API w/ TOKEN
	USER = Github(GetToken())

	# test if user gave a valid token
	try:
		USER.get_repo(f"Faithful-Mods/faithful-mods.github.io")
	except BadCredentialsException:
		print(bcolors.FAIL + 'Invalid Token provided, please update this file /user_settings/token_github.txt with a valid token')
		return EXIT_FAIL
	else:

		## INSERT TITLE HERE
		for FILENAME in FILESLIST:
			print(f' => WATCHING {FILENAME} :')
			REPOSITORY, MOD_NAME, MOD_NAME_CF = CommitToGitHub(USER,FILENAME,BRANCH)
			UpdateTopics(USER,FILENAME)
			AddToModList(REPOSITORY,PATH,BRANCH,MOD_NAME,MOD_NAME_CF,FILENAME)

main(sys.argv[1],sys.argv[2])