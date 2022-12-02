import os, pathlib, platform, subprocess, time, zipfile, requests, sys
import tkinter as tk
from tkinter import messagebox
from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMessageBox, QVBoxLayout, QPushButton, \
    QTableWidgetItem, QAbstractItemView, QWidget, QFileDialog, QLabel


class Problem():
    def __init__(self, code, nickName, fullName, content, testCase, timeLimit, topic, score, tryHard):
        self.code = code
        self.nickName = nickName
        self.fullName = fullName
        self.content = content
        self.testCase = testCase
        self.timeLimit = timeLimit
        self.topic = topic
        self.score = score
        self.tryHard = tryHard


class Subject():
    def __init__(self, subjectId, subjectCode, subjectName, subjectLangs):
        self.id = subjectId
        self.code = subjectCode
        self.name = subjectName
        self.langs = subjectLangs


class LoginPage(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Đăng nhập")
        Dialog.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        Dialog.resize(568, 262)
        Dialog.setMinimumSize(QtCore.QSize(568, 262))
        Dialog.setMaximumSize(QtCore.QSize(568, 262))
        Dialog.setSizeIncrement(QtCore.QSize(580, 281))
        Dialog.setBaseSize(QtCore.QSize(580, 281))
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(30, 10, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(30, 60, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.loginButton = QtWidgets.QPushButton(Dialog)
        self.loginButton.setEnabled(True)
        self.loginButton.setGeometry(QtCore.QRect(420, 190, 111, 38))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.loginButton.setFont(font)
        self.loginButton.setMouseTracking(False)
        self.loginButton.setStyleSheet("\n""QPushButton{\n""    border-radius: 2px;\n""    background-color: #ffffff;\n"
                                       "color: #000;\n""    border: 1px solid #000;\n""}\n""\n""QPushButton:hover{\n"
                                       "background-color: #fffbfa;\n}\n"
                                       "QPushButton:focus {\n"
                                       "outline: none;\n}\n")
        self.loginButton.setObjectName("loginButton")
        self.loginButton.clicked.connect(self.select_subject)
        self.classfield = QtWidgets.QLineEdit(Dialog)
        self.classfield.setGeometry(QtCore.QRect(150, 120, 391, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.classfield.setFont(font)
        self.classfield.setAcceptDrops(False)
        self.classfield.setStyleSheet("border-radius: 3px;\n"
                                      "border: 1px solid #000;")
        self.classfield.setText("")
        self.classfield.setFrame(True)
        self.classfield.setObjectName("classfield")
        self.errorLogin = QtWidgets.QLabel(Dialog)
        self.errorLogin.setGeometry(QtCore.QRect(20, 220, 301, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.errorLogin.setFont(font)
        self.errorLogin.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.errorLogin.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.DefaultContextMenu)
        self.errorLogin.setAcceptDrops(True)
        self.errorLogin.setStyleSheet("color: red;")
        self.errorLogin.setText("")
        self.errorLogin.setObjectName("errorLogin")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(30, 120, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.idfield = QtWidgets.QLineEdit(Dialog)
        self.idfield.setGeometry(QtCore.QRect(150, 70, 391, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.idfield.setFont(font)
        self.idfield.setAcceptDrops(False)
        self.idfield.setStyleSheet("border-radius: 3px;\n"
                                   "border: 1px solid #000;")
        self.idfield.setText("")
        self.idfield.setFrame(True)
        self.idfield.setCursorPosition(0)
        self.idfield.setObjectName("idfield")
        self.namefield = QtWidgets.QLineEdit(Dialog)
        self.namefield.setGeometry(QtCore.QRect(150, 20, 391, 21))
        self.namefield.setMinimumSize(QtCore.QSize(0, 12))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.namefield.setFont(font)
        self.namefield.setMouseTracking(True)
        self.namefield.setAcceptDrops(False)
        self.namefield.setStyleSheet("border-radius: 3px;\n"
                                     "border: 1px solid #000;")
        self.namefield.setText("")
        self.namefield.setFrame(True)
        self.namefield.setReadOnly(False)
        self.namefield.setPlaceholderText("")
        self.namefield.setCursorMoveStyle(QtCore.Qt.CursorMoveStyle.LogicalMoveStyle)
        self.namefield.setObjectName("namefield")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.namefield, self.idfield)
        Dialog.setTabOrder(self.idfield, self.classfield)
        Dialog.setTabOrder(self.classfield, self.loginButton)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Đăng nhập"))
        self.label_3.setText(_translate("Dialog", "Họ và tên"))
        self.label_4.setText(_translate("Dialog", "Mã sinh viên"))
        self.loginButton.setText(_translate("Dialog", "Đăng nhập"))
        self.label_5.setText(_translate("Dialog", "Lớp"))

    def select_subject(self):
        global name, msv, lop, sjSelection, sj_id_list, res, user_id, subjectList
        name = self.namefield.text()
        msv = self.idfield.text()
        lop = self.classfield.text()
        computer_name = platform.node()
        subjectList = []

        url = f"http://test.iptech.edu.vn/finetest4/api-user-login.php?masv={msv}&hoten={name}&lop={lop}&maytinh={computer_name}"
        url = f"http://test.iptech.edu.vn/finetest4/api-user-login.php?masv={msv}&hoten={name}&lop={lop}&maytinh=%23"
        try:
            res = requests.get(url)
        except:
            QMessageBox.about(self, "Thông báo", "Không có kết nối Internet!")
        content = res.json()

        if (content['status'] == 1):
            if (len(content['subjects']) == 0):
                self.errorLogin.setText("* Không có bài làm nào có thể truy cập")
            else:
                user_id = content['id']
                for sj in content['subjects']:
                    subject = Subject(sj['subject_id'], sj['subject_code'], sj['subject_name'], sj['subject_langs'])
                    subjectList.append(subject)
                sj_id_list = [i['subject_id'] for i in content['subjects']]

                sjSelection = QtWidgets.QDialog()
                sjSelection.setWindowTitle("Bạn chọn làm bài nào trong danh sách dưới đây")
                sjSelection.setFixedHeight(80 * int(len(subjectList)))
                sjSelection.setFixedWidth(500)
                connect_box = QVBoxLayout(sjSelection)
                connect_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.errorLogin.setText("")
                for i in range(len(subjectList)):
                    sj = QPushButton(subjectList[i].name)
                    sj.setFixedSize(350, 39)
                    sj.setStyleSheet("color:black; background-color:#7ab0cc; border-radius: 6px;")
                    sj.clicked.connect(lambda _, j=i: self.goToMainPage(subjectId=j, subject=subjectList[i].name))
                    connect_box.addWidget(sj, alignment=Qt.AlignmentFlag.AlignCenter)
                sjSelection.exec()

        elif (content['status'] == 2 or content['status'] == 3):
            self.errorLogin.setText("* Vui lòng liên hệ giáo viên để có thể đăng nhập")
        elif (content['status'] == 4):
            self.errorLogin.setText("* Vui lòng kiểm tra lại thông tin đăng nhập")

    def goToMainPage(self, subjectId, subject):
        global name, msv, lop, sjSelection, sj_id_list, res, main_sj_id, sj_code
        main_sj_id = subjectList[subjectId].id
        sj_langs = subjectList[subjectId].langs
        sj_code = subjectList[subjectId].code
        Dialog.close()
        ui = mainPage()
        ui.setupUi(Dialog, name, msv, lop, subject, main_sj_id, sj_langs)
        Dialog.show()
        sjSelection.reject()

class mainPage(object):
    def setupUi(self, Dialog, name, msv, lop, subject, main_sj_id, sj_langs):
        self.rootPath = rootPath
        self.name = name
        global _msv, _main_sj_id, user_id, _sj_langs, score, totalScore, content, sj_code
        _msv = msv
        _main_sj_id = main_sj_id
        _sj_langs = sj_langs
        _sj_code = sj_code
        Dialog.setObjectName("Dialog")
        Dialog.resize(801, 596)
        Dialog.setMinimumSize(QtCore.QSize(801, 596))
        Dialog.setMaximumSize(QtCore.QSize(801, 596))
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(0, 0, 801, 601))
        font = QtGui.QFont()
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.widget.setFont(font)
        self.widget.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.widget.setMouseTracking(False)
        self.widget.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.widget.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.DefaultContextMenu)
        self.widget.setAccessibleName("")
        self.widget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.widget.setObjectName("widget")
        self.submitButton = QtWidgets.QPushButton(self.widget)
        self.submitButton.setGeometry(QtCore.QRect(50, 490, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.submitButton.setFont(font)
        self.submitButton.setStyleSheet("QPushButton{"
                                        "border-radius: 8px;"
                                        "background-color: rgb(207, 218, 255);}"
                                        "QPushButton:hover{color: white;"
                                        "background-color: rgb(85, 170, 127);}"
                                        "QPushButton:focus{"
                                        "outline:none;}")
        self.submitButton.setObjectName("submitButton")
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setGeometry(QtCore.QRect(520, 10, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: white;"
                                   "background-color: rgb(84, 136, 237);")
        self.label_6.setObjectName("label_6")
        self.label_18 = QtWidgets.QLabel(self.widget)
        self.label_18.setGeometry(QtCore.QRect(170, 600, 151, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_18.setFont(font)
        self.label_18.setStyleSheet("background-color: rgb(227, 219, 255);")
        self.label_18.setObjectName("label_18")
        self.exitButton = QtWidgets.QPushButton(self.widget)
        self.exitButton.setGeometry(QtCore.QRect(50, 530, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.exitButton.setFont(font)
        self.exitButton.setStyleSheet("QPushButton{"
                                      "border-radius: 8px;"
                                      "background-color: rgb(207, 218, 255);}"
                                      "QPushButton:hover{"
                                      "color: white;"
                                      "background-color: rgb(255, 3, 62);"
                                      "QPushButton:focus{outline:none}")
        self.exitButton.setObjectName("exitButton")
        self.classDisplay = QtWidgets.QLabel(self.widget)
        self.classDisplay.setGeometry(QtCore.QRect(50, 70, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.classDisplay.setFont(font)
        self.classDisplay.setStyleSheet("color: white;"
                                        "background-color: rgb(84, 136, 237);")
        self.classDisplay.setObjectName("classDisplay")
        self.label_11 = QtWidgets.QLabel(self.widget)
        self.label_11.setGeometry(QtCore.QRect(810, 540, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet("background-color: rgb(227, 219, 255);")
        self.label_11.setObjectName("label_11")
        self.markDisplay = QtWidgets.QLabel(self.widget)
        self.markDisplay.setGeometry(QtCore.QRect(520, 70, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.markDisplay.setFont(font)
        self.markDisplay.setStyleSheet("color: white;"
                                       "background-color: rgb(84, 136, 237);")
        self.markDisplay.setObjectName("markDisplay")
        self.viewButton = QtWidgets.QPushButton(self.widget)
        self.viewButton.setGeometry(QtCore.QRect(50, 450, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.viewButton.setFont(font)
        self.viewButton.setStyleSheet("QPushButton{"
                                      "  border-radius: 8px;"
                                      "  background-color: rgb(207, 218, 255);}"
                                      "QPushButton:hover{"
                                      "  color: white;\n"
                                      "  background-color: rgb(85, 170, 127);}"
                                      "QPushButton:focus{"
                                      "  outline:none;}")
        self.viewButton.setObjectName("viewButton")
        self.nameDisplay = QtWidgets.QLabel(self.widget)
        self.nameDisplay.setGeometry(QtCore.QRect(50, 10, 361, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.nameDisplay.setFont(font)
        self.nameDisplay.setStyleSheet("color: white;"
                                       "background-color: rgb(84, 136, 237);")
        self.nameDisplay.setObjectName("nameDisplay")
        self.Info_table = QtWidgets.QTableView(self.widget)
        self.Info_table.setGeometry(QtCore.QRect(0, 0, 801, 111))
        self.Info_table.setStyleSheet("background-color: rgb(84, 136, 237);")
        self.Info_table.setObjectName("Info_table")
        self.label_16 = QtWidgets.QLabel(self.widget)
        self.label_16.setGeometry(QtCore.QRect(820, 560, 31, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_16.setFont(font)
        self.label_16.setStyleSheet("background-color: rgb(227, 219, 255);")
        self.label_16.setObjectName("label_16")
        self.sjDisplay = QtWidgets.QLabel(self.widget)
        self.sjDisplay.setGeometry(QtCore.QRect(520, 40, 261, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.sjDisplay.setFont(font)
        self.sjDisplay.setStyleSheet("color: white;"
                                     "background-color: rgb(84, 136, 237);")
        self.sjDisplay.setObjectName("sjDisplay")
        self.label_17 = QtWidgets.QLabel(self.widget)
        self.label_17.setGeometry(QtCore.QRect(820, 590, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_17.setFont(font)
        self.label_17.setStyleSheet("background-color: rgb(227, 219, 255);")
        self.label_17.setObjectName("label_17")
        self.idDisplay = QtWidgets.QLabel(self.widget)
        self.idDisplay.setGeometry(QtCore.QRect(50, 40, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.idDisplay.setFont(font)
        self.idDisplay.setStyleSheet("color: white;"
                                     "background-color: rgb(84, 136, 237);")
        self.idDisplay.setObjectName("idDisplay")
        self.widget_2 = QtWidgets.QWidget(self.widget)
        self.widget_2.setGeometry(QtCore.QRect(30, 120, 741, 271))
        self.widget_2.setStyleSheet("QWidget#widget_2{"
                                    "    border: 1.5px solid black;"
                                    "    border-radius: 8px;"
                                    "}")
        self.widget_2.setObjectName("widget_2")
        self.titleList = QtWidgets.QTableWidget(self.widget_2)
        self.titleList.setGeometry(QtCore.QRect(10, 10, 721, 251))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(False)
        self.titleList.setFont(font)
        self.titleList.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.titleList.setObjectName("titleList")
        self.titleList.setColumnCount(0)
        self.titleList.setRowCount(0)
        self.statusScroll = QtWidgets.QScrollArea(self.widget)
        self.statusScroll.setGeometry(QtCore.QRect(180, 430, 571, 151))
        self.statusScroll.setWidgetResizable(True)
        self.statusScroll.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
        self.statusScroll.setObjectName("statusScroll")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 569, 149))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.statusScroll.setWidget(self.scrollAreaWidgetContents)
        self.progressBar = QtWidgets.QProgressBar(self.widget)
        self.progressBar.setEnabled(True)
        self.progressBar.setGeometry(QtCore.QRect(180, 400, 571, 23))
        self.progressBar.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhNone)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.Info_table.raise_()
        self.submitButton.raise_()
        self.label_6.raise_()
        self.label_18.raise_()
        self.exitButton.raise_()
        self.classDisplay.raise_()
        self.label_11.raise_()
        self.markDisplay.raise_()
        self.viewButton.raise_()
        self.nameDisplay.raise_()
        self.label_16.raise_()
        self.sjDisplay.raise_()
        self.label_17.raise_()
        self.idDisplay.raise_()
        self.widget_2.raise_()
        self.statusScroll.raise_()
        self.progressBar.raise_()

        self.progressBar.setVisible(False)
        self.nameDisplay.setText(f'Họ và tên : {self.name}')
        self.idDisplay.setText(f'Mã sinh viên : {msv}')
        self.classDisplay.setText(f'Lớp : {lop}')
        self.sjDisplay.setText(f'Môn học : {subject}')

        Dialog.setFixedHeight(596)
        Dialog.setFixedWidth(801)

        css_display = "font-size: 13px; font-weight:300; color: white;background-color: rgb(84, 136, 237)"
        self.nameDisplay.setStyleSheet(css_display)
        self.idDisplay.setStyleSheet(css_display)
        self.classDisplay.setStyleSheet(css_display)
        self.sjDisplay.setStyleSheet(css_display)
        self.label_6.setStyleSheet(css_display)
        self.markDisplay.setStyleSheet(css_display)

        self.viewButton.setStyleSheet(
            "QPushButton{border-radius: 8px; font-weight:400;background-color: #e9e3df; color:black; font-size: 13px;}QPushButton:hover{color: white;background-color: rgb(85, 170, 127);}QPushButton:focus{outline:none;}")
        self.submitButton.setStyleSheet(
            "QPushButton{border-radius: 8px; font-weight:400;background-color: #e9e3df; color:black; font-size: 13px;}QPushButton:hover{color: white;background-color: rgb(85, 170, 127);}QPushButton:focus{outline:none;}")
        self.exitButton.setStyleSheet(
            "QPushButton{border-radius: 8px; font-weight:400;background-color: #e9e3df; color:black; font-size: 13px;}QPushButton:hover{color: white;background-color: #d43d41;}QPushButton:focus{outline:none;}")

        self.titleList.setStyleSheet("color: black; font-size: 12px; border: 0px solid #ccc;")

        url_problem = f"http://test.iptech.edu.vn/finetest4/api-user-subject-set.php?userid={user_id}&subjectid={_main_sj_id}"
        res_problem = requests.get(url_problem)
        content = res_problem.json()
        score = 0

        qr = Dialog.frameGeometry()
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        Dialog.move(qr.topLeft())

        total_pr = len(content)

        totalScore = total_pr * 100
        self.viewButton.clicked.connect(lambda x: viewProblem())
        self.exitButton.clicked.connect(lambda x: endProgram())
        self.submitButton.clicked.connect(lambda x: submit())

        self.tableWidget = self.titleList

        # Row count
        self.tableWidget.setRowCount(total_pr + 1)

        # Column count
        self.tableWidget.setColumnCount(6)
        self.tableWidget.verticalHeader().setVisible(False)

        i = 1
        global problemList
        problemList = []
        for item in content:
            problem = Problem(item['problem_id'], item['problem_nickname'], item["problem_fullname"],
                              item["problem_content"], item["problem_testcase"], item["problem_maxtime"],
                              item["problem_topic"], item["score"], item["tryhard"])
            problemList.append(problem)
            exercise_id = item['problem_nickname']
            self.tableWidget.setItem(i, 0, QTableWidgetItem(exercise_id))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(item["problem_fullname"]))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(item["problem_topic"]))
            pr_maxtime = int(item['problem_maxtime']) / 1000
            self.tableWidget.setItem(i, 3, QTableWidgetItem(str(pr_maxtime) + " giây"))
            self.tableWidget.item(i, 3).setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            submit_times = item["tryhard"]
            if submit_times == None: submit_times = '0'
            temp_score = item["score"]
            if temp_score == None: temp_score = '0'
            self.tableWidget.setItem(i, 5, QTableWidgetItem(str(submit_times)))
            self.tableWidget.item(i, 5).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tableWidget.setItem(i, 4, QTableWidgetItem(str(temp_score)))
            self.tableWidget.item(i, 4).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if (temp_score == '100'):
                score += 100
                for k in range(6):
                    self.tableWidget.item(i, k).setForeground(QtGui.QColor(225, 61, 65))
            i += 1
        self.markDisplay.setText(f'Điểm tổng : {score} / {totalScore}')

        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.EditTrigger.NoEditTriggers)
        self.tableWidget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget.setShowGrid(False)
        font = self.tableWidget.font()
        font.setWeight(300)
        self.tableWidget.setFont(font)

        # Table will fit the screen horizontally
        self.tableWidget.setHorizontalHeaderLabels(['MÃ BÀI', 'BÀI TẬP', 'CHỦ ĐỀ', 'GIỚI HẠN', 'ĐIỂM', 'NỘP'])
        self.tableWidget.setColumnWidth(0, 60)
        self.tableWidget.setColumnWidth(1, 250)
        self.tableWidget.setColumnWidth(2, 200)
        self.tableWidget.setColumnWidth(3, 80)
        self.tableWidget.setColumnWidth(4, 60)
        self.tableWidget.setColumnWidth(5, 50)
        self.tableWidget.horizontalHeader().setStyleSheet("QHeaderView { font: bold; font-size: 12px;}")

        self.scroll = self.statusScroll
        self.resultWidget = QWidget()
        self.vbox = QVBoxLayout()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        def viewProblem():
            global sj_code
            try:
                crRow = self.tableWidget.currentRow()
                pr_nickname = self.tableWidget.item(crRow, 0).text()
                filePath = f'{self.rootPath}/Problems/{pr_nickname}.pdf'
                if not os.path.exists(f"{self.rootPath}/Problems"):
                    os.makedirs(f"{self.rootPath}/Problems")
                isExist = os.system(f"open {filePath}")
                self.viewButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
                if isExist != 0:
                    url = f"http://test.iptech.edu.vn/finetest4/problem/{sj_code[0:4]}2021/{pr_nickname}.pdf"
                    try:
                        response = requests.get(url)
                        with open(f'{filePath}', 'wb') as f:
                            f.write(response.content)
                        subprocess.Popen(["open", filePath])
                        self.viewButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
                    except:
                        QMessageBox.about(self.widget, "Thông báo", "Không có kết nối Internet!")
            except:
                pass

        def submit():
            try:
                global score, totalScore, msv, _main_sj_id, _sj_langs, content, sj_code
                tempScore = 0
                crRow = self.tableWidget.currentRow()
                problem_index = int(crRow) - 1
                problem = problemList[int(crRow) - 1]
                pr_maxtime = int(int(problem.timeLimit) / 1000)
                pr_nickname = problem.nickName
                if not os.path.exists(f"{self.rootPath}/Testcase"):
                    os.makedirs(f"{self.rootPath}/Testcase")
                zipFileUrl = f'http://test.iptech.edu.vn/finetest4/problem/{sj_code[0:4]}2021/{pr_nickname}.zip'
                req = requests.get(zipFileUrl)
                zipFileName = f'{self.rootPath}/Testcase/{pr_nickname}.zip'
                with open(zipFileName, 'wb') as output_file:
                    output_file.write(req.content)

                with zipfile.ZipFile(zipFileName, 'r') as zip_ref:
                    zip_ref.extractall(f'{self.rootPath}/TestCase')

                subprocess.run(f"rm {zipFileName}", shell=True)

                testcase_amount = len(os.listdir(f"{self.rootPath}/TestCase/{pr_nickname}")) // 2
                if (_sj_langs != None):
                    subject_langs = ""
                    for item in _sj_langs.split():
                        subject_langs += "*" + item + " "
                        if (item == ".c"):
                            subject_langs += "*.cpp "
                else:
                    subject_langs = "*.cpp *.py"
                try:
                    path = QFileDialog.getOpenFileName(self.widget, 'Open a file', '', f'All Files ({subject_langs})')
                except:
                    pass
                if path != ('', ''):
                    try:
                        newFolderPath = f"{self.rootPath}/User/{pr_nickname}"
                        os.makedirs(newFolderPath)
                    except:
                        pass
                    object = QLabel("---BẮT ĐẦU CHẤM BÀI---")
                    object.setStyleSheet("color: black; font-size:11px;")
                    self.vbox.addWidget(object)
                    self.resultWidget.setLayout(self.vbox)
                    self.scroll.setWidget(self.resultWidget)
                    self.scroll.verticalScrollBar().rangeChanged.connect(lambda x: ResizeScroll())

                    if path[0][-3:] == '.py':
                        drRun = f'python3 {path[0]}'
                    else:
                        drRun = f'{self.rootPath}/a.out'
                    self.progressBar.setVisible(True)
                    prbar_val = 100 / testcase_amount
                    for i in range(1, testcase_amount + 1):
                        if i == 1 and path[0][-3:] == 'cpp':
                            try:
                                isCompiled = os.system(f'cd {self.rootPath}\ng++ {path[0]}')
                                if isCompiled != 0: 
                                    raise Exception("Can not compile!")
                            except:
                                isCompiled = os.system(f'cd {self.rootPath}\ngcc {path[0]}')
                                if(isCompiled != 0):
                                    object = QLabel("Kết quả: Lỗi thực thi")
                                    object.setStyleSheet("color: red; font-size:12px;")
                                    self.vbox.addWidget(object)
                                    self.resultWidget.setLayout(self.vbox)
                                    self.scroll.setWidget(self.resultWidget)
                                    self.scroll.verticalScrollBar().rangeChanged.connect(lambda x: ResizeScroll())
                                    break
                        try:
                            process = subprocess.Popen(
                                f"{drRun} <{self.rootPath}/TestCase/{pr_nickname}/{i}.inp> {self.rootPath}/User/{pr_nickname}/output{i}.out",
                                shell=True)
                        except:
                            object = QLabel("Kết quả: Lỗi thực thi")
                            object.setStyleSheet("color: red; font-size:12px;")
                            self.vbox.addWidget(object)
                            self.resultWidget.setLayout(self.vbox)
                            self.scroll.setWidget(self.resultWidget)
                            self.scroll.verticalScrollBar().rangeChanged.connect(lambda x: ResizeScroll())
                            break

                        try:
                            start_time = time.time()
                            process.wait(timeout=pr_maxtime)
                            file1 = open(f"{self.rootPath}/TestCase/{pr_nickname}/{i}.out", 'r')
                            var1 = file1.read()
                            file1.close()

                            file1 = open(f'{self.rootPath}/User/{pr_nickname}/output{i}.out', 'r')
                            var2 = file1.read()
                            file1.close()

                            exe_time = round((time.time() - start_time), 3)

                            if var2 == var1:
                                tempScore += 20
                                object = QLabel(
                                    f'[{pr_nickname}] Test {i}: Hoàn toàn chính xác - thời gian chạy {exe_time}s')
                                object.setStyleSheet("color: green; font-size:11px;")
                                self.vbox.addWidget(object)
                                self.resultWidget.setLayout(self.vbox)
                                self.scroll.setWidget(self.resultWidget)
                                self.scroll.verticalScrollBar().rangeChanged.connect(lambda x: ResizeScroll())
                                QApplication.processEvents()

                            else:
                                tempVar1 = var1.split()
                                tempVar2 = var2.split()

                                if ''.join(tempVar2) == ''.join(tempVar1):
                                    tempScore += 15
                                    object = QLabel(f'[{pr_nickname}] Test {i}: Đúng nhưng sai sót về trình bày')
                                    object.setStyleSheet("color: black; font-size:11px;")
                                    self.vbox.addWidget(object)
                                    self.resultWidget.setLayout(self.vbox)
                                    self.scroll.setWidget(self.resultWidget)
                                    self.scroll.verticalScrollBar().rangeChanged.connect(lambda x: ResizeScroll())

                                    # prevent freeze
                                    QApplication.processEvents()

                                else:
                                    object = QLabel(
                                        f'[{pr_nickname}] Test {i}: Kết quả sai, hãy kiểm tra lại bài làm - thời gian chạy {exe_time}s')
                                    object.setStyleSheet("color: #ef3d41; font-size:11px;")
                                    self.vbox.addWidget(object)
                                    self.resultWidget.setLayout(self.vbox)
                                    self.scroll.setWidget(self.resultWidget)
                                    self.scroll.verticalScrollBar().rangeChanged.connect(lambda x: ResizeScroll())
                                    QApplication.processEvents()

                        except subprocess.TimeoutExpired:
                            exe_time = round((time.time() - start_time), 3)
                            os.system("pkill a.out")
                            process.kill()
                            object = QLabel(
                                f'[{pr_nickname}] Test {i}: Chương trình chạy quá thời gian - thời gian chạy {exe_time}s')
                            object.setStyleSheet("color: red; font-size:11px;")
                            self.vbox.addWidget(object)
                            self.resultWidget.setLayout(self.vbox)
                            self.scroll.setWidget(self.resultWidget)
                            self.scroll.verticalScrollBar().rangeChanged.connect(lambda x: ResizeScroll())
                            QApplication.processEvents()

                        self.progressBar.setValue(int(i * prbar_val))
                    self.progressBar.setVisible(False)
                    object = QLabel(f'=== KẾT THÚC: ĐIỂM {tempScore}% ===')
                    object.setStyleSheet("color: black; font-size:11px;")
                    self.vbox.addWidget(object)
                    self.resultWidget.setLayout(self.vbox)
                    self.scroll.setWidget(self.resultWidget)
                    self.scroll.verticalScrollBar().rangeChanged.connect(lambda x: ResizeScroll())

                    userScore = float(content[problem_index]['score']) if content[problem_index]['score'] != None else 0

                    if (tempScore > userScore):
                        self.tableWidget.setItem(crRow, 4, QTableWidgetItem(f'{float(tempScore)}'))
                        self.tableWidget.item(crRow, 4).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        # .....update score to database.....

                        #   # Update submit_times
                        submit_times = int(content[problem_index]['tryhard']) if content[problem_index][
                                                                                     'tryhard'] != None else 0
                        self.tableWidget.setItem(crRow, 5, QTableWidgetItem(f'{submit_times + 1}'))
                        self.tableWidget.item(crRow, 5).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        # .....update tryhard to database.....

                        if (tempScore == 100):
                            for i in range(6):
                                self.tableWidget.item(crRow, i).setForeground(QtGui.QColor(20,205,50))
                        score += tempScore
                        self.markDisplay.setText(f'Điểm tổng : {score} / {totalScore}')
                    else:
                        object = QLabel("--GIỮ NGUYÊN ĐIỂM--")
                        self.vbox.addWidget(object)
                        self.resultWidget.setLayout(self.vbox)
                        self.scroll.setWidget(self.resultWidget)
                        self.scroll.verticalScrollBar().rangeChanged.connect(lambda x: ResizeScroll())
                    subprocess.run(f"rm {self.rootPath}/a.out", shell=True)
                else:
                    pass
                self.submitButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            except Exception as e:
                pass

        def ResizeScroll():  # auto scroll
            maxi = self.scroll.verticalScrollBar().maximum()
            self.scroll.verticalScrollBar().setValue(maxi)

        def endProgram():
            app.exit()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "FineTest"))
        self.submitButton.setText(_translate("Dialog", "NỘP BÀI"))
        self.label_6.setText(_translate("Dialog", "Bộ đề :  Bài thực hành mở"))
        self.exitButton.setText(_translate("Dialog", "THOÁT"))
        self.label_11.setText(_translate("Dialog", "NỘP"))
        self.viewButton.setText(_translate("Dialog", "XEM ĐỀ BÀI"))

    def process_finished(self):
        self.proc = None


if __name__ == "__main__":
    rootPath = pathlib.Path(__file__).parent.resolve()
    _version = 1.8
    url = f"https://bsite.net/tuanvu02/version.txt"
    version = float(requests.get(url).text.strip())
    if (version > _version):
        root = tk.Tk()
        root.withdraw()
        ans = messagebox.askyesno("Thông báo", "Hiện đã có phiên bản mới\nTải ngay?")
        if (ans):
            subprocess.run(f"open {rootPath}/update.app", shell=True)
        sys.exit()
    else:
        app = QtWidgets.QApplication(sys.argv)
        Dialog = QtWidgets.QDialog()
        ui = LoginPage()
        ui.setupUi(Dialog)
        Dialog.show()

        app.exec()
