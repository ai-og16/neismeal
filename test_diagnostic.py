"""
NEIS API ERROR-300 문제 진단 및 해결

NEIS API mealServiceDietInfo에서 ERROR-300이 나오는 이유:
API 서버에서 필수 파라미터 검증이 엄격함.
실제로는 필수 파라미터들이 정확한 형식이어야 함.

관찰된 패턴:
- schoolInfo API는 잘 작동함 (SD_SCHUL_CODE로 학교 조회 가능)
- mealServiceDietInfo는 ERROR-300 계속 발생
- 많은 오픈소스 프로젝트도 같은 문제 리포트

해결책:
1. schoolInfo API로 학교 정보 조회 후 모든 필드 저장
2. 그 정보를 기반으로 mealServiceDietInfo 호출
3. 또는 다른 급식 정보 소스 사용
"""

import requests
import json

api_key = "3aeace82f952472ab2151a44cf0e736b"
base_url = "https://open.neis.go.kr/hub"

# 1단계: schoolInfo로 정확한 학교 정보 조회
print("=" * 80)
print("1단계: 학교 정보 상세 조회")
print("=" * 80)

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
        school_data = data['schoolInfo'][1]['row'][0]
        
        print("\n학교 정보:")
        for key, value in school_data.items():
            print(f"  {key}: {value}")
        
        # 필요한 정보 추출
        atpt_code = school_data.get('ATPT_OFCDC_SC_CODE')
        sd_code = school_data.get('SD_SCHUL_CODE')
        school_name = school_data.get('SCHUL_NM')
        school_kind = school_data.get('SCHUL_KND_SC_NM')
        
        print(f"\n추출된 정보:")
        print(f"  교육청 코드: {atpt_code}")
        print(f"  학교 코드: {sd_code}")
        print(f"  학교명: {school_name}")
        print(f"  학교 종류: {school_kind}")
        
except Exception as e:
    print(f"학교 정보 조회 실패: {e}")
    exit(1)

# 2단계: 추출한 정보로 급식 정보 조회
print("\n" + "=" * 80)
print("2단계: 급식 정보 조회")
print("=" * 80)

test_params = [
    {
        'name': '기본 파라미터',
        'params': {
            'KEY': api_key,
            'Type': 'json',
            'pIndex': 1,
            'pSize': 100,
            'ATPT_OFCDE': atpt_code,
            'SD_SCHUL_CODE': sd_code,
            'MLSV_YMD': '20251113'
        }
    },
    {
        'name': '문자열로 변환한 파라미터',
        'params': {
            'KEY': api_key,
            'Type': 'json',
            'pIndex': '1',
            'pSize': '100',
            'ATPT_OFCDE': str(atpt_code),
            'SD_SCHUL_CODE': str(sd_code),
            'MLSV_YMD': '20251113'
        }
    },
]

for test in test_params:
    print(f"\n[{test['name']}]")
    print(f"파라미터: {test['params']}")
    
    try:
        response = requests.get(f"{base_url}/mealServiceDietInfo", params=test['params'], timeout=10)
        data = response.json()
        
        print(f"응답: {json.dumps(data, ensure_ascii=False, indent=2)}")
        
    except Exception as e:
        print(f"에러: {e}")

# 3단계: 모든 가능한 필드로 재시도
print("\n" + "=" * 80)
print("3단계: 추가 필드 시도")
print("=" * 80)

# 학교 종류에 따른 코드 매핑
school_kind_map = {
    '유치원': '01',
    '초등학교': '02',
    '중학교': '03',
    '고등학교': '04',
    '특수학교': '05'
}

school_kind_code = school_kind_map.get(school_kind, '03')

advanced_params = {
    'KEY': api_key,
    'Type': 'json',
    'pIndex': 1,
    'pSize': 100,
    'ATPT_OFCDE': atpt_code,
    'SD_SCHUL_CODE': sd_code,
    'MLSV_YMD': '20251113',
    'SCHUL_NM': school_name,
    'SCHUL_KND_SC_CODE': school_kind_code
}

print(f"확장 파라미터로 시도:")
print(f"{advanced_params}")

try:
    response = requests.get(f"{base_url}/mealServiceDietInfo", params=advanced_params, timeout=10)
    data = response.json()
    print(f"응답: {json.dumps(data, ensure_ascii=False, indent=2)}")
    
except Exception as e:
    print(f"에러: {e}")
