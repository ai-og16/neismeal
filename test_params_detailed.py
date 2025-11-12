import requests
import json
from datetime import datetime, timedelta

api_key = "3aeace82f952472ab2151a44cf0e736b"
base_url = "https://open.neis.go.kr/hub"

print("=" * 80)
print("ERROR-300 해결 - NEIS API 필수 파라미터 찾기")
print("=" * 80)

# 파라미터 추가 시도들
test_configs = [
    {
        'name': 'pIndex, pSize 필수',
        'params': {
            'KEY': api_key,
            'Type': 'json',
            'pIndex': '1',
            'pSize': '100',
            'ATPT_OFCDE': 'B10',
            'SD_SCHUL_CODE': '7130197',
            'MLSV_YMD': '20251112'
        }
    },
    {
        'name': 'SERVICE 파라미터 추가',
        'params': {
            'KEY': api_key,
            'Type': 'json',
            'SERVICE': 'mealServiceDietInfo',
            'pIndex': '1',
            'pSize': '100',
            'ATPT_OFCDE': 'B10',
            'SD_SCHUL_CODE': '7130197',
            'MLSV_YMD': '20251112'
        }
    },
    {
        'name': '교육청명 영문으로',
        'params': {
            'KEY': api_key,
            'Type': 'json',
            'ATPT_OFCDE': 'B10',
            'SD_SCHUL_CODE': '7130197',
            'MLSV_YMD': '20251112',
            'pIndex': '1',
            'pSize': '100'
        }
    },
    {
        'name': '주(週) 파라미터',
        'params': {
            'KEY': api_key,
            'Type': 'json',
            'ATPT_OFCDE': 'B10',
            'SD_SCHUL_CODE': '7130197',
            'MLSV_FROM_YMD': '20251110',
            'MLSV_TO_YMD': '20251112'
        }
    },
    {
        'name': 'URL에 /mealServiceDietInfo 직접 포함',
        'url_override': f"{base_url}/mealServiceDietInfo",
        'params': {
            'KEY': api_key,
            'Type': 'json',
            'ATPT_OFCDE': 'B10',
            'SD_SCHUL_CODE': '7130197',
            'MLSV_YMD': '20251112'
        }
    },
    {
        'name': 'CCTSRMSEQ 파라미터',
        'params': {
            'KEY': api_key,
            'Type': 'json',
            'ATPT_OFCDE': 'B10',
            'SD_SCHUL_CODE': '7130197',
            'MLSV_YMD': '20251112',
            'CCTSRMSEQ': '1'  # 학사일정 참고
        }
    },
]

for config in test_configs:
    print(f"\n[{config['name']}]")
    
    url = config.get('url_override', f"{base_url}/mealServiceDietInfo")
    params = config['params']
    
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"상태: {response.status_code}")
        
        data = response.json()
        
        # 응답 분석
        if 'RESULT' in data:
            code = data['RESULT']['CODE']
            msg = data['RESULT']['MESSAGE']
            status = "❌" if 'ERROR' in code else "✓"
            print(f"{status} RESULT: {code} - {msg}")
        
        if 'mealServiceDietInfo' in data:
            meals = data['mealServiceDietInfo']
            print(f"✓ mealServiceDietInfo 발견! ({len(meals)}개 아이템)")
            
            if len(meals) > 1:
                for idx, meal in enumerate(meals[1:3]):  # 처음 2개만 출력
                    print(f"  [{idx}] {json.dumps(meal, ensure_ascii=False)[:150]}")
        
        # 다른 키가 있는지 확인
        other_keys = [k for k in data.keys() if k not in ['RESULT', 'mealServiceDietInfo']]
        if other_keys:
            print(f"다른 응답 키: {other_keys}")
            
    except Exception as e:
        print(f"❌ 에러: {e}")

print("\n" + "=" * 80)
print("특정 날짜 범위로 시도")
print("=" * 80)

# 오늘부터 일주일을 범위로 설정
today = datetime.now()

range_tests = [
    {
        'name': '오늘',
        'date': today.strftime('%Y%m%d')
    },
    {
        'name': '내일',
        'date': (today + timedelta(days=1)).strftime('%Y%m%d')
    },
    {
        'name': '어제',
        'date': (today - timedelta(days=1)).strftime('%Y%m%d')
    },
    {
        'name': '일주일 뒤',
        'date': (today + timedelta(days=7)).strftime('%Y%m%d')
    },
]

for test in range_tests:
    print(f"\n[{test['name']} ({test['date']}) 조회]")
    
    params = {
        'KEY': api_key,
        'Type': 'json',
        'pIndex': '1',
        'pSize': '100',
        'ATPT_OFCDE': 'B10',
        'SD_SCHUL_CODE': '7130197',
        'MLSV_YMD': test['date']
    }
    
    try:
        response = requests.get(f"{base_url}/mealServiceDietInfo", params=params, timeout=10)
        data = response.json()
        
        if 'RESULT' in data:
            code = data['RESULT']['CODE']
            msg = data['RESULT']['MESSAGE']
            if code == 'INFO-000':
                print(f"✓ 성공!")
            else:
                print(f"  {code}: {msg}")
        
        if 'mealServiceDietInfo' in data:
            meals = data['mealServiceDietInfo']
            print(f"  mealServiceDietInfo: {len(meals)}개 아이템")
            
    except Exception as e:
        print(f"  에러: {e}")
