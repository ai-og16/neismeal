import requests
import json

api_key = "3aeace82f952472ab2151a44cf0e736b"
base_url = "https://open.neis.go.kr/hub"

print("=" * 80)
print("NEIS API 디버깅 - 웹사이트 참고값으로 재구성")
print("=" * 80)

# 이미지에서 보인 파라미터들을 정확히 분석
# 교육청 코드 (ATPT): B10
# 학교 행정 코드 (SD): 7130197  -> 잘못됨! 실제로는 30197
# 조회 시작일: 2025-11-12

# 이미지에 있는 올바른 데이터로 다시 시도
test_cases = [
    {
        'name': '이미지의 정확한 값 (30197)',
        'atpt': 'B10',
        'sd_code': '30197',
        'meal_date': '20251112'
    },
    {
        'name': '30197 앞에 01 추가',
        'atpt': 'B10',
        'sd_code': '0130197',
        'meal_date': '20251112'
    },
    {
        'name': '30197 앞에 7 추가',
        'atpt': 'B10',
        'sd_code': '730197',
        'meal_date': '20251112'
    },
    {
        'name': '원래 7130197 사용',
        'atpt': 'B10',
        'sd_code': '7130197',
        'meal_date': '20251112'
    },
]

for test in test_cases:
    print(f"\n[{test['name']}]")
    print(f"  파라미터: ATPT={test['atpt']}, SD_SCHUL_CODE={test['sd_code']}, MLSV_YMD={test['meal_date']}")
    
    params = {
        'KEY': api_key,
        'Type': 'json',
        'ATPT_OFCDE': test['atpt'],
        'SD_SCHUL_CODE': test['sd_code'],
        'MLSV_YMD': test['meal_date']
    }
    
    try:
        response = requests.get(f"{base_url}/mealServiceDietInfo", params=params, timeout=10)
        data = response.json()
        
        if 'RESULT' in data:
            code = data['RESULT']['CODE']
            msg = data['RESULT']['MESSAGE']
            print(f"  결과: {code} - {msg}")
        
        if 'mealServiceDietInfo' in data:
            meals = data['mealServiceDietInfo']
            print(f"  ✓ mealServiceDietInfo 응답 발견! (아이템 수: {len(meals)})")
            if len(meals) > 1:
                print(f"    데이터: {json.dumps(meals[1], ensure_ascii=False)[:100]}")
                
    except Exception as e:
        print(f"  에러: {e}")

print("\n" + "=" * 80)
print("학교 코드 확인 - 다시 검색")
print("=" * 80)

try:
    url = f"{base_url}/schoolInfo"
    params = {
        'KEY': api_key,
        'Type': 'json',
        'SCHUL_NM': '오금중'  # 부분 일치로 검색
    }
    
    response = requests.get(url, params=params, timeout=10)
    data = response.json()
    
    if 'schoolInfo' in data and len(data['schoolInfo']) > 1:
        schools = data['schoolInfo'][1]['row']
        print(f"검색된 학교 ({len(schools)}개):")
        
        for school in schools:
            print(f"  - {school.get('SCHUL_NM')}")
            print(f"    SD_SCHUL_CODE: {school.get('SD_SCHUL_CODE')}")
            print(f"    ATPT_OFCDC_SC_CODE: {school.get('ATPT_OFCDC_SC_CODE')}")
            print()
            
except Exception as e:
    print(f"에러: {e}")
