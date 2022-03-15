import requests, zipfile, os, subprocess
from io import BytesIO
from tqdm import tqdm

try:
	subprocess.run(f"del /f FineTest.exe",shell=True)
except:
	pass
print("Wait a minute!")
print('Downloading.....')

#Defining the zip file URL
url = 'https://bsite.net/tuanvu02/update.zip'
req = requests.get(url, stream=True)

# extracting the zip file contents
file= zipfile.ZipFile(BytesIO(req.content))

for data in tqdm(iterable=file.namelist(), total=len(file.namelist()), desc="Updating", bar_format="{l_bar}{bar}|"):
	file.extract(member=data)
file.close()
print("-----------------")
print('Updated!')