import sys, subprocess, os, urllib, zipfile, time, json, PyQt5, requests
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from urllib import request
from io import BytesIO
from urllib.request import urlopen

					


url = "https://bsite.net/tuanvu02/data.json"
response = urlopen(url)
main_data = json.loads(response.read())


class LoginPage(QDialog):
	def __init__(self):

		# current_version
		__version = 1.1
		super(LoginPage, self).__init__()

		
		# check version
		url = 'https://bsite.net/tuanvu02/version.txt'
		file = urllib.request.urlopen(url)
		version = float(file.read())
		if (version > __version):
			print("Update!")
			reply = QMessageBox.question(self,'Update', 'Hiện đã có phiên bản mới\nTải về để tiếp tục!',
			QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

			if reply == QMessageBox.Yes:
				app = QApplication(sys.argv)
				app.exit()
				os.startfile("update.exe")
			else:
				app = QApplication(sys.argv)
				app.exit()
		else:
			print("Continue!")

			# Load loginpage 
			loadUi("loginpage.ui", self)
			widget.width = 580
			widget.height = 262
			widget.setWindowTitle('Đăng nhập')
			self.loginButton.clicked.connect(self.select_subject)
			self.label_3.setStyleSheet("font-size: 13px; ")
			self.label_4.setStyleSheet("font-size: 13px; ")
			self.label_5.setStyleSheet("font-size: 13px; ")
			self.loginButton.setStyleSheet("font-size: 13px;")

			self.namefield.setStyleSheet("border-radius: 3px; border: 1px solid #000; font-size:12px;")
			self.idfield.setStyleSheet("border-radius: 3px; border: 1px solid #000; font-size:12px;")
			self.classfield.setStyleSheet("border-radius: 3px; border: 1px solid #000; font-size:12px;")
			self.errorLogin.setStyleSheet("font-size:12px; color:red;")



			


	def select_subject(self):
		global name, msv, lop, sjSelection, main_data, sj_id_list, res, user_id
		name = self.namefield.text()
		msv = self.idfield.text()  #0912102165
		lop = self.classfield.text()

		url = f"http://test.iptech.edu.vn/finetest4/api-user-login.php?masv={msv}&hoten={name}&lop={lop}&maytinh=%23"
		res = requests.get(url)
		content = res.json()

		if(content['status'] == 1):
			if(len(content['subjects']) == 0):
				self.errorLogin.setText("* Không có bài làm nào có thể truy cập")
			else:
				user_id = content['id']
				sj_id_list = [ i['subject_id'] for i in content['subjects']]
				sj_list = [ i['subject_name'] for i in content['subjects']]

				sjSelection = QDialog(self)
				sjSelection.setWindowTitle("Bạn chọn làm bài nào trong danh sách dưới đây")
				sjSelection.setFixedHeight(80 * int(len(sj_list)))
				sjSelection.setFixedWidth(500)
				connect_box = QVBoxLayout(sjSelection)
				connect_box.setAlignment(Qt.AlignCenter)  
				self.errorLogin.setText("")
				for i in sj_list:
					sj = QPushButton(i)
					sj.setFixedSize(350, 39)
					sj.setStyleSheet("color:black; background-color:#7ab0cc; border-radius: 6px;")
					sj.clicked.connect(self.goToMainPage)
					connect_box.addWidget(sj, alignment=Qt.AlignCenter)
				sjSelection.exec()

		elif (content['status'] == 2 or content['status'] == 3):
			self.errorLogin.setText("* Vui lòng liên hệ giáo viên để có thể đăng nhập")
		elif (content['status'] == 4):
			self.errorLogin.setText("* Vui lòng kiểm tra lại thông tin đăng nhập")
			
			print("Wrong!")

	def goToMainPage(self):
		global name, msv, lop, sjSelection, main_data, sj_id_list, res, main_sj_id, sj_code
		subject = self.sender().text()
		print(subject)
		for i in res.json()['subjects']:
			if(i['subject_name'] == subject):
				main_sj_id = i['subject_id']
				sj_langs = i['subject_langs']
				sj_code = i['subject_code']
				break
		print(main_sj_id)
		print(sj_langs)
		main = mainPage(name, msv, lop, subject, main_sj_id, sj_langs)
		widget.addWidget(main)
		widget.setCurrentIndex(widget.currentIndex()+1)
		widget.setFixedHeight(596)
		widget.setFixedWidth(801)
		sjSelection.reject()
		
		


class mainPage(QDialog):
	def __init__(self, name, msv, lop, subject, main_sj_id, sj_langs):
		global _msv, _main_sj_id, user_id, _sj_langs, score, totalScore, content, sj_code
		_msv = msv
		_main_sj_id = main_sj_id
		_sj_langs = sj_langs
		_sj_code = sj_code
		print(_sj_code)
		widget.setWindowTitle('FineTest')
		super(mainPage, self).__init__()
		loadUi("mainpage.ui", self)
		self.progressBar.setVisible(False)
		self.nameDisplay.setText(f'Họ và tên : {name}')
		self.idDisplay.setText(f'Mã sinh viên : {msv}')
		self.classDisplay.setText(f'Lớp : {lop}')
		self.sjDisplay.setText(f'Môn học : {subject}')

		self.setFixedHeight(596)
		self.setFixedWidth(801)

		css_display = "font-size: 13px; color: white;background-color: rgb(84, 136, 237)"
		self.nameDisplay.setStyleSheet(css_display)
		self.idDisplay.setStyleSheet(css_display)
		self.classDisplay.setStyleSheet(css_display)
		self.sjDisplay.setStyleSheet(css_display)
		self.label_6.setStyleSheet(css_display)
		self.markDisplay.setStyleSheet(css_display)
		
		self.viewButton.setStyleSheet("QPushButton{border-radius: 8px;background-color: #e9e3df; color:black; font-size: 13px;}QPushButton:hover{color: white;background-color: rgb(85, 170, 127);}QPushButton:focus{outline:none;}")
		self.submitButton.setStyleSheet("QPushButton{border-radius: 8px;background-color: #e9e3df; color:black; font-size: 13px;}QPushButton:hover{color: white;background-color: rgb(85, 170, 127);}QPushButton:focus{outline:none;}")
		self.exitButton.setStyleSheet("QPushButton{border-radius: 8px;background-color: #e9e3df; color:black; font-size: 13px;}QPushButton:hover{color: white;background-color: #d43d41;}QPushButton:focus{outline:none;}")

		self.titleList.setStyleSheet("color: black; font-size: 12px; border: 0px solid #ccc;")
	
		url_problem = f"http://test.iptech.edu.vn/finetest4/api-user-subject-set.php?userid={user_id}&subjectid={_main_sj_id}&fbclid=IwAR30jurteX107CLh6wNF9W9_Fv6Il_NbZeBKaG2qNqAqitp5P5QoxjHMaDw"
		res_problem = requests.get(url_problem)
		content = res_problem.json()
		score = 0

		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		widget.move(qr.topLeft())


		

		
		total_pr = len(content)

		totalScore = total_pr * 100
		self.viewButton.clicked.connect(self.open)
		self.exitButton.clicked.connect(self.exit)
		self.submitButton.clicked.connect(self.submit)



		self.tableWidget = self.titleList

		#Row count
		self.tableWidget.setRowCount(total_pr + 1) 

		#Column count
		self.tableWidget.setColumnCount(6)
		self.tableWidget.verticalHeader().setVisible(False)

		
		exercise_id_list = [i['problem_id'] for i in content]
		i = 1
		for item in content:
			exercise_id = item['problem_nickname']
			self.tableWidget.setItem(i,0, QTableWidgetItem(exercise_id))
			self.tableWidget.setItem(i,1, QTableWidgetItem(item["problem_fullname"]))
			self.tableWidget.setItem(i,2, QTableWidgetItem(item["problem_topic"]))
			pr_maxtime = int(item['problem_maxtime'])/1000
			self.tableWidget.setItem(i,3, QTableWidgetItem(str(pr_maxtime) + " giây"))
			self.tableWidget.item(i,3).setTextAlignment(Qt.AlignCenter)
			
			submit_times = item["tryhard"]
			if submit_times == None: submit_times = '0'
			temp_score = item["score"]
			if temp_score == None: temp_score = '0'
			self.tableWidget.setItem(i,5, QTableWidgetItem(str(submit_times)))
			self.tableWidget.item(i,5).setTextAlignment(Qt.AlignCenter)
			self.tableWidget.setItem(i,4, QTableWidgetItem(str(temp_score)))
			self.tableWidget.item(i,4).setTextAlignment(Qt.AlignCenter)
			if (temp_score == '100'):
				score += 100
				for k in range(6):
					self.tableWidget.item(i,k).setForeground(QtGui.QColor(225, 61, 65))
			i+=1
		self.markDisplay.setText(f'Điểm tổng : {score} / {totalScore}')

			

		self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
		self.tableWidget.setFocusPolicy(Qt.NoFocus)
		self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.tableWidget.setShowGrid(False)


		

		#Table will fit the screen horizontally
		self.tableWidget.setHorizontalHeaderLabels(['MÃ BÀI','BÀI TẬP', 'CHỦ ĐỀ', 'GIỚI HẠN', 'ĐIỂM', 'NỘP'])
		self.tableWidget.setColumnWidth(0,60)
		self.tableWidget.setColumnWidth(1,250)
		self.tableWidget.setColumnWidth(2,200)
		self.tableWidget.setColumnWidth(3,80)
		self.tableWidget.setColumnWidth(4,60)
		self.tableWidget.setColumnWidth(5,50)
		self.tableWidget.horizontalHeader().setStyleSheet("QHeaderView { font: bold; font-size: 12px;}")

		
		self.scroll = self.statusScroll             # Scroll Area which contains the widgets, set as the centralWidget
		self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
		self.vbox = QVBoxLayout()               # The Vertical Box that contains the Horizontal Boxes of  labels and buttons

		

	
	def submit(self):
		try:
			global score, totalScore, main_data, msv, _main_sj_id, _sj_langs, content, sj_code
			tempScore = 0
			crRow = self.tableWidget.currentRow()
			pr_nickname = self.tableWidget.item(crRow,0).text()
			problem_index = None
			for i in range(len(content)):
				if(content[i]['problem_nickname'] == pr_nickname):
					problem_index = i
					break
			zipFileUrl = f'http://test.iptech.edu.vn/finetest4/problem/{sj_code[0:4]}2021/{pr_nickname}.zip'
			req = requests.get(zipFileUrl)
			zipFileName = f'{pr_nickname}.zip'
			with open(zipFileName,'wb') as output_file:
			    output_file.write(req.content)

			with zipfile.ZipFile(zipFileName, 'r') as zip_ref:
			    zip_ref.extractall('TestCase')

			subprocess.run(f"rm {zipFileName}",shell=True)

			testcase_amount = len(os.listdir(f"TestCase/{pr_nickname}"))
			if(_sj_langs != None):
				subject_langs = ""
				for item in _sj_langs.split():
					subject_langs+= "*"+item + " "
					if(item == ".c"):
						subject_langs+="*.cpp "
			else:
				subject_langs = "*.cpp *.py"
			path = QFileDialog.getOpenFileName(self, 'Open a file', '',f'All Files ({subject_langs})')
			if path != ('', ''):
				try:
					newFolder = f"{os.getcwd()}/User/{pr_nickname}"
					os.mkdir(newFolder)
				except:
					print("Folder existed!")
				print(path[0])
				object = QLabel("---BẮT ĐẦU CHẤM BÀI---")
				object.setStyleSheet("color: black; font-size:11px;")
				self.vbox.addWidget(object)
				self.widget.setLayout(self.vbox)
				self.scroll.setWidget(self.widget)
				self.scroll.verticalScrollBar().rangeChanged.connect(self.ResizeScroll)

				#create a new folder to contain user's output
				newpath = f'./User/{pr_nickname}' 
				if not os.path.exists(newpath):
				    os.makedirs(newpath)
				if path[0][-3:] == '.py':
					drRun = f'python3 {path[0]}'
				else:
					drRun = './a.out'
				self.progressBar.setVisible(True)
				prbar_val = 100/testcase_amount
				for i in range(1,testcase_amount+1):
					
					if i == 1 and path[0][-3:] == 'cpp':
						subprocess.run(f'g++ {path[0]}', shell=True)

					process = subprocess.Popen(f"{drRun} <./Submit/{pr_nickname}/{i}.inp> ./User/{pr_nickname}/output{i}.out", shell=True)

					try:
						start_time = time.time()
						print('Running in process', process.pid)
						process.wait(timeout=1)
						file1 = open(f"./Submit/{pr_nickname}/{i}.out",'r')
						var1 = file1.read()
						file1.close()

						file1 = open(f'./User/{pr_nickname}/output{i}.out', 'r')
						var2 = file1.read()
						file1.close()

						exe_time = round((time.time() - start_time), 3)
						# Compare
						if var2 == var1:
							tempScore+=20
							object = QLabel(f'[{pr_nickname}] Test {i}: Hoàn toàn chính xác - thời gian chạy {exe_time}s')
							object.setStyleSheet("color: green; font-size:11px;")
							self.vbox.addWidget(object)
							self.widget.setLayout(self.vbox)
							self.scroll.setWidget(self.widget)
							self.scroll.verticalScrollBar().rangeChanged.connect(self.ResizeScroll)
							QApplication.processEvents()
							
						else:
							tempVar1 = var1.split()
							tempVar2 = var2.split()

							if ''.join(tempVar2) == ''.join(tempVar1):
								tempScore+=15
								object = QLabel(f'[{pr_nickname}] Test {i}: Đúng nhưng sai sót về trình bày')
								object.setStyleSheet("color: black; font-size:11px;")
								self.vbox.addWidget(object)
								self.widget.setLayout(self.vbox)
								self.scroll.setWidget(self.widget)
								self.scroll.verticalScrollBar().rangeChanged.connect(self.ResizeScroll)

								#prevent freeze
								QApplication.processEvents()
								
							else:
								object = QLabel(f'[{pr_nickname}] Test {i}: Kết quả sai, hãy kiểm tra lại bài làm - thời gian chạy {exe_time}s')
								object.setStyleSheet("color: #ef3d41; font-size:11px;")
								self.vbox.addWidget(object)
								self.widget.setLayout(self.vbox)
								self.scroll.setWidget(self.widget)
								self.scroll.verticalScrollBar().rangeChanged.connect(self.ResizeScroll)
								QApplication.processEvents()
								
					except subprocess.TimeoutExpired:
						exe_time = round((time.time() - start_time), 3)
						print('Timed out - killing', process.pid)
						os.system("TASKKILL /F /IM a.exe /T")
						process.kill()
						object = QLabel(f'[{pr_nickname}] Test {i}: Chương trình chạy quá thời gian - thời gian chạy {exe_time}s')
						object.setStyleSheet("color: red; font-size:11px;")
						self.vbox.addWidget(object)
						self.widget.setLayout(self.vbox)
						self.scroll.setWidget(self.widget)
						self.scroll.verticalScrollBar().rangeChanged.connect(self.ResizeScroll)
						QApplication.processEvents()
						
						
					self.progressBar.setValue(int(i*prbar_val))
					print("--- %s seconds ---" % (time.time() - start_time))
					print(f"Test {i} oke!")
				self.progressBar.setVisible(False)
				object = QLabel(f'=== KẾT THÚC: ĐIỂM {tempScore}% ===')
				object.setStyleSheet("color: black; font-size:11px;")
				self.vbox.addWidget(object)
				self.widget.setLayout(self.vbox)
				self.scroll.setWidget(self.widget)
				self.scroll.verticalScrollBar().rangeChanged.connect(self.ResizeScroll)

				userScore = float(content[problem_index]['score'])
				if(tempScore > userScore):
					self.tableWidget.setItem(crRow,4, QTableWidgetItem(f'{float(tempScore)}'))
					self.tableWidget.item(crRow,4).setTextAlignment(Qt.AlignCenter)
					#.....update score to database.....

				# 	# Update submit_times
					submit_times = int(content[problem_index]['tryhard'])
					self.tableWidget.setItem(crRow,5, QTableWidgetItem(f'{submit_times + 1}'))
					self.tableWidget.item(crRow,5).setTextAlignment(Qt.AlignCenter)
					#.....update tryhard to database.....

					if(tempScore == 100):
						for i in range(6):
							self.tableWidget.item(crRow,i).setForeground(QtGui.QColor(250, 3, 0))
					score+=tempScore
					self.markDisplay.setText(f'Điểm tổng : {score} / {totalScore}')
				else:
					object = QLabel("--GIỮ NGUYÊN ĐIỂM--")
					self.vbox.addWidget(object)
					self.widget.setLayout(self.vbox)
					self.scroll.setWidget(self.widget)
					self.scroll.verticalScrollBar().rangeChanged.connect(self.ResizeScroll)
				subprocess.run(f"rm a.out",shell=True)
			else:
				print("No choose file!")
		except Exception as e:
			print(e)
			print("Do not select!")
	def ResizeScroll(self, min, maxi): #auto scroll
		self.scroll.verticalScrollBar().setValue(maxi)

	def open(self):
		global sj_code
		try:
			crRow = self.tableWidget.currentRow()
			pr_nickname = self.tableWidget.item(crRow,0).text()
			simp_path_Problems = 'Problems'
			abs_path_Data = os.path.abspath(simp_path_Problems)
			file = f'Problems/{pr_nickname}.pdf'
			try:
				# raise error
				temp = open(file)
				subprocess.Popen(["open", file])
				self.viewButton.setFocusPolicy(Qt.NoFocus)
			except:
				print("try")
				url = f"http://test.iptech.edu.vn/finetest4/problem/{sj_code[0:4]}2021/{pr_nickname}.pdf"
				response = requests.get(url)
				with open(f'Problems/{pr_nickname}.pdf', 'wb') as f:
					f.write(response.content)
				subprocess.Popen(["open", file])
				self.viewButton.setFocusPolicy(Qt.NoFocus)
		except Exception as e:
			print("Do not select!")
	def exit(self):
		app.exit()





#main

app = QApplication(sys.argv)

widget = QStackedWidget()
welcome = LoginPage()
widget.addWidget(welcome)
widget.show()
try:
	sys.exit(app.exec_())
except:
	print("Exiting")	

