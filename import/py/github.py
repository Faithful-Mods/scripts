import os
import sys

def main(branch):
	onlyfiles = next(os.walk('resources/'))[1]
	NBFiles   = len(onlyfiles) # and not onlyfans

	# check if files have been placed in the /resources folder
	if NBFiles == 0:
		print('You need to place all your mods resource in the /resources folder following this : "/resources/<asset_name>/..."')
		print('Ex: /resources/botania/...')
		return 0

	for file in os.listdir('resources/'):
		BranchExist = False

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

	return 0

main(sys.argv[1])