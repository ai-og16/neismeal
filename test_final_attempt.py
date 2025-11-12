import requests
import json

# NEIS API 공식 문서에서 얻은 정보:
# 급식식단정보 API의 필수 파라미터 분석

api_key = "3aeace82f952472ab2151a44cf0e736b"
base_url = "https://open.neis.go.kr/hub"

print("=" * 80)
print("NEIS 급식식단정보 API - 공식 문서 기반 재분석")
print("=" * 80)

# NEIS API 공식 문서에 따르면:
# 필수 요청 인자:
# - KEY: 인증키
# - Type: 응답 형식 (json/xml)
# - pIndex: 페이지 번호
# - pSize: 페이지당 출력 건수
# - ATPT_OFCDE: 교육청 코드
# - SD_SCHUL_CODE: 학교 행정 코드  
# - MLSV_YMD: 급식 제공 일자 (YYYYMMDD)

# 그런데 ERROR-300이 계속 나옴 = 뭔가 더 필수 파라미터가 있을 것

# API 포털 페이지에서 실제 요청 데이터를 본 다른 사용자들의 정보:
# - SCHUL_NM: 학교 이름
# - SCHUL_KND: 학교 구분

test_cases = [
    {
        'name': '기본 필수 + SCHUL_NM',
        'params': {
            'KEY': api_key,
            'Type': 'json',
            'pIndex': 1,
            'pSize': 100,
            'ATPT_OFCDE': 'B10',
            'SD_SCHUL_CODE': '7130197',
            'MLSV_YMD': '20251112',
            'SCHUL_NM': '오금중학교'
        }
    },
    {
        'name': '기본 필수 + SCHUL_KND',
        'params': {
            'KEY': api_key,
            'Type': 'json',
            'pIndex': 1,
            'pSize': 100,
            'ATPT_OFCDE': 'B10',
            'SD_SCHUL_CODE': '7130197',
            'MLSV_YMD': '20251112',
            'SCHUL_KND': 'M'  # M: 중학교, H: 고등학교 등
        }
    },
    {
        'name': '기본 필수 + SCHUL_KND (03)',
        'params': {
            'KEY': api_key,
            'Type': 'json',
            'pIndex': 1,
            'pSize': 100,
            'ATPT_OFCDE': 'B10',
            'SD_SCHUL_CODE': '7130197',
            'MLSV_YMD': '20251112',
            'SCHUL_KND': '03'  # 중학교 코드
        }
    },
    {
        'name': '기본 필수 + 양쪽 다 (SCHUL_NM + SCHUL_KND)',
        'params': {
            'KEY': api_key,
            'Type': 'json',
            'pIndex': 1,
            'pSize': 100,
            'ATPT_OFCDE': 'B10',
            'SD_SCHUL_CODE': '7130197',
            'MLSV_YMD': '20251112',
            'SCHUL_NM': '오금중학교',
            'SCHUL_KND': 'M'
        }
    },
    {
        'name': 'API 필터 없이 교육청만',
        'params': {
            'KEY': api_key,
            'Type': 'json',
            'pIndex': 1,
            'pSize': 100,
            'ATPT_OFCDE': 'B10',
            'MLSV_YMD': '20251112'
        }
    },
    {
        'name': 'CULI_COURSE_SC_CODE 추가',
        'params': {
            'KEY': api_key,
            'Type': 'json',
            'pIndex': 1,
            'pSize': 100,
            'ATPT_OFCDE': 'B10',
            'SD_SCHUL_CODE': '7130197',
            'MLSV_YMD': '20251112',
            'CULI_COURSE_SC_CODE': '1'  # 1: 중식, 2: 조식
        }
    },
]

for test in test_cases:
    print(f"\n[{test['name']}]")
    
    try:
        response = requests.get(f"{base_url}/mealServiceDietInfo", params=test['params'], timeout=10)
        data = response.json()
        
        if 'RESULT' in data:
            code = data['RESULT']['CODE']
            msg = data['RESULT']['MESSAGE']
            print(f"결과: {code} - {msg}")
        
        if 'mealServiceDietInfo' in data:
            meals = data['mealServiceDietInfo']
            print(f"[SUCCESS] mealServiceDietInfo 발견! ({len(meals)}개)")
            if len(meals) > 1:
                print(f"데이터: {json.dumps(meals[1], ensure_ascii=False)}")
        
        # RESULT가 없고 다른 키가 있으면
        if 'RESULT' not in data and 'mealServiceDietInfo' not in data:
            print(f"응답: {data}")
            
    except Exception as e:
        print(f"에러: {e}")

print("\n" + "=" * 80)
print("깃허브/오픈소스 참고 - 알려진 작동 파라미터")
print("=" * 80)

# 여러 오픈소스 프로젝트에서 확인된 작동하는 파라미터
working_params = {
    'KEY': api_key,
    'Type': 'json',
    'pIndex': 1,
    'pSize': 100,
    'ATPT_OFCDE': 'B10',
    'SD_SCHUL_CODE': '7130197',
    'MLSV_YMD': '20251113'
}

print(f"\n테스트 URL:")
print(f"{base_url}/mealServiceDietInfo?{'&'.join(f'{k}={v}' for k,v in working_params.items())}")

try:
    response = requests.get(f"{base_url}/mealServiceDietInfo", params=working_params, timeout=10)
    data = response.json()
    print(f"\n응답: {json.dumps(data, ensure_ascii=False, indent=2)}")
    
except Exception as e:
    print(f"에러: {e}")
