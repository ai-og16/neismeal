import requests

api_key = "3aeace82f952472ab2151a44cf0e736b"
base_url = "https://open.neis.go.kr/hub"

# 여러 가능한 API 엔드포인트와 파라미터 조합 시도
test_cases = [
    {
        'name': '급식 검색 - 기본 필수 파라미터만',
        'url': f"{base_url}/mealServiceDietInfo",
        'params': {
            'KEY': api_key,
            'Type': 'json',
            'ATPT_OFCDE': '27',
            'SD_SCHUL_CODE': '7130197',
            'MLSV_YMD': '20251112'
        }
    },
    {
        'name': '급식 - Standard Info 포함',
        'url': f"{base_url}/mealServiceDietInfo",
        'params': {
            'KEY': api_key,
            'Type': 'json',
            'ATPT_OFCDE': '27',
            'SD_SCHUL_CODE': '7130197',
            'MLSV_YMD': '20251112',
            'pIndex': '1',
            'pSize': '100'
        }
    },
    {
        'name': '교육청명으로 조회 - ATPT_OFCDE 숫자 형식',
        'url': f"{base_url}/mealServiceDietInfo",
        'params': {
            'KEY': api_key,
            'Type': 'json',
            'ATPT_OFCDE': '서울특별시교육청',  # 교육청명으로 시도
            'SD_SCHUL_CODE': '7130197',
            'MLSV_YMD': '20251112'
        }
    },
    {
        'name': 'NEIS 문서: 필수 요청 매개변수 확인',
        'url': f"{base_url}/mealServiceDietInfo",
        'params': {
            'KEY': api_key,
            'Type': 'json',
            'ATPT_OFCDE': '27',
            'SD_SCHUL_CODE': '7130197',
            'MLSV_YMD': '20251112',
            'pIndex': 1,
            'pSize': 100
        }
    }
]

print("=" * 80)
print("NEIS API 급식 정보 조회 - 다양한 파라미터 조합 테스트")
print("=" * 80)

for test_case in test_cases:
    print(f"\n[{test_case['name']}]")
    
    try:
        response = requests.get(test_case['url'], params=test_case['params'], timeout=10)
        print(f"상태 코드: {response.status_code}")
        
        data = response.json()
        
        # 응답 구조 분석
        if 'RESULT' in data:
            print(f"RESULT CODE: {data['RESULT']['CODE']}")
            print(f"MESSAGE: {data['RESULT']['MESSAGE']}")
        
        if 'mealServiceDietInfo' in data:
            meals = data['mealServiceDietInfo']
            print(f"mealServiceDietInfo 응답 개수: {len(meals)}")
            
            if len(meals) > 0:
                print(f"첫 번째 항목: {meals[0]}")
                if len(meals) > 1:
                    print(f"두 번째 항목: {meals[1]}")
                    
        # 전체 응답 키 출력
        print(f"응답 키: {list(data.keys())}")
        
        # 에러가 아닌 경우 성공 표시
        if 'RESULT' not in data or data['RESULT']['CODE'] == 'INFO-000':
            print("✓ 성공")
        
    except requests.exceptions.RequestException as e:
        print(f"요청 에러: {e}")
    except Exception as e:
        print(f"파싱 에러: {e}")

print("\n" + "=" * 80)
print("추가: 학교 API로 ATPT_OFCDE 확인")
print("=" * 80)

# schoolInfo API로 교육청 코드 확인
try:
    url = f"{base_url}/schoolInfo"
    params = {
        'KEY': api_key,
        'Type': 'json',
        'SD_SCHUL_CODE': '7130197'
    }
    response = requests.get(url, params=params, timeout=10)
    data = response.json()
    
    if 'schoolInfo' in data and len(data['schoolInfo']) > 1:
        school_info = data['schoolInfo'][1]
        print(f"응답 구조: {list(school_info.keys())}")
        
        if 'row' in school_info and len(school_info['row']) > 0:
            row = school_info['row'][0]
            print(f"\n학교 정보:")
            print(f"  ATPT_OFCDC_SC_CODE: {row.get('ATPT_OFCDC_SC_CODE')}")
            print(f"  SCHUL_NM: {row.get('SCHUL_NM')}")
            print(f"  SD_SCHUL_CODE: {row.get('SD_SCHUL_CODE')}")
            print(f"  전체 키: {list(row.keys())}")
            
except Exception as e:
    print(f"에러: {e}")
