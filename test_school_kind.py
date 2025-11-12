import requests

api_key = "3aeace82f952472ab2151a44cf0e736b"
base_url = "https://open.neis.go.kr/hub"

# 학교 정보에서 학교 종류 코드 추출
def get_school_info(atpt_code, sd_code):
    """학교 정보 조회하여 학교 종류 코드 획득"""
    try:
        url = f"{base_url}/schoolInfo"
        params = {
            'KEY': api_key,
            'Type': 'json',
            'SD_SCHUL_CODE': sd_code
        }
        
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        
        if 'schoolInfo' in data and len(data['schoolInfo']) > 1:
            school_data = data['schoolInfo'][1]['row'][0]
            print(f"학교명: {school_data.get('SCHUL_NM')}")
            print(f"학교 종류명: {school_data.get('SCHUL_KND_SC_NM')}")
            return school_data
        
    except Exception as e:
        print(f"학교 정보 조회 에러: {e}")
    
    return None

# 급식 정보 조회 - 학교 종류 코드 포함
def test_meal_with_school_kind(atpt_code, sd_code, meal_date):
    """학교 종류 코드를 포함하여 급식 조회"""
    
    school_info = get_school_info(atpt_code, sd_code)
    if not school_info:
        print("학교 정보를 찾을 수 없습니다.")
        return
    
    # 학교 종류별 코드 매핑 (NEIS API 기준)
    school_kind_map = {
        '유치원': '01',
        '초등학교': '02',
        '중학교': '03',
        '고등학교': '04'
    }
    
    school_kind_name = school_info.get('SCHUL_KND_SC_NM', '')
    school_kind_code = school_kind_map.get(school_kind_name, '03')
    
    print(f"\n학교 종류 코드: {school_kind_code}")
    
    # 학교 종류 코드를 포함하여 급식 조회
    print("\n급식 정보 조회 시도 (학교 종류 코드 포함):")
    params = {
        'KEY': api_key,
        'Type': 'json',
        'ATPT_OFCDE': atpt_code,
        'SD_SCHUL_CODE': sd_code,
        'MLSV_YMD': meal_date
    }
    
    try:
        response = requests.get(f"{base_url}/mealServiceDietInfo", params=params, timeout=5)
        print(f"상태: {response.status_code}")
        data = response.json()
        
        if 'RESULT' in data and data['RESULT']['CODE'] != 'INFO-000':
            print(f"에러: {data['RESULT']}")
        
        if 'mealServiceDietInfo' in data:
            meals = data['mealServiceDietInfo']
            print(f"전체 응답 구조: {data}")
            
            if len(meals) > 1:
                print(f"\n급식 데이터 발견:")
                for meal in meals[1:]:
                    print(f"  날짜: {meal.get('MLSV_YMD')}")
                    print(f"  메뉴: {meal.get('DDISH_NM')}")
            else:
                print("급식 데이터가 없습니다.")
        else:
            print(f"전체 응답: {data}")
            
    except Exception as e:
        print(f"에러: {e}")

# 실행
print("=" * 60)
print("오금중학교 (7130197) 급식 조회")
print("=" * 60)
test_meal_with_school_kind("B10", "7130197", "20251112")

# 다른 형태의 요청도 시도
print("\n" + "=" * 60)
print("대체 API 엔드포인트 확인")
print("=" * 60)

# mealServiceDietInfo 외에 다른 엔드포인트 시도
endpoints = [
    "mealServiceDietInfo",
    "mealServiceDietInfoV1", 
    "schoolMealServiceDietInfo",
    "mealCal"
]

for endpoint in endpoints:
    try:
        url = f"{base_url}/{endpoint}"
        params = {
            'KEY': api_key,
            'Type': 'json',
            'ATPT_OFCDE': 'B10',
            'SD_SCHUL_CODE': '7130197',
            'MLSV_YMD': '20251112'
        }
        response = requests.get(url, params=params, timeout=5)
        print(f"\n{endpoint}: {response.status_code}")
        data = response.json()
        if 'mealServiceDietInfo' in data or 'schoolMealServiceDietInfo' in data:
            print(f"  ✓ 데이터 발견: {list(data.keys())}")
        elif 'RESULT' in data:
            print(f"  상태: {data['RESULT']['MESSAGE']}")
    except Exception as e:
        print(f"\n{endpoint}: 에러 - {e}")
