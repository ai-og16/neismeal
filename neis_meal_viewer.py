import sys
import requests
import webbrowser
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import QDate, Qt, QSettings
from PyQt5.QtGui import QFont

class MealApp(QWidget):
    def __init__(self):
        super().__init__()
        self.api_key = '3aeace82f952472ab2151a44cf0e736b'
        self.settings = QSettings("SangminApp", "MealApp")
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Sangmin's 학교 급식 정보 조회 앱")
        self.setGeometry(300, 300, 800, 600)
        main_layout = QVBoxLayout()

        title_label = QLabel("Sangmin's 학교 급식 정보 조회 앱")
        title_label.setFont(QFont('Arial', 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)

        input_layout = QHBoxLayout()
        edu_code_label = QLabel('교육청 코드:')
        self.edu_code_input = QLineEdit()
        self.edu_code_input.setPlaceholderText("예: B10")
        school_code_label = QLabel('학교 코드:')
        self.school_code_input = QLineEdit()
        self.school_code_input.setPlaceholderText("예: 7010578")
        self.load_settings()

        code_search_label = QLabel('#교육청 및 학교 코드 조회</a>')
        code_search_label.setOpenExternalLinks(False)
        code_search_label.linkActivated.connect(self.search_codes)

        search_button = QPushButton('조회')
        search_button.clicked.connect(self.get_meals)

        input_layout.addWidget(edu_code_label)
        input_layout.addWidget(self.edu_code_input)
        input_layout.addWidget(school_code_label)
        input_layout.addWidget(self.school_code_input)
        input_layout.addWidget(code_search_label)
        input_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        input_layout.addWidget(search_button)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['날짜', '급식 메뉴'])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        # 세로 헤더도 내용에 맞춰 자동 크기 조정
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        main_layout.addWidget(title_label)
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)
        self.show_message("조회할 정보를 입력하세요.")

    def load_settings(self):
        edu_code = self.settings.value("edu_code", "")
        school_code = self.settings.value("school_code", "")
        self.edu_code_input.setText(edu_code)
        self.school_code_input.setText(school_code)

    def search_codes(self):
        webbrowser.open('https://open.neis.go.kr/portal/data/service/selectServicePage.do?page=1&rows=10&sortColumn=&sortDirection=&infId=OPEN17320190722180924242823&infSeq=1&cateId=C0001')

    def get_meals(self):
        edu_code = self.edu_code_input.text().strip()
        school_code = self.school_code_input.text().strip()
        if not edu_code or not school_code:
            QMessageBox.warning(self, '입력 오류', '교육청 코드와 학교 코드를 모두 입력해주세요.')
            return
        self.settings.setValue("edu_code", edu_code)
        self.settings.setValue("school_code", school_code)
        today = QDate.currentDate()
        start_date = today.toString('yyyyMMdd')
        end_date = today.addDays(6).toString('yyyyMMdd')
        url = 'https://open.neis.go.kr/hub/mealServiceDietInfo'
        params = {
            'KEY': self.api_key,
            'Type': 'json',
            'pIndex': 1,
            'pSize': 100,
            'ATPT_OFCDC_SC_CODE': edu_code,
            'SD_SCHUL_CODE': school_code,
            'MLSV_FROM_YMD': start_date,
            'MLSV_TO_YMD': end_date
        }
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            meal_dict = {}
            if 'mealServiceDietInfo' in data:
                # API 구조에 따라 row 추출
                meal_info = data['mealServiceDietInfo']
                rows = []
                if isinstance(meal_info, list):
                    for item in meal_info:
                        if isinstance(item, dict) and 'row' in item:
                            rows = item['row']
                            break
                elif isinstance(meal_info, dict) and 'row' in meal_info:
                    rows = meal_info['row']
                for meal in rows:
                    meal_dict[meal['MLSV_YMD']] = meal['DDISH_NM'].replace('<br/>', '\n')
            # 날짜별로 모두 표시
            meals = []
            for i in range(7):
                qdate = today.addDays(i)
                ymd = qdate.toString('yyyyMMdd')
                menu = meal_dict.get(ymd, "급식 없음")
                meals.append({'MLSV_YMD': ymd, 'DDISH_NM': menu})
            self.display_meals(meals)
        except Exception as e:
            self.show_message(f"오류: {str(e)}")

    def display_meals(self, meals):
        self.table.setRowCount(len(meals))
        day_names = ["월", "화", "수", "목", "금", "토", "일"]
        for i, meal in enumerate(meals):
            date_str = meal['MLSV_YMD']
            qdate = QDate.fromString(date_str, 'yyyyMMdd')
            day_of_week = day_names[qdate.dayOfWeek() - 1]
            formatted_date = f"{qdate.toString('yyyy-MM-dd')} ({day_of_week})"
            menu = meal['DDISH_NM']
            self.table.setItem(i, 0, QTableWidgetItem(formatted_date))
            self.table.setItem(i, 1, QTableWidgetItem(menu))
        self.table.resizeRowsToContents()

    def show_message(self, message):
        self.table.clearContents()
        self.table.setRowCount(1)
        item = QTableWidgetItem(message)
        item.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(0, 0, item)
        self.table.setSpan(0, 0, 1, 2)
        self.table.resizeRowsToContents()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MealApp()
    ex.show()
    sys.exit(app.exec_())