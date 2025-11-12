import requests
from datetime import datetime, timedelta

api_key = '3aeace82f952472ab2151a44cf0e736b'

# 오금중학교 (B10, 7130197)
atpt_code = 'B10'
sd_code = '7130197'

print("=" * 80)
print("오금중학교 급식 정보 조회 - 날짜별 상세 확인")
print("=" * 80)

# 오늘부터 14일까지 조회
today = datetime.now()

for i in range(14):
    target_date = today + timedelta(days=i)
    date_str = target_date.strftime('%Y%m%d')
    day_name = ['월', '화', '수', '목', '금', '토', '일'][target_date.weekday()]
    
    url = 'https://open.neis.go.kr/hub/mealServiceDietInfo'
    params = {
        'KEY': api_key,
        'Type': 'json',
        'pIndex': 1,
        'pSize': 100,
        'ATPT_OFCDC_SC_CODE': atpt_code,
        'SD_SCHUL_CODE': sd_code,
        'MLSV_FROM_YMD': date_str,
        'MLSV_TO_YMD': date_str
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        status = "❌ 데이터 없음"
        if 'mealServiceDietInfo' in data and len(data['mealServiceDietInfo']) > 1:
            try:
                meals = data['mealServiceDietInfo'][1]['row']
                if meals:
                    menu = meals[0]['DDISH_NM'][:50]
                    status = f"✓ 있음: {menu}..."
            except:
                status = "⚠ 에러"
        
        print(f"{target_date.strftime('%Y-%m-%d')} ({day_name}): {status}")
        
    except Exception as e:
        print(f"{target_date.strftime('%Y-%m-%d')} ({day_name}): 요청 실패 - {e}")

print("\n" + "=" * 80)
print("기간 조회 테스트 (범위 조회)")
print("=" * 80)

# 오늘부터 7일 범위로 한 번에 조회
today = datetime.now()
start_date = today.strftime('%Y%m%d')
end_date = (today + timedelta(days=6)).strftime('%Y%m%d')

print(f"조회 범위: {start_date} ~ {end_date}")

url = 'https://open.neis.go.kr/hub/mealServiceDietInfo'
params = {
    'KEY': api_key,
    'Type': 'json',
    'pIndex': 1,
    'pSize': 100,
    'ATPT_OFCDC_SC_CODE': atpt_code,
    'SD_SCHUL_CODE': sd_code,
    'MLSV_FROM_YMD': start_date,
    'MLSV_TO_YMD': end_date
}

try:
    response = requests.get(url, params=params, timeout=10)
    data = response.json()
    
    print(f"\n응답 상태: {response.status_code}")
    
    if 'mealServiceDietInfo' in data:
        meal_info = data['mealServiceDietInfo']
        print(f"응답 구조: {type(meal_info)}")
        print(f"응답 항목 수: {len(meal_info)}")
        
        if len(meal_info) > 1:
            rows = meal_info[1]
            print(f"행 데이터 타입: {type(rows)}")
            
            if isinstance(rows, dict) and 'row' in rows:
                rows_list = rows['row']
                print(f"급식 데이터 수: {len(rows_list)}")
                
                for meal in rows_list:
                    print(f"\n  날짜: {meal['MLSV_YMD']}")
                    print(f"  메뉴: {meal['DDISH_NM'][:100]}")
            elif isinstance(rows, list):
                print(f"급식 데이터 수: {len(rows)}")
                for meal in rows:
                    print(f"\n  날짜: {meal['MLSV_YMD']}")
                    print(f"  메뉴: {meal['DDISH_NM'][:100]}")
    elif 'RESULT' in data:
        print(f"API 응답: {data['RESULT']}")
        
except Exception as e:
    print(f"요청 실패: {e}")
