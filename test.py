# # import requests
# # print('Downloading started')
# # url = 'http://test.iptech.edu.vn/finetest4/problem/prog2021/HELLOVN.zip'

# req = requests.get(url)
# filename = url.split('/')[-1]
# with open(filename,'wb') as output_file:
#     output_file.write(req.content)

# import zipfile
# with zipfile.ZipFile('HELLOVN.zip', 'r') as zip_ref:
#     zip_ref.extractall('Check')


# import os

# listFile = os.listdir("Te") # dir is your directory path
# number_files = len(list)
# print number_files


string = "programing"


print(string[0:4])