import requests
import json

api_key = "3aeace82f952472ab2151a44cf0e736b"
base_url = "https://open.neis.go.kr/hub"

print("=" * 80)
print("NEIS API 사용 가능한 서비스 목록 확인")
print("=" * 80)

# 사용 가능한 모든 API 서비스 목록
services = [
    'academy',
    'acaGyeong',
    'acaFeature',
    'acaPay',
    'acaSangseo',
    'acaTypCd',
    'acaWelfareFacility',
    'classroomEquipment',
    'dongkumTongbanDong',
    'dongkumTongbanRi',
    'dongkumTongban',
    'excRetirement',
    'excService',
    'excTransfer',
    'foodCode',  # 식재 코드
    'foodAllergy',  # 식재 알레르기
    'foodInfo',  # 식재 정보
    'foodOrigin',  # 식재 원산지
    'fundingEducation',
    'mealServiceDietInfo',  # 급식 식단 정보
    'mealServiceInfo',  # 급식 정보
    'schoolBasicInfo',
    'schoolInfo',
    'schoolSchedule',
    'specialization',
    'supplierMeal'
]

print("테스트 중인 서비스들...")

for service in services:
    try:
        url = f"{base_url}/{service}"
        params = {
            'KEY': api_key,
            'Type': 'json',
            'ATPT_OFCDE': 'B10',
            'SD_SCHUL_CODE': '7130197',
            'MLSV_YMD': '20251112'
        }
        
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        
        # 에러 코드 확인
        if 'RESULT' in data:
            code = data['RESULT']['CODE']
            msg = data['RESULT']['MESSAGE']
            
            if code == 'INFO-000':
                print(f"✓ {service}: 성공! MESSAGE={msg}")
            elif code == 'ERROR-300':
                print(f"  {service}: ERROR-300 (필수값 누락)")
            elif code == 'ERROR-310':
                print(f"  {service}: ERROR-310 (서비스 없음)")
            else:
                print(f"  {service}: {code} - {msg}")
        else:
            # RESULT가 없으면 데이터가 있을 수도
            if service in data:
                print(f"✓ {service}: 데이터 있음! 키={list(data.keys())}")
            else:
                print(f"  {service}: 응답 키={list(data.keys())}")
                
    except Exception as e:
        print(f"  {service}: 에러 - {str(e)[:40]}")

print("\n" + "=" * 80)
print("가장 가능성 높은 서비스들 상세 테스트")
print("=" * 80)

# 가능한 파라미터 조합들 테스트
test_params_list = [
    {
        'name': 'mealServiceDietInfo - 표준 파라미터',
        'service': 'mealServiceDietInfo',
        'params': {
            'KEY': api_key,
            'Type': 'json',
            'ATPT_OFCDE': 'B10',
            'SD_SCHUL_CODE': '7130197',
            'MLSV_YMD': '20251112'
        }
    },
    {
        'name': 'foodInfo - 식재 정보',
        'service': 'foodInfo',
        'params': {
            'KEY': api_key,
            'Type': 'json',
            'ATPT_OFCDE': 'B10',
            'SD_SCHUL_CODE': '7130197'
        }
    },
    {
        'name': 'mealServiceInfo - 급식 정보',
        'service': 'mealServiceInfo',
        'params': {
            'KEY': api_key,
            'Type': 'json',
            'ATPT_OFCDE': 'B10',
            'SD_SCHUL_CODE': '7130197'
        }
    },
]

for test in test_params_list:
    print(f"\n[{test['name']}]")
    try:
        url = f"{base_url}/{test['service']}"
        response = requests.get(url, params=test['params'], timeout=5)
        data = response.json()
        
        print(f"응답: {json.dumps(data, ensure_ascii=False, indent=2)[:300]}")
        
    except Exception as e:
        print(f"에러: {e}")
