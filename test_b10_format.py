import requests
import json

api_key = "3aeace82f952472ab2151a44cf0e736b"
base_url = "https://open.neis.go.kr/hub"

print("=" * 80)
print("NEIS 급식 정보 API - B10 형식 (올바른 형식으로 재시도)")
print("=" * 80)

# 학교 정보에서 얻은 정확한 코드: B10
test_requests = [
    {
        'name': 'B10 + 7130197 (원본 형식)',
        'atpt': 'B10',
        'sd_code': '7130197',
        'meal_date': '20251112'
    },
    {
        'name': 'B10을 소문자로',
        'atpt': 'b10',
        'sd_code': '7130197',
        'meal_date': '20251112'
    },
    {
        'name': '두자리 형식만',
        'atpt': '10',
        'sd_code': '7130197',
        'meal_date': '20251112'
    },
    {
        'name': '다른 날짜 (2025-11-10 월요일)',
        'atpt': 'B10',
        'sd_code': '7130197',
        'meal_date': '20251110'
    },
    {
        'name': '다른 날짜 (2025-11-13 목요일)',
        'atpt': 'B10',
        'sd_code': '7130197',
        'meal_date': '20251113'
    }
]

for test in test_requests:
    print(f"\n[{test['name']}]")
    
    params = {
        'KEY': api_key,
        'Type': 'json',
        'ATPT_OFCDE': test['atpt'],
        'SD_SCHUL_CODE': test['sd_code'],
        'MLSV_YMD': test['meal_date']
    }
    
    try:
        response = requests.get(f"{base_url}/mealServiceDietInfo", params=params, timeout=10)
        print(f"URL: {response.url}")
        print(f"상태: {response.status_code}")
        
        data = response.json()
        
        # 전체 응답 출력
        print(f"응답:\n{json.dumps(data, ensure_ascii=False, indent=2)}")
        
    except Exception as e:
        print(f"에러: {e}")

print("\n" + "=" * 80)
print("API 문서 참고: mealServiceDietInfo 대신 다른 엔드포인트")
print("=" * 80)

# NEIS 문서에 있는 다른 API들
other_endpoints = [
    'mealServiceDietInfo',
    'SchoolMealServiceDietInfo',
    'schoolMealServiceInfo',
    'mealServiceInfo',
    'foodInfo'
]

for endpoint in other_endpoints:
    try:
        url = f"{base_url}/{endpoint}"
        params = {
            'KEY': api_key,
            'Type': 'json',
            'ATPT_OFCDE': 'B10',
            'SD_SCHUL_CODE': '7130197',
            'MLSV_YMD': '20251112'
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        print(f"\n{endpoint}:")
        
        if 'RESULT' in data:
            print(f"  CODE: {data['RESULT']['CODE']}")
            print(f"  MESSAGE: {data['RESULT']['MESSAGE']}")
        else:
            print(f"  응답 키: {list(data.keys())}")
            print(f"  (가능한 엔드포인트)")
            
    except Exception as e:
        print(f"\n{endpoint}: {e}")
