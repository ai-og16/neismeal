import requests

# NEIS API를 이용해서 학교 정보 확인
api_key = "3aeace82f952472ab2151a44cf0e736b"
base_url = "https://open.neis.go.kr/hub"

# 1. 학교 검색 API 테스트
def search_school(atpt_code, school_name):
    """학교명으로 학교 검색"""
    try:
        url = f"{base_url}/schoolInfo"
        params = {
            'KEY': api_key,
            'Type': 'json',
            'pIndex': 1,
            'pSize': 100,
            'ATPT_OFCDE': atpt_code,
            'SCHUL_NM': school_name
        }
        
        response = requests.get(url, params=params, timeout=5)
        print(f"요청 URL: {response.url}")
        print(f"상태 코드: {response.status_code}")
        
        data = response.json()
        print(f"응답 데이터: {data}")
        
        if 'schoolInfo' in data:
            schools = data['schoolInfo']
            if len(schools) > 1:
                for school in schools[1:]:
                    print(f"\n학교명: {school.get('SCHUL_NM')}")
                    print(f"학교 행정 코드: {school.get('SD_SCHUL_CODE')}")
                    print(f"주소: {school.get('ORG_RDNMA')}")
        return data
    except Exception as e:
        print(f"에러: {e}")

# 2. 급식 정보 조회 테스트
def test_meal_info(atpt_code, sd_code, meal_date):
    """급식 정보 조회"""
    try:
        url = f"{base_url}/mealServiceDietInfo"
        params = {
            'KEY': api_key,
            'Type': 'json',
            'pIndex': 1,
            'pSize': 100,
            'ATPT_OFCDE': atpt_code,
            'SD_SCHUL_CODE': sd_code,
            'MLSV_YMD': meal_date
        }
        
        response = requests.get(url, params=params, timeout=5)
        print(f"\n급식 조회 URL: {response.url}")
        print(f"상태 코드: {response.status_code}")
        
        data = response.json()
        print(f"응답 데이터: {data}")
        
        if 'mealServiceDietInfo' in data:
            meals = data['mealServiceDietInfo']
            print(f"급식 데이터 개수: {len(meals)}")
            if len(meals) > 1:
                for meal in meals[1:]:
                    print(f"\n급식 날짜: {meal.get('MLSV_YMD')}")
                    print(f"급식 내용: {meal.get('DDISH_NM')}")
        return data
    except Exception as e:
        print(f"에러: {e}")

print("=" * 60)
print("1. 오금중학교 검색")
print("=" * 60)
search_school("B10", "오금중학교")

print("\n" + "=" * 60)
print("2. 코드 7130197로 급식 조회 (2025-11-12)")
print("=" * 60)
test_meal_info("B10", "7130197", "20251112")

print("\n" + "=" * 60)
print("3. 코드로 학교 정보 직접 조회")
print("=" * 60)
try:
    url = f"{base_url}/schoolInfo"
    params = {
        'KEY': api_key,
        'Type': 'json',
        'pIndex': 1,
        'pSize': 100,
        'SD_SCHUL_CODE': '7130197'
    }
    
    response = requests.get(url, params=params, timeout=5)
    print(f"URL: {response.url}")
    data = response.json()
    print(f"응답: {data}")
    
    if 'schoolInfo' in data and len(data['schoolInfo']) > 1:
        school = data['schoolInfo'][1]
        print(f"\n학교명: {school.get('SCHUL_NM')}")
        print(f"학교 종류: {school.get('SCHUL_KND_SC_NM')}")
        print(f"주소: {school.get('ORG_RDNMA')}")
except Exception as e:
    print(f"에러: {e}")
