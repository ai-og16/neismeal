import requests

api_key = "3aeace82f952472ab2151a44cf0e736b"
base_url = "https://open.neis.go.kr/hub"

# 다양한 파라미터 조합 테스트
def test_meal_api():
    """여러 방식으로 급식 API 테스트"""
    
    # 테스트 데이터
    atpt_code = "B10"
    sd_code = "7130197"
    meal_date = "20251112"
    
    # 테스트 1: 기본 파라미터
    print("테스트 1: 기본 파라미터")
    params1 = {
        'KEY': api_key,
        'Type': 'json',
        'ATPT_OFCDE': atpt_code,
        'SD_SCHUL_CODE': sd_code,
        'MLSV_YMD': meal_date
    }
    try:
        response = requests.get(f"{base_url}/mealServiceDietInfo", params=params1, timeout=5)
        print(f"상태: {response.status_code}")
        print(f"응답: {response.json()}\n")
    except Exception as e:
        print(f"에러: {e}\n")
    
    # 테스트 2: pIndex, pSize 추가
    print("테스트 2: pIndex, pSize 추가")
    params2 = {
        'KEY': api_key,
        'Type': 'json',
        'pIndex': 1,
        'pSize': 100,
        'ATPT_OFCDE': atpt_code,
        'SD_SCHUL_CODE': sd_code,
        'MLSV_YMD': meal_date
    }
    try:
        response = requests.get(f"{base_url}/mealServiceDietInfo", params=params2, timeout=5)
        print(f"상태: {response.status_code}")
        print(f"응답: {response.json()}\n")
    except Exception as e:
        print(f"에러: {e}\n")
    
    # 테스트 3: 메뉴조회 API 사용
    print("테스트 3: 급식메뉴조회 API (mealServiceDietInfo 대신 사용)")
    params3 = {
        'KEY': api_key,
        'Type': 'json',
        'ATPT_OFCDE': atpt_code,
        'SD_SCHUL_CODE': sd_code,
        'MLSV_YMD': meal_date
    }
    try:
        response = requests.get(f"{base_url}/mealServiceDietInfo", params=params3, timeout=5)
        print(f"상태: {response.status_code}")
        data = response.json()
        print(f"응답: {data}\n")
        
        # 응답 구조 분석
        if 'mealServiceDietInfo' in data:
            print("mealServiceDietInfo 구조 확인:")
            meals = data['mealServiceDietInfo']
            print(f"전체 항목 수: {len(meals)}")
            if len(meals) > 0:
                print(f"첫 번째 항목 (메타데이터): {meals[0]}")
                if len(meals) > 1:
                    print(f"두 번째 항목 (데이터): {meals[1]}")
    except Exception as e:
        print(f"에러: {e}\n")
    
    # 테스트 4: 다른 날짜 시도
    print("테스트 4: 다른 날짜로 시도 (20251110 - 월요일)")
    params4 = {
        'KEY': api_key,
        'Type': 'json',
        'ATPT_OFCDE': atpt_code,
        'SD_SCHUL_CODE': sd_code,
        'MLSV_YMD': '20251110'
    }
    try:
        response = requests.get(f"{base_url}/mealServiceDietInfo", params=params4, timeout=5)
        print(f"상태: {response.status_code}")
        data = response.json()
        print(f"응답: {data}\n")
    except Exception as e:
        print(f"에러: {e}\n")

test_meal_api()
