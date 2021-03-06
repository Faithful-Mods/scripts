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

# need to have an array for all mc versions
MCVersionArray = [
  ('1.16.3',6), ('1.16.2',6),

  ('1.16.1',5), ('1.16'  ,5), ('1.15.2',5), ('1.15.1',5), ('1.15',  5),

  ('1.14.4',4), ('1.14.3',4), ('1.14.2',4), ('1.14.1',4), ('1.14',  4), ('1.13.2',4), ('1.13.1',4), ('1.13', 4),

  ('1.12.2',3), ('1.12.1',3), ('1.12'  ,3), ('1.11.2',3), ('1.11.1',3), ('1.11',  3), 

  ('1.10.2',2), ('1.10.1',2), ('1.10'  ,2), ('1.9.4', 2), ('1.9.3', 2), ('1.9.2', 2), ('1.9.1', 2), ('1.9',   2),

  ('1.8.9', 1), ('1.8.8', 1), ('1.8.7', 1), ('1.8.6', 1), ('1.8.5', 1), ('1.8.4', 1), ('1.8.3', 1), ('1.8.2', 1), 
  ('1.8.1', 1), ('1.8',   1), ('1.7.10',1), ('1.7.9', 1), ('1.7.8', 1), ('1.7.7', 1), ('1.7.6', 1), ('1.7.5', 1), 
  ('1.7.4', 1), ('1.7.3', 1), ('1.7.2' ,1), ('1.7.1' ,1), ('1.7'   ,1), ('1.6.4', 1), ('1.6.3', 1), ('1.6.2', 1), ('1.6.1', 1)
]

def createmcmeta(PackFormat):
	data = {"pack":{"pack_format": PackFormat,"description": "Faithful Mods"}}
	with open('resources/pack.mcmeta', 'a', encoding="utf8") as f:
		json.dump(data, f, indent=1)

def findpackpng():
	result = False
	for file in os.listdir('resources/'):
		if file == 'pack.png':
			result = True
	return result

def askversionagain(MCVersion):
	if MCVersion == 'undefined':
		MCVersion = input(bcolors.FAIL + 'Enter a valid Minecraft version please : ' + bcolors.ENDC)
	for x,y in MCVersionArray: 
		if x == MCVersion:
			PackFormat = y
			break
		else:
			PackFormat = 0
	if PackFormat == 0:
		print(bcolors.FAIL +'The MC version you specified is invalid or not supported' + bcolors.ENDC)
		PackFormat, MCVersion = askversionagain('undefined')
	return PackFormat, MCVersion

#########

def main():
	PackFormat = 0
	MCVersion = 0

	PackFormat, MCVersion = askversionagain(sys.argv[1])

	try:
		os.remove('resources/pack.mcmeta')
	except:
		pass

	createmcmeta(PackFormat)
	PackPNG = findpackpng()
	print('Selected MC version      : ' + bcolors.OKBLUE + MCVersion  + bcolors.ENDC)
	print('Resource Pack format     : ' + bcolors.OKBLUE + str(PackFormat) + bcolors.ENDC)
	print('Resource Pack Icon found : ' + bcolors.OKBLUE + str(PackPNG)    + bcolors.ENDC)

	return 0

main()
