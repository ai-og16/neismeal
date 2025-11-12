import requests

api_key = "3aeace82f952472ab2151a44cf0e736b"
base_url = "https://open.neis.go.kr/hub"

# 교육청 코드 변환 함수
def convert_atpt_code(code_str):
    """교육청 코드 B10을 숫자로 변환"""
    atpt_map = {
        'B10': '27',  # 서울특별시교육청
        'C10': '28',  # 부산광역시교육청
        'D10': '29',  # 대구광역시교육청
        'E10': '30',  # 인천광역시교육청
        'F10': '31',  # 광주광역시교육청
        'G10': '32',  # 대전광역시교육청
        'H10': '33',  # 울산광역시교육청
        'I10': '34',  # 세종특별자치시교육청
        'J10': '35',  # 경기도교육청
        'K10': '36',  # 강원도교육청
        'M10': '37',  # 충청북도교육청
        'N10': '38',  # 충청남도교육청
        'O10': '39',  # 전라북도교육청
        'P10': '40',  # 전라남도교육청
        'Q10': '41',  # 경상북도교육청
        'R10': '42',  # 경상남도교육청
        'S10': '43',  # 제주도교육청
    }
    
    # B10 형식이면 변환
    if code_str in atpt_map:
        return atpt_map[code_str]
    
    # 이미 숫자면 그대로 반환
    return code_str

print("=" * 60)
print("교육청 코드 변환 테스트")
print("=" * 60)

# 여러 교육청 코드 형식 테스트
test_codes = [
    ("B10", "7130197"),   # B10 형식
    ("27", "7130197"),    # 숫자 형식
    ("02", "7130197"),    # 두자리 숫자
]

for atpt_code, sd_code in test_codes:
    print(f"\n교육청 코드: {atpt_code}, 학교 코드: {sd_code}")
    
    params = {
        'KEY': api_key,
        'Type': 'json',
        'ATPT_OFCDE': atpt_code,
        'SD_SCHUL_CODE': sd_code,
        'MLSV_YMD': '20251112'
    }
    
    try:
        response = requests.get(f"{base_url}/mealServiceDietInfo", params=params, timeout=5)
        data = response.json()
        
        if 'RESULT' in data:
            print(f"  RESULT: {data['RESULT']['MESSAGE']}")
        elif 'mealServiceDietInfo' in data:
            meals = data['mealServiceDietInfo']
            if len(meals) > 1:
                print(f"  ✓ 급식 데이터 발견!")
                meal = meals[1]
                if isinstance(meal, dict):
                    print(f"    메뉴: {meal.get('DDISH_NM', 'N/A')}")
            else:
                print(f"  응답은 있으나 데이터 없음")
        else:
            print(f"  응답 키: {list(data.keys())}")
            
    except Exception as e:
        print(f"  에러: {e}")

print("\n" + "=" * 60)
print("숫자로 변환하여 재시도")
print("=" * 60)

converted = convert_atpt_code("B10")
print(f"B10 변환 -> {converted}")

params = {
    'KEY': api_key,
    'Type': 'json',
    'ATPT_OFCDE': converted,
    'SD_SCHUL_CODE': '7130197',
    'MLSV_YMD': '20251112'
}

try:
    response = requests.get(f"{base_url}/mealServiceDietInfo", params=params, timeout=5)
    print(f"요청 URL: {response.url}")
    data = response.json()
    print(f"응답: {data}")
    
except Exception as e:
    print(f"에러: {e}")
