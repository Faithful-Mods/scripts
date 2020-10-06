import os
import sys
from github import Github
from github import BadCredentialsException

def main(AskedBranch,GHusername,GHpassword):
	onlyfiles = next(os.walk('resources/'))[1]
	NBFiles   = len(onlyfiles) # and not onlyfans

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
			ExistBranch = False
			ExistRepo   = False

			for repo in repos:
				# if repository exist:
				if FileName == repo.name:
					ExistRepo = True
					print('[v] -> Repository found, checking branches...')

					try:
						repo.get_branch(branch=AskedBranch)
					except:
						print('[x] -> Branch not found, creating one...')
						
					else: 
						print('[v] -> Branch found, merging files...')

			# if repository doesn't exist yet:
			if ExistRepo == False:
				print('[x] -> Repository not found, creating one...')

				# Information used in mods.json (mods list) & GitHub repos:
				ModName   = input('      - Mod Name       : ')
				ModURL    = input('      - CurseForge URL : ')
				ModNameCF = ModURL.replace('https://www.curseforge.com/minecraft/mc-mods/','')

				# Create a new repository:
				organization = g.get_organization("Faithful-Mods")
				organization.create_repo(
					FileName, 
					description=f"Official {ModName} Faithful Resource Pack", 
					homepage=ModURL, 
					private=True, 
					has_issues=False, 
					has_wiki=False, 
					has_downloads=False, 
					has_projects=False, 
					delete_branch_on_merge=False
				)

		'''
		#check if repo already exist:
		if file == #repo name :

			#loop in all branches to check if branch already exist:
			for branches in #branches list:
				if branch == branches:
					BranchExist = True
					#merge file into this branch
			
			if BranchExist == False: # !!! not in the loop to avoid creating branches each time the branch isn't found
				#create new branch
				#set branch as a tag (ex: 1-12-2) !!! replace . with -
				if branch #is higher than others:
					#set branch as the new master

		# the repo doesn't exist yet:
		else:
			#create repo
			#create branch
			#import files
			#set repo website link to curse forge mod page
			#set tag to repo (ex:botania,1-12-2) (assetfile name & branch name as tags)
	'''
	return 0

main(sys.argv[1],sys.argv[2],sys.argv[3])