import sys
from datetime import datetime, timedelta
import requests
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QTableWidget, 
                             QTableWidgetItem, QMessageBox, QDateEdit, QGroupBox)
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QFont, QColor

class MealViewerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.api_key = "3aeace82f952472ab2151a44cf0e736b"
        self.base_url = "https://open.neis.go.kr/hub"
        self.init_ui()
        
    def init_ui(self):
        """GUI 초기화"""
        self.setWindowTitle('NEIS 급식 조회 시스템')
        self.setGeometry(100, 100, 1000, 700)
        
        # 메인 레이아웃
        main_layout = QVBoxLayout()
        
        # 1. 제목
        title_label = QLabel('NEIS 급식 조회 시스템')
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)
        
        # 2. 검색 조건 그룹
        search_group = QGroupBox("검색 조건")
        search_layout = QHBoxLayout()
        
        # 교육청 코드
        search_layout.addWidget(QLabel('교육청 코드:'))
        self.atpt_code_input = QLineEdit()
        self.atpt_code_input.setPlaceholderText('예: B10 (서울), C10 (부산)')
        self.atpt_code_input.setText('B10')
        self.atpt_code_input.setMaximumWidth(200)
        search_layout.addWidget(self.atpt_code_input)
        
        # 학교 행정 코드
        search_layout.addWidget(QLabel('학교 행정 코드:'))
        self.sd_code_input = QLineEdit()
        self.sd_code_input.setPlaceholderText('예: 7130197')
        self.sd_code_input.setText('7130197')
        self.sd_code_input.setMaximumWidth(200)
        search_layout.addWidget(self.sd_code_input)
        
        # 조회 시작일
        search_layout.addWidget(QLabel('조회 시작일:'))
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        search_layout.addWidget(self.date_input)
        
        search_layout.addStretch()
        
        # 조회 버튼
        self.search_button = QPushButton('급식 조회')
        self.search_button.setMaximumWidth(100)
        self.search_button.clicked.connect(self.search_meals)
        search_layout.addWidget(self.search_button)
        
        search_group.setLayout(search_layout)
        main_layout.addWidget(search_group)
        
        # 3. 설명 레이블
        info_label = QLabel('※ 교육청 코드와 학교 행정 코드를 입력하고 조회 버튼을 클릭하세요. (7일간의 급식 정보 표시)')
        info_label.setStyleSheet("color: #666666; font-size: 10px;")
        main_layout.addWidget(info_label)
        
        # 4. 결과 테이블
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(2)
        self.result_table.setHorizontalHeaderLabels(['날짜', '급식 내용'])
        self.result_table.horizontalHeader().setStretchLastSection(True)
        main_layout.addWidget(self.result_table)
        
        # 5. 상태 메시지 레이블
        self.status_label = QLabel('준비 완료')
        self.status_label.setStyleSheet("color: #0066cc; font-weight: bold;")
        main_layout.addWidget(self.status_label)
        
        self.setLayout(main_layout)
        
    def search_meals(self):
        """급식 정보 조회"""
        atpt_code = self.atpt_code_input.text().strip()
        sd_code = self.sd_code_input.text().strip()
        
        # 입력 값 검증
        if not atpt_code or not sd_code:
            QMessageBox.warning(self, '입력 오류', '교육청 코드와 학교 행정 코드를 입력해주세요.')
            return
        
        # 학교 행정 코드는 숫자여야 함
        try:
            sd_code_int = int(sd_code)
        except ValueError:
            QMessageBox.warning(self, '입력 오류', '학교 행정 코드는 숫자여야 합니다.')
            return
        
        self.status_label.setText('조회 중...')
        self.status_label.setStyleSheet("color: #ff9900; font-weight: bold;")
        QApplication.processEvents()
        
        try:
            # 시작일부터 7일간의 급식 정보 조회
            start_date = self.date_input.date().toPyDate()
            meals_data = {}
            
            for i in range(7):
                current_date = start_date + timedelta(days=i)
                meals_info = self.fetch_meal_info(atpt_code, sd_code, current_date)
                
                if meals_info:
                    meals_data[current_date] = meals_info
            
            if meals_data:
                self.display_results(meals_data)
                self.status_label.setText(f'조회 완료 - {len(meals_data)}일의 급식 정보를 표시합니다.')
                self.status_label.setStyleSheet("color: #009900; font-weight: bold;")
            else:
                QMessageBox.information(self, '조회 결과', '해당 기간의 급식 정보가 없습니다.\n학교 코드를 확인해주세요.')
                self.status_label.setText('조회 완료 - 결과 없음')
                self.status_label.setStyleSheet("color: #ff0000; font-weight: bold;")
                
        except Exception as e:
            QMessageBox.critical(self, '오류', f'조회 중 오류가 발생했습니다:\n{str(e)}')
            self.status_label.setText('오류 발생')
            self.status_label.setStyleSheet("color: #ff0000; font-weight: bold;")
    
    def fetch_meal_info(self, atpt_code, sd_code, target_date):
        """NEIS API에서 급식 정보 조회
        
        API 문제로 인해 URL 직접 구성으로 변경
        """
        try:
            # 날짜를 YYYYMMDD 형식으로 변환
            meal_date = target_date.strftime('%Y%m%d')
            
            # NEIS API 요청 - 여러 형식으로 시도
            params = {
                'KEY': self.api_key,
                'Type': 'json',
                'pIndex': 1,
                'pSize': 100,
                'ATPT_OFCDE': atpt_code,
                'SD_SCHUL_CODE': sd_code,
                'MLSV_YMD': meal_date
            }
            
            url = f"{self.base_url}/mealServiceDietInfo"
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            # 응답 데이터 파싱
            if 'mealServiceDietInfo' in data:
                meals_list = data['mealServiceDietInfo']
                if meals_list and len(meals_list) > 1:
                    # 첫 번째 요소는 결과 정보, 나머지가 실제 데이터
                    for meal_data in meals_list[1:]:
                        if isinstance(meal_data, dict) and 'DDISH_NM' in meal_data:
                            meals_str = meal_data['DDISH_NM'].replace('<br/>', '\n')
                            return meals_str
            
            # API 응답이 없으면 None 반환
            return None
            
        except requests.exceptions.RequestException as e:
            # 네트워크 에러는 조용히 처리
            print(f"API 요청 실패 ({meal_date}): {str(e)}")
            return None
        except (KeyError, IndexError, ValueError) as e:
            # 데이터 파싱 에러는 조용히 처리
            print(f"데이터 파싱 오류 ({meal_date}): {str(e)}")
            return None
    
    def display_results(self, meals_data):
        """결과를 테이블에 표시"""
        self.result_table.setRowCount(0)
        
        # 날짜 순서대로 정렬
        sorted_dates = sorted(meals_data.keys())
        
        for idx, date in enumerate(sorted_dates):
            self.result_table.insertRow(idx)
            
            # 날짜 열
            date_str = date.strftime('%Y-%m-%d (%a)')
            date_item = QTableWidgetItem(date_str)
            date_item.setFont(QFont('Arial', 10, QFont.Bold))
            self.result_table.setItem(idx, 0, date_item)
            
            # 급식 내용 열
            meal_content = meals_data[date]
            if meal_content:
                meal_item = QTableWidgetItem(meal_content)
            else:
                meal_item = QTableWidgetItem('급식 정보 없음')
                meal_item.setBackground(QColor('#ffe0e0'))
            
            meal_item.setFont(QFont('Arial', 9))
            meal_item.setAlignment(Qt.AlignTop | Qt.AlignLeft)
            self.result_table.setItem(idx, 1, meal_item)
            
            # 행 높이 자동 조정
            self.result_table.resizeRowToContents(idx)

def main():
    app = QApplication(sys.argv)
    viewer = MealViewerApp()
    viewer.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
