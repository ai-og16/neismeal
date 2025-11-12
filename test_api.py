import requests
import json

api_key = "3aeace82f952472ab2151a44cf0e736b"
base_url = "https://open.neis.go.kr/hub"

# 교육청 코드 10 (서울)
# 학교 행정 코드 30197 (이미지 예제)

print("=" * 60)
print("NEIS API 테스트")
print("=" * 60)

# 1. 학교 정보 조회
print("\n1. 학교 정보 조회")
url = f"{base_url}/schoolInfo"
params = {
    'KEY': api_key,
    'Type': 'json',
    'ATPT_OFCDE': '10',
    'SD_SCHUL_CODE': '30197'
}
print(f"URL: {url}")
print(f"Params: {params}")

try:
    response = requests.get(url, params=params, timeout=5)
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text[:500]}")
    data = response.json()
    print(f"Response JSON: {json.dumps(data, indent=2, ensure_ascii=False)[:1000]}")
except Exception as e:
    print(f"Error: {e}")

# 2. 급식 정보 조회
print("\n\n2. 급식 정보 조회")
url = f"{base_url}/mealServiceDietInfo"
params = {
    'KEY': api_key,
    'Type': 'json',
    'ATPT_OFCDE': '10',
    'SD_SCHUL_CODE': '30197',
    'MLSV_YMD': '20251112'
}
print(f"URL: {url}")
print(f"Params: {params}")

try:
    response = requests.get(url, params=params, timeout=5)
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text[:500]}")
    data = response.json()
    print(f"Response JSON: {json.dumps(data, indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"Error: {e}")
