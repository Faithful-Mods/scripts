import os
import sys
import base64
from github import Github
from github import InputGitTreeElement
from getpass import getpass

def main(AskedBranch,GHusername,GHpassword):
	onlyfiles = next(os.walk('resources'))[1]
	NBFiles   = len(onlyfiles) # and not onlyfans :)

	# check if files have been placed in the /resources folder
	if NBFiles == 0:
		print('You need to place all your mods resource in the /resources folder following this : "/resources/<asset_name>/..."')
		print('Ex: /resources/botania/...')
		return 0

	try:
		g = Github(GHusername,GHpassword)
	except github.BadCredentialsException: # doesn't work :/
		print('Invalid password or GitHub username')
		return 0
	else:
		repos = g.get_user().get_repos()

		for FileName in onlyfiles:
			print('Watching :',FileName)

			try:
				repo = g.get_repo(f"Faithful-Mods/{FileName}")

			## REPOSITORY DOES NOT EXIST
			except:
				print('[x] -> Repository not found, creating one...')

				# Information used in mods.json (mods list) & GitHub repos:
				ModName   = input('      - Mod Name       : ')
				ModURL    = input('      - CurseForge URL : ')
				ModNameCF = ModURL.replace('https://www.curseforge.com/minecraft/mc-mods/','')
				print('      - CurseForge img :',ModNameCF)

				# Create a new repository: 
				organization = g.get_organization("Faithful-Mods")
				organization.create_repo(
					FileName, 
					description=f"Official {ModName} Faithful Resource Pack", 
					homepage=ModURL, 
					private=True, 
					
					delete_branch_on_merge=False
				)

				## INITIAL COMMIT -> create the default branch
				repo = g.get_repo(f"Faithful-Mods/{FileName}")
				repo.create_file("initialcommit.txt", "initial commit", "")

			repo = g.get_repo(f"Faithful-Mods/{FileName}")

			## REPOSITORY ALREADY EXIST OR HAS BEEN CREATED
			print('[v] -> Repository found, checking branches...')
			try:
				repo.get_branch(branch=AskedBranch)

			### BRANCH DOES NOT EXIST
			except:
				print('[x] -> Branch not found, creating one...')

				# create a new branch
				try:
					sb = repo.get_branch('main') # since 1st october 2020, every new repo as main as default branch instead of master
				except:
					sb = repo.get_branch('master')

				repo.create_git_ref(ref='refs/heads/' + AskedBranch, sha=sb.commit.sha)

			### BRANCH ALREADY EXIST OR HAS BEEN CREATED
			## IMPORT FILES
			print('[v] -> Branch found, looking for files to push...')

			file_list  = []
			file_names = []

			for root, dirs, files in os.walk(f'resources\\{FileName}'):
				for file_name in files:
					file_list.append(os.path.join(root, file_name)) #path
					file_names.append(file_name)                    #names

			for i in range(0,len(file_list)):
				print(f'       Found file : {file_names[i]} in {file_list[i]}')

			commit_message = 'upload files'
			master_ref     = repo.get_git_ref(f'heads/{AskedBranch}')
			master_sha     = master_ref.object.sha
			base_tree      = repo.get_git_tree(master_sha)

			element_list = list()

			for entry in file_list:
				with open(entry, 'rb') as input_file:
					data = input_file.read()
				if entry.endswith('.png'):
					old_file = repo.get_contents(entry)
					commit = repo.update_file('/' + entry, 'Update PNG content', data, old_file.sha)
				element = InputGitTreeElement(entry, '100644', 'blob', data)
				element_list.append(element)
			
			tree = repo.create_git_tree(element_list, base_tree)
			parent = repo.get_git_commit(master_sha)
			commit = repo.create_git_commit(commit_message, tree, [parent])
			master_ref.edit(commit.sha)

	return 0

username = input('GitHub username : ')
password = getpass('GitHub password : ')

main(sys.argv[1],username,password)