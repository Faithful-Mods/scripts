import os

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

os.system('chcp 65001')
os.system('cls')

print('------------------------------------------------------------\n')
print(' [' + bcolors.HEADER + '1' + bcolors.ENDC + '/?] Applying settings...\n')
print('------------------------------------------------------------')
print(bcolors.WARNING + 'WARNING :' + bcolors.ENDC + ' PyGithub is required to use this sccript : pip install PyGithub')
print(bcolors.WARNING + 'WARNING :' + bcolors.ENDC + ' GitPython is required to use this sccript  : pip install GitPython')
print(bcolors.WARNING + 'WARNING :' + bcolors.ENDC + ' getpass is required to use this sccript  : pip install getpass\n')

MCVERSION = input('Minecraft version : ')
CHOICE    = input('Have you placed mods resource pack under the /resources folder [Y/N]? ')

if CHOICE == 'y' or CHOICE == 'yes' or CHOICE == 'Y' or CHOICE == 'YES':
	print('\n------------------------------------------------------------\n')
	print(' [' + bcolors.HEADER + '2' + bcolors.ENDC + '/?] Load settings...\n')
	print('------------------------------------------------------------')
	os.system(f'python py\\check_settings.py "{MCVERSION}"')
	print('\n------------------------------------------------------------\n')
	print(' [' + bcolors.HEADER + '3' + bcolors.ENDC + '/?] Import Files to GitHub...\n')
	print('------------------------------------------------------------')
	os.system(f'python py\\github_import.py "{MCVERSION}"')

	'''
	# to avoid : delete repo from google when it crashed, will be removed
	if input('Should delete repo? [y/n] ') == 'y':
		os.system('python py\\delete_repo.py "cosmeticarmorreworked"')
	'''
	
elif CHOICE == 'n' or CHOICE == 'no' or CHOICE == 'N' or CHOICE == 'NO':
	print('You need to place all your mods resource in the /resources folder following this : "/resources/<asset_name>/..."\nex: "/resources/minecraft/..." or ex: "/resources/botania/..."')

else:
	print('Invalid value')