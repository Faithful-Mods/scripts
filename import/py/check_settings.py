import sys
import os
import json

class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

MCVersion   = sys.argv[1]
PackFormat  = 0

# need to have an array for all mc versions
MCVersionArray = [
  ('1.16.3',6), ('1.16.2',6),
  ('1.16.1',5), ('1.15.2',5), ('1.15', 5),
  ('1.14.4',4), ('1.13.2',4), ('1.13', 4),
  ('1.12.2',3), ('1.11.2',3), 
  ('1.10.2',2), ('1.10'  ,2), ('1.9.4',2), ('1.9', 2),
  ('1.8.9', 1), ('1.7.10',1), ('1.6.1',1)
]

def createmcmeta(PackFormat):
	data = {"pack":{"pack_format": PackFormat,"description": "Faithful Mods"}}
	with open('resources/pack.mcmeta', 'a', encoding="utf8") as f:
		json.dump(data, f)

def findpackpng():
	result = False
	for file in os.listdir('resources/'):
		if file == 'pack.png':
			result = True
	return result

#########

def main():
	PackFormat = 0

	for x,y in MCVersionArray: 
		if x == MCVersion:
			PackFormat = y

	if PackFormat == 0:
		print(bcolors.FAIL +'The MC version you specified is invalid or not supported' + bcolors.ENDC)
		return 0

	try:
		os.remove('resources/pack.mcmeta')
	except:
		pass

	createmcmeta(PackFormat)
	PackPNG = findpackpng()
	print('Selected MC version      : ' + bcolors.OKBLUE + f'{MCVersion}' + bcolors.ENDC)
	print('Resource Pack format     : ' + bcolors.OKBLUE + f'{PackFormat}' + bcolors.ENDC)
	print('Resource Pack Icon found : ' + bcolors.OKBLUE + f'{PackPNG}' + bcolors.ENDC)

	if PackPNG == False:
		print(bcolors.FAIL +'Error when locating the pack.png image, please paste it into the resources/ folder' + bcolors.ENDC)
		return 0

	return 0

main()
