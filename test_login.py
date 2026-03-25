"""
测试登录功能
"""
import requests
import json

url = "http://localhost:8000/api/v1/auth/login"
data = {
    "username": "testuser",
    "password": "123456"
}

print(f"测试登录: {data['username']} / {data['password']}")
print("=" * 50)

try:
    response = requests.post(url, json=data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

    if response.status_code == 200:
        print("\n✅ 登录成功！")
        token = response.json().get('access_token')
        print(f"Token: {token[:50]}...")
    else:
        print("\n❌ 登录失败")

except Exception as e:
    print(f"❌ 错误: {e}")