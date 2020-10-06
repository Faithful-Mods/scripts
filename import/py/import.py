# Import mods resource pack from f32 to github
# v1.0

import sys
import os
import json

MCVersion   = sys.argv[1]
PackFormat  = 0
ModsPath    = sys.argv[2]

# need to have an array for all mc versions
MCVersionArray = [
	("1.6.1", 1), ("1.8.9", 1),
	("1.9",   2), ("1.10.2",2),
	("1.11.2",3), ("1.12.2",3),
	("1.13",  4), ("1.14.4",4),
	("1.15",  5), ("1.16.1",5),
	("1.16.2",6)
]

def createmcmeta(PackFormat):
	data = {"pack":{"pack_format": PackFormat,"description": "Faithful Mods"}}
	with open('resources/pack.mcmeta', 'a') as f:
		json.dump(data, f)

def findpackpng():
	result = False
	for file in os.listdir('resources/'):
		if file == 'pack.png':
			result = True
	return result

#########
def main():
	for x,y in MCVersionArray: 
		if x == MCVersion:
			PackFormat = y

	if PackFormat == 0:
		print('The MC version you specified is invalid or not supported')
		return 0

	createmcmeta(PackFormat)
	PackPNG = findpackpng()
	print('Selected MC version      :',MCVersion)
	print('Resource Pack format     :',PackFormat)
	print('Resource Pack Icon found :',PackPNG)

	if PackPNG == False:
		print('Error when locating the pack.png image, please paste it into the resources/ folder')
		return 0

	print('\nStart Import with GitHub API\n')

	onlyfiles = next(os.walk('resources/'))[1]
	NBFiles   = len(onlyfiles) # and not onlyfans

	if NBFiles == 0:
		print('You need to place all your mods resource in the /resources folder following this : "/resources/<asset_name>/..."')
		print('Ex: /resources/botania/...')
		return 0

	print('yes')

	return 0

main()
